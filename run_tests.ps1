# Script de PowerShell para ejecutar pytest
# Uso: .\run_tests.ps1 [opciones de pytest]

# Activar el entorno virtual
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "Activando entorno virtual..." -ForegroundColor Green
    & .venv\Scripts\Activate.ps1
} else {
    Write-Host "Error: No se encontró el entorno virtual. Ejecuta: uv venv" -ForegroundColor Red
    exit 1
}

# Ejecutar pytest con los argumentos pasados
if ($args.Count -gt 0) {
    Write-Host "Ejecutando: pytest $args" -ForegroundColor Cyan
    pytest $args
} else {
    Write-Host "Ejecutando: pytest -v" -ForegroundColor Cyan
    pytest -v
}
