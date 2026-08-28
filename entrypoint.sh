#!/usr/bin/env bash
# ==============================================================================
# NOVA — Cloud Container Entrypoint (Docker & Render 24/7)
# Inicializa o microsserviço Spring Boot em background e o Dashboard Web em foreground.
# ==============================================================================

set -e

echo "======================================================================"
echo "🌌 INICIALIZANDO NOVA CONTROL CENTER EM NUVEM (DOCKER RUNTIME 24/7)"
echo "======================================================================"

HTTP_PORT="${PORT:-10000}"
export NOVA_PORT="$HTTP_PORT"

echo "☕ [1/2] Iniciando Agente Financeiro (Spring Boot 3.3 na porta 8081)..."
java ${JAVA_OPTS:--Xms128m -Xmx384m} -jar /app/agente-financeiro.jar > /tmp/financeiro.log 2>&1 &
SPRING_PID=$!
echo "   ↳ Spring Boot iniciado com PID $SPRING_PID (Log: /tmp/financeiro.log)"

echo "⏳ Aguardando aquecimento do Spring Boot..."
for i in $(seq 1 30); do
    if curl -s http://127.0.0.1:8081/api/transacoes/resumo > /dev/null 2>&1; then
        echo "   ✅ Spring Boot API pronta e operacional na porta 8081!"
        break
    fi
    sleep 1
done

echo "🧭 [2/2] Iniciando NOVA Control Center Dashboard na porta $HTTP_PORT..."
echo "======================================================================"
echo "✨ ECOSSISTEMA PRONTO PARA TRÁFEGO WEB EM PRODUÇÃO!"
echo "======================================================================"

exec python3 /app/dashboard/server.py --port "$HTTP_PORT"
