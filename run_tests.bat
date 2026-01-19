@echo off
REM Script batch para ejecutar pytest en Windows
REM Uso: run_tests.bat [opciones de pytest]

echo Activando entorno virtual...
call .venv\Scripts\activate.bat

if %errorlevel% neq 0 (
    echo Error: No se encontro el entorno virtual. Ejecuta: uv venv
    exit /b 1
)

if "%1"=="" (
    echo Ejecutando: pytest -v
    pytest -v
) else (
    echo Ejecutando: pytest %*
    pytest %*
)
