#!/usr/bin/env bash
set -e

# Configura Java 21 LTS como prioridade se disponível
if [ -d "/Library/Java/JavaVirtualMachines/zulu-21.jdk/Contents/Home" ]; then
    export JAVA_HOME="/Library/Java/JavaVirtualMachines/zulu-21.jdk/Contents/Home"
    export PATH="$JAVA_HOME/bin:$PATH"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/java-services/agente-financeiro"

./run-tests.sh
