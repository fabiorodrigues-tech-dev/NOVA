#!/usr/bin/env bash
# ==============================================================================
# NOVA — Script de Configuração de Domínio Local (http://nova.local)
# Configura o mapeamento 127.0.0.1 nova.local no /etc/hosts do macOS
# ==============================================================================

set -e

HOST_ENTRY="127.0.0.1 nova.local"
HOSTS_FILE="/etc/hosts"

echo "======================================================================"
echo "🌐 CONFIGURAÇÃO DE DOMÍNIO LOCAL DO NOVA (http://nova.local)"
echo "======================================================================"

# Verifica se a entrada já existe no /etc/hosts
if grep -q "nova.local" "$HOSTS_FILE"; then
    echo "✅ A entrada 'nova.local' já está presente em $HOSTS_FILE."
else
    echo "🔧 Adicionando '$HOST_ENTRY' ao seu $HOSTS_FILE..."
    if [ "$EUID" -ne 0 ]; then
        echo "🔐 Solicitando permissão de administrador (sudo) para atualizar $HOSTS_FILE:"
        sudo sh -c "echo '$HOST_ENTRY' >> $HOSTS_FILE"
    else
        echo "$HOST_ENTRY" >> "$HOSTS_FILE"
    fi
    echo "✅ Entrada adicionada com sucesso ao $HOSTS_FILE!"
fi

# Limpa o cache DNS local do macOS
echo "🔄 Limpando cache DNS do macOS..."
sudo dscacheutil -flushcache 2>/dev/null || true
sudo killall -HUP mDNSResponder 2>/dev/null || true

echo ""
echo "======================================================================"
echo "🎉 DOMÍNIO LOCAL CONFIGURADO COM SUCESSO!"
echo "======================================================================"
echo "📍 Você pode acessar o ecossistema das seguintes formas:"
echo "   • 🌐 http://nova.local:3000 (ou http://nova.local se rodando na porta 80)"
echo "   • 🌐 http://localhost:3000"
echo ""
echo "💡 Dica: Para iniciar o painel na porta padrão, execute: ./start-all.sh"
echo "======================================================================"
