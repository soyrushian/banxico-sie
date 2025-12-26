"""
Ejemplos básicos de uso del cliente banxico-sie

Antes de ejecutar, asegúrate de:
1. Tener un token de Banxico (https://www.banxico.org.mx/SieAPIRest/service/v1/)
2. Instalar el paquete: pip install banxico-sie
3. Configurar tu token en una variable de ambiente o directamente en el código
"""

import os
from datetime import datetime, timedelta
from banxico_sie import BanxicoSIEClient, Currency, RateType


def main():
    # Obtén tu token de la API de Banxico
    # Lo ideal es usar variables de ambiente
    token = os.getenv("BANXICO_TOKEN", "tu_token_aqui")
    
    # Inicializa el cliente
    client = BanxicoSIEClient(token)
    
    print("=" * 60)
    print("EJEMPLOS DE USO - BANXICO SIE")
    print("=" * 60)
    
    # Ejemplo 1: Tipo de cambio actual
    print("\n1. Tipo de cambio USD actual (FIX):")
    try:
        usd = client.get_rate(Currency.USD)
        print(f"   {usd['simbolo']} {usd['moneda']}: ${usd['valor']:.4f} MXN")
        print(f"   Fecha: {usd['fecha']}")
        print(f"   Tipo: {usd['tipo_descripcion']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Ejemplo 2: Múltiples monedas
    print("\n2. Tipos de cambio actuales de todas las monedas:")
    monedas = [Currency.USD, Currency.EUR, Currency.CAD, Currency.JPY]
    
    for moneda in monedas:
        try:
            rate = client.get_rate(moneda)
            print(f"   {rate['simbolo']} {rate['moneda']}: ${rate['valor']:.4f} MXN")
        except Exception as e:
            print(f"   {moneda.name}: Error - {e}")
    
    # Ejemplo 3: Fecha específica
    print("\n3. USD del 1 de diciembre 2024:")
    try:
        usd_historico = client.get_rate(
            Currency.USD,
            fecha="2024-12-01"
        )
        print(f"   Valor: ${usd_historico['valor']:.4f} MXN")
        print(f"   Fecha: {usd_historico['fecha']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Ejemplo 4: Tipo de cambio para pagos
    print("\n4. EUR tipo 'Para pagos':")
    try:
        eur_pagos = client.get_rate(
            Currency.EUR,
            rate_type=RateType.PAGOS
        )
        print(f"   {eur_pagos['simbolo']} EUR: ${eur_pagos['valor']:.4f} MXN")
        print(f"   Tipo: {eur_pagos['tipo_descripcion']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Ejemplo 5: Rango de fechas (última semana)
    print("\n5. USD última semana:")
    try:
        hoy = datetime.now()
        hace_semana = hoy - timedelta(days=7)
        
        historico = client.get_rates_range(
            Currency.USD,
            start_date=hace_semana,
            end_date=hoy
        )
        
        print(f"   Datos obtenidos: {len(historico)} días")
        print("   Últimos 3 registros:")
        for rate in historico[-3:]:
            print(f"   - {rate['fecha']}: ${rate['valor']:.4f}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Ejemplo 6: Análisis básico
    print("\n6. Análisis USD último mes:")
    try:
        hoy = datetime.now()
        hace_mes = hoy - timedelta(days=30)
        
        historico = client.get_rates_range(
            Currency.USD,
            start_date=hace_mes,
            end_date=hoy
        )
        
        valores = [r['valor'] for r in historico if r['valor'] is not None]
        
        if valores:
            minimo = min(valores)
            maximo = max(valores)
            promedio = sum(valores) / len(valores)
            
            print(f"   Mínimo: ${minimo:.4f}")
            print(f"   Máximo: ${maximo:.4f}")
            print(f"   Promedio: ${promedio:.4f}")
            print(f"   Variación: ${maximo - minimo:.4f} ({((maximo/minimo - 1) * 100):.2f}%)")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Ejemplo 7: Comparación de monedas
    print("\n7. Comparación de monedas (hoy):")
    try:
        print("   Moneda    | Valor MXN  | Símbolo")
        print("   " + "-" * 38)
        
        for moneda in [Currency.USD, Currency.EUR, Currency.CAD, Currency.JPY]:
            rate = client.get_rate(moneda)
            print(f"   {moneda.name:<8} | ${rate['valor']:>9.4f} | {rate['simbolo']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 60)
    print("Ejemplos completados!")
    print("=" * 60)


if __name__ == "__main__":
    main()