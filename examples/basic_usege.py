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
    
    # Ejemplo 1: USD con diferentes tipos
    print("\n1. Tipos de cambio USD (FIX vs PAGOS):")
    try:
        usd_fix = client.get_rate(Currency.USD, rate_type=RateType.FIX)
        print(f"   USD FIX (Por determinación): ${usd_fix['valor']:.4f} MXN")
        print(f"   - {usd_fix['tipo_descripcion']}")
        print(f"   - Fecha: {usd_fix['fecha']}")
        
        usd_pagos = client.get_rate(Currency.USD, rate_type=RateType.PAGOS)
        print(f"\n   USD PAGOS (Para liquidación): ${usd_pagos['valor']:.4f} MXN")
        print(f"   - {usd_pagos['tipo_descripcion']}")
        print(f"   - Fecha: {usd_pagos['fecha']}")
        
        diferencia = abs(usd_fix['valor'] - usd_pagos['valor'])
        print(f"\n   Diferencia: ${diferencia:.4f} MXN")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Ejemplo 2: Otras monedas (solo FIX)
    print("\n2. Otras monedas (solo tipo FIX disponible):")
    monedas = [Currency.EUR, Currency.CAD, Currency.JPY]
    
    for moneda in monedas:
        try:
            rate = client.get_rate(moneda)
            print(f"   {rate['simbolo']} {rate['moneda']}: ${rate['valor']:.4f} MXN")
        except Exception as e:
            print(f"   {moneda.name}: Error - {e}")
    
    # Ejemplo 3: Validación de tipo PAGOS
    print("\n3. Validación: PAGOS solo funciona con USD")
    try:
        # Esto lanzará un ValueError
        eur_pagos = client.get_rate(Currency.EUR, rate_type=RateType.PAGOS)
    except ValueError as e:
        print(f"   ✓ Error esperado: {e}")
    except Exception as e:
        print(f"   Error inesperado: {e}")
    
    # Ejemplo 4: Histórico USD comparando tipos
    print("\n4. Histórico USD última semana (FIX vs PAGOS):")
    try:
        hoy = datetime.now()
        hace_semana = hoy - timedelta(days=7)
        
        historico_fix = client.get_rates_range(
            Currency.USD,
            start_date=hace_semana,
            end_date=hoy,
            rate_type=RateType.FIX
        )
        
        historico_pagos = client.get_rates_range(
            Currency.USD,
            start_date=hace_semana,
            end_date=hoy,
            rate_type=RateType.PAGOS
        )
        
        print(f"   Registros FIX: {len(historico_fix)}")
        print(f"   Registros PAGOS: {len(historico_pagos)}")
        
        print("\n   Últimos 3 días:")
        print("   Fecha         | FIX      | PAGOS    | Dif")
        print("   " + "-" * 48)
        
        for i in range(min(3, len(historico_fix), len(historico_pagos))):
            fix_val = historico_fix[-(i+1)]['valor']
            pagos_val = historico_pagos[-(i+1)]['valor']
            diff = abs(fix_val - pagos_val)
            fecha = historico_fix[-(i+1)]['fecha']
            
            print(f"   {fecha} | ${fix_val:.4f} | ${pagos_val:.4f} | ${diff:.4f}")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    # Ejemplo 5: Análisis USD FIX último mes
    print("\n5. Análisis USD FIX último mes:")
    try:
        hoy = datetime.now()
        hace_mes = hoy - timedelta(days=30)
        
        historico = client.get_rates_range(
            Currency.USD,
            start_date=hace_mes,
            end_date=hoy,
            rate_type=RateType.FIX
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
    
    # Ejemplo 6: Análisis USD PAGOS último mes
    print("\n6. Análisis USD PAGOS último mes:")
    try:
        hoy = datetime.now()
        hace_mes = hoy - timedelta(days=30)
        
        historico = client.get_rates_range(
            Currency.USD,
            start_date=hace_mes,
            end_date=hoy,
            rate_type=RateType.PAGOS
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
    
    # Ejemplo 7: Comparación todas las monedas (FIX)
    print("\n7. Tabla comparativa - Todas las monedas (tipo FIX):")
    try:
        print("   Moneda    | Valor MXN  | Símbolo | Tipo")
        print("   " + "-" * 50)
        
        for moneda in [Currency.USD, Currency.EUR, Currency.CAD, Currency.JPY]:
            rate = client.get_rate(moneda, rate_type=RateType.FIX)
            print(f"   {moneda.name:<8} | ${rate['valor']:>9.4f} | {rate['simbolo']:<7} | FIX")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Ejemplo 8: get_latest con ambos tipos
    print("\n8. Último tipo de cambio disponible:")
    try:
        latest_fix = client.get_latest(Currency.USD, rate_type=RateType.FIX)
        latest_pagos = client.get_latest(Currency.USD, rate_type=RateType.PAGOS)
        
        print(f"   USD FIX: ${latest_fix['valor']:.4f} ({latest_fix['fecha']})")
        print(f"   USD PAGOS: ${latest_pagos['valor']:.4f} ({latest_pagos['fecha']})")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 60)
    print("Ejemplos completados!")
    print("\nNOTA: Solo USD soporta tipo PAGOS.")
    print("      Otras monedas solo tienen tipo FIX.")
    print("=" * 60)


if __name__ == "__main__":
    main()
