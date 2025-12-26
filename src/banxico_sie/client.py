"""Cliente principal para interactuar con la API del SIE de Banxico"""

import requests
from datetime import datetime, date
from typing import Union, List, Dict, Optional
from dateutil.parser import parse as parse_date

from .enums import Currency, RateType
from .exceptions import (
    BanxicoAPIError,
    BanxicoAuthError,
    BanxicoRateLimitError,
    BanxicoDataNotFoundError,
)


class BanxicoSIEClient:
    """
    Cliente para consultar tipos de cambio del Sistema de Información Económica (SIE) de Banxico
    
    Args:
        api_token: Token de API de Banxico (obtener en https://www.banxico.org.mx/SieAPIRest/service/v1/)
        timeout: Timeout para las peticiones HTTP en segundos (default: 30)
    
    Example:
        >>> client = BanxicoSIEClient("tu_token_aqui")
        >>> rate = client.get_rate(Currency.USD)
        >>> print(f"USD: ${rate['valor']}")
    """
    
    BASE_URL = "https://www.banxico.org.mx/SieAPIRest/service/v1/series"
    
    def __init__(self, api_token: str, timeout: int = 30):
        if not api_token:
            raise ValueError("Se requiere un token de API válido")
        
        self.api_token = api_token
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Bmx-Token": api_token,
            "Accept": "application/json"
        })
    
    def _format_date(self, date_obj: Union[str, date, datetime]) -> str:
        """
        Convierte fecha a formato YYYY-MM-DD requerido por la API
        
        Args:
            date_obj: Fecha como string, date o datetime
            
        Returns:
            Fecha en formato YYYY-MM-DD
        """
        if isinstance(date_obj, str):
            date_obj = parse_date(date_obj)
        return date_obj.strftime("%Y-%m-%d")
    
    def _make_request(self, series_ids: List[str], start_date: str, end_date: str) -> Dict:
        """
        Realiza la petición HTTP a la API de Banxico
        
        Args:
            series_ids: Lista de IDs de series a consultar
            start_date: Fecha inicial en formato YYYY-MM-DD
            end_date: Fecha final en formato YYYY-MM-DD
            
        Returns:
            Respuesta JSON de la API
            
        Raises:
            BanxicoAuthError: Si el token es inválido
            BanxicoRateLimitError: Si se excede el límite de peticiones
            BanxicoAPIError: Para otros errores de la API
        """
        series_str = ",".join(series_ids)
        url = f"{self.BASE_URL}/{series_str}/datos/{start_date}/{end_date}"
        
        try:
            response = self.session.get(url, timeout=self.timeout)
            
            # Manejo de errores HTTP
            if response.status_code == 401:
                raise BanxicoAuthError(
                    status_code=response.status_code,
                    response=response.json() if response.content else None
                )
            elif response.status_code == 429:
                raise BanxicoRateLimitError(
                    status_code=response.status_code,
                    response=response.json() if response.content else None
                )
            elif response.status_code >= 400:
                raise BanxicoAPIError(
                    f"Error HTTP {response.status_code}",
                    status_code=response.status_code,
                    response=response.json() if response.content else None
                )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            raise BanxicoAPIError("Timeout al conectar con la API de Banxico")
        except requests.exceptions.ConnectionError:
            raise BanxicoAPIError("Error de conexión con la API de Banxico")
        except requests.exceptions.RequestException as e:
            raise BanxicoAPIError(f"Error en la petición: {str(e)}")
    
    def _parse_response(self, data: Dict, currency: Currency) -> List[Dict]:
        """
        Parsea la respuesta JSON de la API
        
        Args:
            data: Respuesta JSON de la API
            currency: Moneda consultada
            
        Returns:
            Lista de diccionarios con los datos parseados
            
        Raises:
            BanxicoDataNotFoundError: Si no hay datos disponibles
            BanxicoAPIError: Si hay error parseando la respuesta
        """
        try:
            series_data = data["bmx"]["series"][0]["datos"]
            
            if not series_data:
                raise BanxicoDataNotFoundError(
                    f"No hay datos disponibles para {currency.name_es}"
                )
            
            results = []
            for item in series_data:
                results.append({
                    "fecha": item["fecha"],
                    "moneda": currency.name,
                    "moneda_nombre": currency.name_es,
                    "simbolo": currency.symbol,
                    "valor": float(item["dato"]) if item["dato"] else None
                })
            
            return results
            
        except (KeyError, IndexError) as e:
            raise BanxicoAPIError(f"Error parseando respuesta de Banxico: {e}")
    
    def get_rate(
        self,
        currency: Currency,
        fecha: Optional[Union[str, date, datetime]] = None,
        rate_type: RateType = RateType.FIX
    ) -> Dict:
        """
        Obtiene el tipo de cambio para una fecha específica
        
        Args:
            currency: Moneda a consultar (USD, EUR, CAD, JPY)
            fecha: Fecha de consulta (default: fecha actual)
            rate_type: Tipo de cambio (FIX o PAGOS)
            
        Returns:
            Dict con la información del tipo de cambio:
            {
                'fecha': '2024-12-26',
                'moneda': 'USD',
                'moneda_nombre': 'Dólar estadounidense',
                'simbolo': '$',
                'valor': 20.3456,
                'tipo': 'fix',
                'tipo_descripcion': 'Tipo de cambio FIX, Publicación DOF'
            }
            
        Raises:
            BanxicoDataNotFoundError: Si no hay datos para la fecha
            BanxicoAPIError: Para otros errores
            
        Example:
            >>> rate = client.get_rate(Currency.USD, fecha="2024-12-01")
            >>> print(f"{rate['moneda']}: ${rate['valor']}")
        """
        if fecha is None:
            fecha = datetime.now()
        
        fecha_str = self._format_date(fecha)
        data = self._make_request([currency.value], fecha_str, fecha_str)
        results = self._parse_response(data, currency)
        
        if not results:
            raise BanxicoDataNotFoundError(
                f"No hay datos disponibles para {currency.name_es} en {fecha_str}"
            )
        
        result = results[0]
        result["tipo"] = rate_type.value
        result["tipo_descripcion"] = rate_type.description
        
        return result
    
    def get_rates_range(
        self,
        currency: Currency,
        start_date: Union[str, date, datetime],
        end_date: Union[str, date, datetime],
        rate_type: RateType = RateType.FIX
    ) -> List[Dict]:
        """
        Obtiene tipos de cambio para un rango de fechas
        
        Args:
            currency: Moneda a consultar (USD, EUR, CAD, JPY)
            start_date: Fecha inicial del rango
            end_date: Fecha final del rango
            rate_type: Tipo de cambio (FIX o PAGOS)
            
        Returns:
            Lista de dicts con los tipos de cambio para cada fecha
            
        Raises:
            BanxicoDataNotFoundError: Si no hay datos para el rango
            BanxicoAPIError: Para otros errores
            
        Example:
            >>> rates = client.get_rates_range(
            ...     Currency.USD,
            ...     start_date="2024-01-01",
            ...     end_date="2024-01-31"
            ... )
            >>> for rate in rates:
            ...     print(f"{rate['fecha']}: ${rate['valor']}")
        """
        start_str = self._format_date(start_date)
        end_str = self._format_date(end_date)
        
        data = self._make_request([currency.value], start_str, end_str)
        results = self._parse_response(data, currency)
        
        for result in results:
            result["tipo"] = rate_type.value
            result["tipo_descripcion"] = rate_type.description
        
        return results
    
    def get_latest(
        self,
        currency: Currency,
        rate_type: RateType = RateType.FIX
    ) -> Dict:
        """
        Obtiene el tipo de cambio más reciente disponible
        
        Args:
            currency: Moneda a consultar (USD, EUR, CAD, JPY)
            rate_type: Tipo de cambio (FIX o PAGOS)
            
        Returns:
            Dict con el tipo de cambio más reciente
            
        Example:
            >>> latest = client.get_latest(Currency.EUR)
            >>> print(f"Último EUR: ${latest['valor']} ({latest['fecha']})")
        """
        return self.get_rate(currency, rate_type=rate_type)