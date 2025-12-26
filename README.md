# 💱 Banxico SIE

Cliente Python para consultar tipos de cambio del Sistema de Información Económica (SIE) de Banxico.

## 🚀 Instalación

```bash
pip install banxico-sie-xp
```

O desde el source:

```bash
git clone https://github.com/soyrushian/banxico-sie.git
cd banxico-sie
pip install -e .
```

## 🔑 Requisitos

Necesitas un token de la API de Banxico. Lo consigues gratis aquí:
👉 https://www.banxico.org.mx/SieAPIRest/service/v1/token

## 💡 Uso

### Setup básico

```python
from banxico_sie import BanxicoSIEClient, Currency

# Inicializa el cliente con tu token
client = BanxicoSIEClient("tu_token_aqui")
```

### Consultar tipo de cambio actual

```python
# USD FIX (por determinación)
usd = client.get_rate(Currency.USD)
print(f"USD: ${usd['valor']} MXN")

# USD para liquidación
usd_pagos = client.get_rate(Currency.USD_PAGOS)
print(f"USD PAGOS: ${usd_pagos['valor']} MXN")

# Otras monedas
eur = client.get_rate(Currency.EUR)
cad = client.get_rate(Currency.CAD)
jpy = client.get_rate(Currency.JPY)
```

### Consultar fecha específica

```python
from datetime import datetime

# Fecha específica como string
rate = client.get_rate(Currency.USD, fecha="2024-12-01")
print(f"USD el 1 dic 2024: ${rate['valor']}")

# Fecha como datetime
rate = client.get_rate(Currency.EUR, fecha=datetime(2024, 11, 15))
```

### Rango de fechas

```python
# Histórico USD FIX
historico = client.get_rates_range(
    Currency.USD,
    start_date="2024-01-01",
    end_date="2024-12-31"
)

# Histórico USD para liquidación
historico_pagos = client.get_rates_range(
    Currency.USD_PAGOS,
    start_date="2024-01-01",
    end_date="2024-12-31"
)

for rate in historico:
    print(f"{rate['fecha']}: ${rate['valor']}")
```

### Obtener el más reciente

```python
# Último USD FIX
latest = client.get_latest(Currency.USD)
print(f"Último USD: ${latest['valor']} ({latest['fecha']})")

# Último USD para liquidación
latest_pagos = client.get_latest(Currency.USD_PAGOS)
print(f"Último USD PAGOS: ${latest_pagos['valor']} ({latest_pagos['fecha']})")
```

## 🌍 Monedas disponibles

```python
Currency.USD        # 🇺🇸 Dólar (FIX - Determinación DOF)
Currency.USD_PAGOS  # 🇺🇸 Dólar (Para liquidación)
Currency.EUR        # 🇪🇺 Euro
Currency.CAD        # 🇨🇦 Dólar canadiense
Currency.JPY        # 🇯🇵 Yen japonés
```

## 📦 Estructura de respuesta

```python
{
    'fecha': '26/12/2024',
    'moneda': 'USD',
    'moneda_nombre': 'Dólar estadounidense',
    'simbolo': '$',
    'valor': 20.3456,
    'tipo': 'FIX - Determinación publicada en DOF'
}
```

Para `Currency.USD_PAGOS`:
```python
{
    'fecha': '26/12/2024',
    'moneda': 'USD',
    'moneda_nombre': 'Dólar estadounidense',
    'simbolo': '$',
    'valor': 20.4567,
    'tipo': 'Para liquidación (obligaciones)'
}
```

## 📋 Series de Banxico

| Currency | Serie | Tipo |
|----------|-------|------|
| `Currency.USD` | SF60652 | FIX - Determinación publicada en DOF |
| `Currency.USD_PAGOS` | SF60653 | Para liquidación de obligaciones |
| `Currency.EUR` | SF46410 | FIX |
| `Currency.CAD` | SF43687 | FIX |
| `Currency.JPY` | SF46406 | FIX |

## 🔥 Ejemplos prácticos

### Comparar USD FIX vs PAGOS

```python
usd_fix = client.get_rate(Currency.USD)
usd_pagos = client.get_rate(Currency.USD_PAGOS)

print(f"USD FIX: ${usd_fix['valor']:.4f}")
print(f"USD PAGOS: ${usd_pagos['valor']:.4f}")
print(f"Diferencia: ${abs(usd_fix['valor'] - usd_pagos['valor']):.4f}")
```

### Histórico con análisis

```python
from datetime import datetime, timedelta

hace_mes = datetime.now() - timedelta(days=30)
historico = client.get_rates_range(
    Currency.USD,
    start_date=hace_mes,
    end_date=datetime.now()
)

valores = [r['valor'] for r in historico if r['valor']]
print(f"Mínimo: ${min(valores):.4f}")
print(f"Máximo: ${max(valores):.4f}")
print(f"Promedio: ${sum(valores)/len(valores):.4f}")
```

### Tabla de todas las monedas

```python
monedas = [Currency.USD, Currency.USD_PAGOS, Currency.EUR, Currency.CAD, Currency.JPY]

for moneda in monedas:
    rate = client.get_rate(moneda)
    print(f"{rate['simbolo']} {rate['moneda']}: ${rate['valor']:.4f} MXN")
```

## 🛠️ Desarrollo

### Instalar dependencias de desarrollo

```bash
pip install -e ".[dev]"
```

### Correr tests

```bash
pytest
```

### Formatear código

```bash
black src/ tests/
```

### Linter

```bash
flake8 src/ tests/
```

## 📝 Licencia

MIT License - puedes hacer lo que quieras con este código.

## 🤝 Contribuir

Pull requests son bienvenidos. Para cambios grandes, abre un issue primero para discutir qué te gustaría cambiar.

## ⚠️ Disclaimer

Este paquete no está afiliado con el Banco de México. Usa los datos bajo tu propio riesgo y verifica la información crítica directamente con fuentes oficiales.

## 🔗 Links útiles

- [API de Banxico SIE](https://www.banxico.org.mx/SieAPIRest/service/v1/)
- [Documentación oficial](https://www.banxico.org.mx/SieAPIRest/service/swagger-ui.html#/Series)
- [Catálogo de series](https://www.banxico.org.mx/SieAPIRest/service/v1/doc/catalogoSeries)

## 📮 Contacto

Issues: https://github.com/soyrushian/banxico-sie/issues
