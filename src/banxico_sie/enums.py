"""Enumeraciones para tipos de cambio y monedas soportadas por Banxico SIE"""

from enum import Enum


class Currency(Enum):
    """
    Monedas soportadas por el SIE de Banxico
    
    Los valores corresponden a las series del SIE para tipo de cambio FIX
    """
    USD = "SF43718"  # Dólar estadounidense
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


class RateType(Enum):
    """
    Tipos de tipo de cambio disponibles en Banxico
    
    FIX: Tipo de cambio oficial publicado en el Diario Oficial de la Federación
    PAGOS: Tipo de cambio para solventar obligaciones denominadas en moneda extranjera
    """
    FIX = "fix"  # FIX, Publicación DOF
    PAGOS = "pagos"  # Para pagos
    
    @property
    def description(self) -> str:
        """Retorna la descripción del tipo de cambio"""
        descriptions = {
            "fix": "Tipo de cambio FIX, Publicación DOF",
            "pagos": "Tipo de cambio para pagos"
        }
        return descriptions[self.value]