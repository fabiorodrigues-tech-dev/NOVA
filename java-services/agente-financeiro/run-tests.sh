#!/usr/bin/env bash
set -e

# Define o caminho do Maven se instalado no Homebrew
export PATH="/opt/homebrew/bin:$PATH"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🔨 Compilando classes principais..."
mvn compile -q

echo "📦 Gerando classpath de testes..."
mvn dependency:build-classpath -DincludeScope=test -Dmdep.outputFile=cp.txt -q

mkdir -p target/test-classes
echo "🧪 Compilando testes unitários e de integração..."
javac -cp "target/classes:$(cat cp.txt)" -d target/test-classes $(find src/test/java -name "*.java")

echo "🚀 Executando suíte de testes JUnit 5..."
java -cp "target/classes:target/test-classes:$(cat cp.txt)" com.nova.agentefinanceiro.TestExecutionMain
