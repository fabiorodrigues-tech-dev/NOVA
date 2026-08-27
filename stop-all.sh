#!/usr/bin/env bash
# ==============================================================================
# 🛑 NOVA — Script de Parada Unificada (stop-all.sh)
# Finaliza limpa e seguramente todos os 3 serviços do ecossistema NOVA.
# ==============================================================================

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOGS_DIR="$ROOT_DIR/logs"

echo "======================================================================"
echo "🛑 FINALIZANDO SERVIÇOS DO ECOSSISTEMA NOVA"
echo "======================================================================"

# Função para matar por PID e por Porta
stop_service() {
    local name=$1
    local port=$2
    local pid_file="$LOGS_DIR/$3.pid"

    echo "🔻 Parando $name..."

    # 1. Tenta matar pelo arquivo de PID
    if [ -f "$pid_file" ]; then
        PID=$(cat "$pid_file" 2>/dev/null || true)
        if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
            kill "$PID" 2>/dev/null || true
            sleep 0.5
            if kill -0 "$PID" 2>/dev/null; then
                kill -9 "$PID" 2>/dev/null || true
            fi
            echo "   ↳ Processo PID $PID finalizado."
        fi
        rm -f "$pid_file"
    fi

    # 2. Garante que nada ficou travando a porta
    PORT_PIDS=$(lsof -ti :"$port" 2>/dev/null || true)
    if [ -n "$PORT_PIDS" ]; then
        echo "   ↳ Liberando porta $port (PIDs: $PORT_PIDS)..."
        kill -9 $PORT_PIDS 2>/dev/null || true
    fi

    echo "   ✅ $name parado (Porta $port liberada)."
}

# Para os 3 serviços
stop_service "Agente Financeiro (Spring Boot)" 8081 "financeiro"
stop_service "NOVA Control Center (Dashboard)" 3000 "dashboard"
stop_service "NOVA Voice Studio" 5050 "voz"

echo ""
echo "======================================================================"
echo "✨ TODOS OS SERVIÇOS DO NOVA FORAM ENCERRADOS COM SUCESSO!"
echo "======================================================================"
