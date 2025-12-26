"""Enumeraciones para tipos de cambio y monedas soportadas por Banxico SIE"""

from enum import Enum


class Currency(Enum):
    """
    Monedas soportadas por el SIE de Banxico
    
    Cada moneda tiene asociada su serie de Banxico
    """
    USD = "SF43718"  # Dólar estadounidense (FIX)
    USD_PAGOS = "SF60653"  # Dólar estadounidense (Para liquidación)
    CAD = "SF57770"  # Dólar canadiense  
    EUR = "SF46410"  # Euro
    JPY = "SF46406"  # Yen japonés
    
    @property
    def name_es(self) -> str:
        """Retorna el nombre en español de la moneda"""
        names = {
            "USD": "Dólar estadounidense",
            "USD_PAGOS": "Dólar estadounidense",
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
            "USD_PAGOS": "$",
            "CAD": "C$",
            "EUR": "€",
            "JPY": "¥"
        }
        return symbols[self.name]
    
    @property
    def tipo(self) -> str:
        """Retorna el tipo de cambio de la serie"""
        if self == Currency.USD_PAGOS:
            return "Para liquidación (obligaciones)"
        return "FIX - Determinación publicada en DOF"

