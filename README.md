# 💱 Banxico SIE

Cliente Python para consultar tipos de cambio del Sistema de Información Económica (SIE) de Banxico.

## 🚀 Instalación

```bash
pip install banxico-sie
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
from banxico_sie import BanxicoSIEClient, Currency, RateType

# Inicializa el cliente con tu token
client = BanxicoSIEClient("tu_token_aqui")
```

### Consultar tipo de cambio actual

```python
# Dólar del día (FIX - Publicación DOF)
usd = client.get_rate(Currency.USD)
print(f"USD: ${usd['valor']} MXN")

# Euro con tipo "Para pagos"
eur = client.get_rate(Currency.EUR, rate_type=RateType.PAGOS)
print(f"EUR: ${eur['valor']} MXN")
```

### Consultar fecha específica

```python
from datetime import datetime

# Fecha específica
rate = client.get_rate(
    Currency.USD,
    fecha="2024-12-01"
)
print(f"USD el 1 dic 2024: ${rate['valor']}")

# También acepta objetos datetime
rate = client.get_rate(
    Currency.JPY,
    fecha=datetime(2024, 11, 15)
)
```

### Rango de fechas

```python
# Histórico de tipos de cambio
historico = client.get_rates_range(
    Currency.USD,
    start_date="2024-01-01",
    end_date="2024-12-31"
)

for rate in historico:
    print(f"{rate['fecha']}: ${rate['valor']}")
```

### Obtener el más reciente disponible

```python
# Último tipo de cambio publicado
latest = client.get_latest(Currency.CAD)
print(f"Último CAD: ${latest['valor']} ({latest['fecha']})")
```

## 🌍 Monedas disponibles

```python
Currency.USD  # 🇺🇸 Dólar estadounidense
Currency.CAD  # 🇨🇦 Dólar canadiense
Currency.EUR  # 🇪🇺 Euro
Currency.JPY  # 🇯🇵 Yen japonés
```

## 📊 Tipos de cambio

```python
RateType.FIX    # FIX - Publicación DOF (default)
RateType.PAGOS  # Para pagos
```

**Nota:** Actualmente Banxico publica principalmente el tipo FIX. El tipo PAGOS puede no estar disponible para todas las fechas.

## 📦 Estructura de respuesta

### get_rate() y get_latest()

```python
{
    'fecha': '2024-12-26',
    'moneda': 'USD',
    'moneda_nombre': 'Dólar estadounidense',
    'valor': 20.3456,
    'tipo': 'fix',
    'tipo_descripcion': 'Tipo de cambio FIX, Publicación DOF'
}
```

### get_rates_range()

```python
[
    {
        'fecha': '2024-12-01',
        'moneda': 'USD',
        'moneda_nombre': 'Dólar estadounidense',
        'valor': 20.1234,
        'tipo': 'fix',
        'tipo_descripcion': 'Tipo de cambio FIX, Publicación DOF'
    },
    {
        'fecha': '2024-12-02',
        'moneda': 'USD',
        'moneda_nombre': 'Dólar estadounidense',
        'valor': 20.2345,
        'tipo': 'fix',
        'tipo_descripcion': 'Tipo de cambio FIX, Publicación DOF'
    },
    # ...
]
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
