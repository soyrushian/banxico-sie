"""Enumeraciones para tipos de cambio y monedas soportadas por Banxico SIE"""

from enum import Enum
from typing import Optional


class Currency(Enum):
    """
    Monedas soportadas por el SIE de Banxico
    
    Los valores corresponden a las series del SIE para tipo de cambio FIX
    """
    USD = "SF43718"  # Dólar estadounidense (tipo FIX)
    CAD = "SF43687"  # Dólar canadiense  
    EUR = "SF46410"  # Euro
    JPY = "SF46406"  # Yen japonés
    
    @property
    def name_es(self) -> str:
        """Retorna el nombre en español de la moneda"""
        names = {
            "USD": "Dólar estadounidense",
            "CAD": "Dólar canadiense",
            "EUR": "Euro",
            "JPY": "Yen japonés"
        }
        return names[self.name]
    
    @property
    def symbol(self) -> str:
        """Retorna el símbolo de la moneda"""
        symbols = {
            "USD": "$",
            "CAD": "C$",
            "EUR": "€",
            "JPY": "¥"
        }
        return symbols[self.name]
    
    def get_series_id(self, rate_type: 'RateType' = None) -> str:
        """
        Retorna el ID de serie según el tipo de cambio
        
        Args:
            rate_type: Tipo de cambio (solo aplica para USD)
            
        Returns:
            ID de serie de Banxico
        """
        # Solo USD soporta múltiples tipos de cambio
        if self == Currency.USD and rate_type is not None:
            if rate_type == RateType.PAGOS:
                return "SF60653"  # Para liquidación
            elif rate_type == RateType.FIX:
                return "SF60652"  # Por determinación (FIX)
        
        # Para otras monedas o sin especificar tipo, usar el valor por defecto
        return self.value
    
    @property
    def supports_rate_types(self) -> bool:
        """Indica si la moneda soporta múltiples tipos de cambio"""
        return self == Currency.USD


class RateType(Enum):
    """
    Tipos de tipo de cambio disponibles en Banxico
    
    FIX: Tipo de cambio por determinación (FIX), publicado en el DOF
    PAGOS: Tipo de cambio para liquidación de obligaciones
    
    Nota: Solo USD soporta ambos tipos. Otras monedas solo tienen FIX.
    """
    FIX = "fix"  # Por determinación (FIX), Publicación DOF
    PAGOS = "pagos"  # Para liquidación
    
    @property
    def description(self) -> str:
        """Retorna la descripción del tipo de cambio"""
        descriptions = {
            "fix": "Tipo de cambio por determinación (FIX), Publicación DOF",
            "pagos": "Tipo de cambio para liquidación de obligaciones"
        }
        return descriptions[self.value]
