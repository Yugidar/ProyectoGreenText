#!/bin/bash
echo "=== INICIANDO PIPELINE DE SEGURIDAD ==="
FALLOS=0

echo "[1] Revisando secretos en el codigo..."
gitleaks detect --no-git --source ./app -v --redact > reportes/gitleaks.txt 2>&1
if [ $? -ne 0 ]; then
    echo "  [X] UMBRAL SUPERADO: Se detectaron secretos"
    FALLOS=$((FALLOS+1))
else
    echo "  [OK] Cero secretos encontrados."
fi

echo "[2] Revisando infraestructura (Terraform)..."
trivy config infra/foro_infra.tf --severity HIGH,CRITICAL --exit-code 1 > reportes/trivy_iac.txt 2>&1
if [ $? -ne 0 ]; then
    echo "  [X] UMBRAL SUPERADO: Vulnerabilidad en IaC"
    FALLOS=$((FALLOS+1))
else
    echo "  [OK] Infraestructura segura."
fi

echo "[3] Revisando dependencias de Python..."

docker run --rm -v $(pwd):/workspace -w /workspace python:3.10 bash -c "pip install -q pip-audit && pip-audit -r app/api/requirements.txt" > reportes/pip_audit.txt 2>&1

if [ $? -ne 0 ]; then
    echo "  [X] UMBRAL SUPERADO: Dependencia vulnerable encontrada"
    FALLOS=$((FALLOS+1))
else
    echo "  [OK] Dependencias limpias."
fi

echo "[4] Analisis Estatico de Codigo (Semgrep)..."
semgrep scan --config auto --error ./app > reportes/semgrep.txt 2>&1
if [ $? -ne 0 ]; then
    echo "  [X] UMBRAL SUPERADO: Vulnerabilidades de codigo detectadas por Semgrep"
    FALLOS=$((FALLOS+1))
else
    echo "  [OK] Codigo fuente seguro."
fi

echo "======================================="
if [ $FALLOS -gt 0 ]; then
    echo "VEREDICTO FINAL: BLOQUEADO ($FALLOS controles fallaron)"
    exit 1
else
    echo "VEREDICTO FINAL: PERMITIDO (Todos los controles en verde)"
    exit 0
fi
