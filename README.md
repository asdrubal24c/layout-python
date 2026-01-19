# Rick and Morty API Client

Cliente asíncrono profesional en Python para consumir la API de Rick and Morty ([rickandmortyapi.com](https://rickandmortyapi.com/)). Este proyecto sigue los estándares modernos de desarrollo Python (2026) con tipado fuerte, linting, testing con mocks, y CI/CD robusto.

## 🚀 Características principales

- **Cliente asíncrono** usando `httpx.AsyncClient` para realizar peticiones HTTP no bloqueantes
- **Modelos de datos** definidos con `Pydantic` y type hints completos, permitiendo validación fuerte y tipado estático con `mypy --strict`
- **Tests robustos** escritos con `pytest` y `pytest-asyncio`
- **Mocking de la API** usando `respx` para simular respuestas HTTP, garantizando que los tests pasen incluso sin conexión a internet o si la API deja de estar disponible
- **CI/CD automatizado** con GitHub Actions que ejecuta linting, type checking y tests en cada push/PR

## 📋 Requisitos

- Python 3.10 o superior
- [uv](https://github.com/astral-sh/uv) como gestor de paquetes

## 🛠️ Instalación

1. Clona el repositorio:
   ```bash
   git clone <repository-url>
   cd layout-python
   ```

2. Instala las dependencias usando `uv`:
   ```bash
   uv pip install -e ".[dev]"
   ```

   O si prefieres usar un entorno virtual:
   ```bash
   uv venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   uv pip install -e ".[dev]"
   ```

## 💻 Uso

### Ejemplo básico

```python
import asyncio
from src.client import RickAndMortyClient

async def main():
    async with RickAndMortyClient() as client:
        character = await client.get_character(1)
        print(f"Nombre: {character.name}")
        print(f"Estado: {character.status}")
        print(f"Especie: {character.species}")
        print(f"Origen: {character.origin.name}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Ejemplo con manejo de errores

```python
import asyncio
import httpx
from src.client import RickAndMortyClient

async def main():
    try:
        async with RickAndMortyClient() as client:
            character = await client.get_character(1)
            print(character.name)
    except httpx.HTTPStatusError as e:
        print(f"Error HTTP: {e.response.status_code}")
    except httpx.RequestError as e:
        print(f"Error de conexión: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 🧪 Testing y Mocks

### ¿Por qué usar Mocks?

Los **mocks** son fundamentales para garantizar un CI/CD robusto porque:

1. **Independencia de servicios externos**: Los tests no dependen de la disponibilidad de la API de Rick and Morty
2. **Velocidad**: Los tests se ejecutan más rápido al no realizar peticiones HTTP reales
3. **Confiabilidad**: Los tests son determinísticos y no fallan por problemas de red o cambios en la API
4. **Control total**: Podemos simular diferentes escenarios (éxito, errores 404, 500, timeouts, etc.)

### Cómo funcionan los mocks en este proyecto

Este proyecto usa [`respx`](https://github.com/lundberg/respx) para interceptar las peticiones HTTP de `httpx` y simular respuestas. Esto permite:

- **Simular respuestas exitosas** con datos de prueba
- **Simular errores HTTP** (404, 500, etc.)
- **Verificar que las peticiones se realizan correctamente**
- **Ejecutar tests sin conexión a internet**

### Ejemplo de test con mock

```python
import pytest
import httpx
import respx
from src.client import RickAndMortyClient

@pytest.mark.asyncio
async def test_get_character_success(respx_mock):
    """Test que simula una respuesta exitosa de la API."""
    url = "https://rickandmortyapi.com/api/character/1"
    
    fake_response = {
        "id": 1,
        "name": "Rick Sanchez",
        "status": "Alive",
        # ... más datos
    }
    
    # Mock de la petición HTTP
    route = respx_mock.get(url).mock(
        return_value=httpx.Response(status_code=200, json=fake_response)
    )
    
    async with RickAndMortyClient() as client:
        character = await client.get_character(1)
    
    assert route.called  # Verifica que se hizo la petición
    assert character.name == "Rick Sanchez"
```

### Ejecutar los tests

```bash
# Ejecutar todos los tests
pytest

# Ejecutar con más verbosidad
pytest -v

# Ejecutar un test específico
pytest tests/test_client.py::test_get_character_success
```

## 🔍 Calidad de código

### Ruff (Linter y Formatter)

Ruff se usa para:
- **Linting**: Detectar errores y problemas de estilo
- **Formatting**: Formatear el código automáticamente

```bash
# Verificar estilo y errores
ruff check .

# Formatear código
ruff format .

# Verificar formato sin aplicar cambios
ruff format --check .
```

### Mypy (Type Checking)

Mypy se ejecuta en modo `strict` para garantizar tipado completo:

```bash
# Verificar tipos
mypy src tests
```

## 🚀 CI/CD (GitHub Actions)

El workflow configurado en `.github/workflows/ci.yml` se ejecuta automáticamente en cada push y pull request hacia las ramas principales. El workflow:

1. **Instala el proyecto** con `uv`
2. **Ejecuta Ruff** para verificar linting y formato
3. **Ejecuta Mypy** para verificar tipos
4. **Ejecuta los tests** con `pytest`

### Ventajas del CI/CD con Mocks

Gracias al uso de mocks, el CI/CD:

- ✅ **No requiere conexión a internet** para ejecutar los tests
- ✅ **Es rápido y determinístico** (no depende de latencia de red)
- ✅ **No falla por problemas de la API externa** (caídas, cambios, rate limiting)
- ✅ **Puede ejecutarse en cualquier momento** sin preocuparse por la disponibilidad de servicios externos

## 📁 Estructura del proyecto

```
layout-python/
├── .github/
│   └── workflows/
│       └── ci.yml              # Workflow de GitHub Actions
├── src/
│   ├── __init__.py
│   ├── client.py               # Cliente asíncrono
│   └── models.py               # Modelos Pydantic
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Configuración de pytest y fixtures
│   └── test_client.py          # Tests con mocks
├── pyproject.toml              # Configuración del proyecto y dependencias
└── README.md                   # Este archivo
```

## 🛠️ Tecnologías utilizadas

- **[httpx](https://www.python-httpx.org/)**: Cliente HTTP asíncrono
- **[Pydantic](https://docs.pydantic.dev/)**: Validación de datos y modelos
- **[pytest](https://pytest.org/)**: Framework de testing
- **[pytest-asyncio](https://pytest-asyncio.readthedocs.io/)**: Soporte para tests asíncronos
- **[respx](https://github.com/lundberg/respx)**: Mocking de peticiones HTTP
- **[Ruff](https://docs.astral.sh/ruff/)**: Linter y formatter ultra-rápido
- **[Mypy](https://mypy.readthedocs.io/)**: Type checker estático
- **[uv](https://github.com/astral-sh/uv)**: Gestor de paquetes moderno y rápido

## 📝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Asegúrate de que todos los tests pasen: `pytest`
2. Verifica que Ruff no reporte errores: `ruff check .`
3. Verifica que Mypy pase: `mypy src tests`
4. Añade tests para nuevas funcionalidades
5. Mantén el tipado completo y documentación actualizada

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

## 🔗 Referencias

- [API de Rick and Morty](https://rickandmortyapi.com/)
- [Documentación de httpx](https://www.python-httpx.org/)
- [Documentación de Pydantic](https://docs.pydantic.dev/)
- [Documentación de respx](https://github.com/lundberg/respx)
