#!/usr/bin/env bash
# ==============================================================================
# 🚀 NOVA — Script de Inicialização Unificada (start-all.sh)
# Sobe simultaneamente os 3 serviços do ecossistema em background com logs dedicados.
# 1. Agente Financeiro (Java 21 / Spring Boot 3 na porta 8081)
# 2. NOVA Control Center Dashboard (Python Web na porta 3000)
# 3. NOVA Voice Studio (Python Web na porta 5050)
# ==============================================================================

set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOGS_DIR="$ROOT_DIR/logs"
mkdir -p "$LOGS_DIR"

echo "======================================================================"
echo "🌌 INICIALIZANDO ECOSSISTEMA MULTI-AGENTE NOVA"
echo "======================================================================"

# Função auxiliar para verificar se porta está em uso
check_port() {
    local port=$1
    if lsof -ti :"$port" >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# 1. Agente Financeiro (Spring Boot / Java 21)
if check_port 8081; then
    echo "⚠️  Porta 8081 já em uso. Agente Financeiro já está rodando."
else
    echo "☕ [1/3] Iniciando Agente Financeiro (Spring Boot na porta 8081)..."
    cd "$ROOT_DIR/java-services/agente-financeiro"
    mvn compile -q
    if [ ! -f "cp.txt" ]; then
        mvn dependency:build-classpath -Dmdep.outputFile=cp.txt -q
    fi
    nohup java -cp "target/classes:$(cat cp.txt)" com.nova.agentefinanceiro.AgenteFinanceiroApplication > "$LOGS_DIR/financeiro.log" 2>&1 &
    FIN_PID=$!
    echo $FIN_PID > "$LOGS_DIR/financeiro.pid"
    echo "   ↳ PID: $FIN_PID | Log: logs/financeiro.log"
fi

# 2. NOVA Control Center Dashboard
if check_port 3000; then
    echo "⚠️  Porta 3000 já em uso. Dashboard já está rodando."
else
    echo "🧭 [2/3] Iniciando NOVA Control Center (Dashboard na porta 3000)..."
    cd "$ROOT_DIR"
    nohup python3 dashboard/server.py > "$LOGS_DIR/dashboard.log" 2>&1 &
    DASH_PID=$!
    echo $DASH_PID > "$LOGS_DIR/dashboard.pid"
    echo "   ↳ PID: $DASH_PID | Log: logs/dashboard.log"
fi

# 3. NOVA Voice Studio
if check_port 5050; then
    echo "⚠️  Porta 5050 já em uso. Voice Studio já está rodando."
else
    echo "🎙️  [3/3] Iniciando NOVA Voice Studio (Voz Neural na porta 5050)..."
    cd "$ROOT_DIR"
    nohup python3 voz/scripts/voice_studio_app.py > "$LOGS_DIR/voz.log" 2>&1 &
    VOZ_PID=$!
    echo $VOZ_PID > "$LOGS_DIR/voz.pid"
    echo "   ↳ PID: $VOZ_PID | Log: logs/voz.log"
fi

# Aguarda 2 segundos para estabilização inicial dos processos rápidos
sleep 2

echo ""
echo "======================================================================"
echo "✨ TODOS OS SERVIÇOS DO NOVA FORAM DISPARADOS COM SUCESSO!"
echo "======================================================================"
echo ""
echo "📱 PAINEL UNIFICADO & ENDPOINTS:"
echo "   • 🌐 Domínio Limpo:                       http://nova.local:3000"
echo "   • 🌐 Acesso Local Padrão:                 http://localhost:3000"
echo "     ├── 🧭 Dashboard Executivo & KPIs (Bento Grid)"
echo "     ├── 🎙️ NOVA Voice Assistant (Microfone & Síntese Base64)"
echo "     └── 🎛️ NOVA Voice Studio Integrado (Laboratório & Catálogo de Vozes)"
echo "   • ☕ Agente Financeiro (Spring Boot 3):   http://localhost:8081/api/transacoes/resumo"
echo "   • 🔧 Voice Studio Backend (Proxy Interno): http://localhost:5050"
echo ""
echo "📂 LOGS EM TEMPO REAL:"
echo "   • Financeiro: tail -f logs/financeiro.log"
echo "   • Dashboard:  tail -f logs/dashboard.log"
echo "   • Voz:        tail -f logs/voz.log"
echo ""
echo "🛑 Para parar todos os serviços, execute: ./stop-all.sh"
echo "======================================================================"
