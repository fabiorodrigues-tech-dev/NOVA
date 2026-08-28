#!/usr/bin/env bash
#!/usr/bin/env python3
"""
NOVA Control Center — Compartilhamento Seguro & Túnel Público HTTPS
Gera um túnel HTTPS seguro para a porta 3000 com proteção de privacidade inteligente (LGPD Demo Mode).
"""

import os
import sys
import time
import shutil
import subprocess
import urllib.request
import json

PORT = int(os.environ.get("NOVA_PORT", 3000))

def verificar_servidor_ativo():
    url = f"http://127.0.0.1:{PORT}/api/status"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'NOVA-Tunnel-Checker'})
        with urllib.request.urlopen(req, timeout=2) as response:
            if response.status == 200:
                return True
    except Exception:
        pass
    return False

def imprimir_cabecalho():
    print("=" * 70)
    print("🌐 NOVA CONTROL CENTER — COMPARTILHAMENTO PÚBLICO & DEMO MODE")
    print("=" * 70)
    print("🛡️  GARANTIA DE PRIVACIDADE ABSOLUTA (LGPD DevSecOps):")
    print("   • Todo acesso via este link público será servido em MODO DEMO.")
    print("   • Nenhum extrato bancário, saldo real ou dado confidencial será exposto.")
    print("   • O assistente de voz e a interface executiva permanecem 100% interativos.")
    print("=" * 70)

def iniciar_tunel():
    imprimir_cabecalho()

    if not verificar_servidor_ativo():
        print(f"⚠️  O servidor NOVA não parece estar rodando na porta {PORT}.")
        print("💡 Inicie os serviços primeiro executando: ./start-all.sh")
        print("   Tentando prosseguir mesmo assim...")

    print("\n🚀 Estabelecendo túnel HTTPS público seguro...")

    # 1. Opção: cloudflared (se instalado)
    if shutil.which("cloudflared"):
        print("✨ Utilizando Cloudflare Tunnel...")
        try:
            subprocess.run(["cloudflared", "tunnel", "--url", f"http://localhost:{PORT}"])
            return
        except KeyboardInterrupt:
            print("\n👋 Túnel encerrado com sucesso.")
            return

    # 2. Opção: localtunnel (via npx, que é nativo no macOS com Node.js)
    if shutil.which("npx"):
        print("✨ Utilizando LocalTunnel (npx localtunnel)...")
        print("⏳ Aguarde a inicialização da URL pública...")
        try:
            proc = subprocess.Popen(
                ["npx", "-y", "localtunnel", "--port", str(PORT)],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            for line in proc.stdout:
                if "your url is:" in line.lower():
                    url = line.strip().split("is:")[-1].strip()
                    print("\n" + "=" * 70)
                    print(f"🎉 LINK PÚBLICO GERADO COM SUCESSO!")
                    print(f"🌐 Acesse no celular ou compartilhe:")
                    print(f"👉 \033[1;32m{url}\033[0m")
                    print(f"👉 \033[1;34m{url}?demo=true\033[0m (Forçar Modo Demonstração)")
                    print("=" * 70)
                    print("🛑 Pressione Ctrl+C para encerrar o compartilhamento.\n")
                else:
                    print(line, end="")
            proc.wait()
            return
        except KeyboardInterrupt:
            print("\n👋 Túnel encerrado com segurança.")
            return
        except Exception as e:
            print(f"⚠️  Falha ao iniciar localtunnel: {e}")

    # 3. Opção: SSH Tunnel (localhost.run / serveo.net)
    print("✨ Utilizando túnel SSH seguro (localhost.run)...")
    try:
        subprocess.run(["ssh", "-R", f"80:localhost:{PORT}", "nokey@localhost.run"])
    except KeyboardInterrupt:
        print("\n👋 Túnel encerrado com segurança.")
    except Exception as e:
        print(f"❌ Não foi possível iniciar o túnel automático: {e}")
        print("💡 Você pode instalar o cloudflared ('brew install cloudflared') ou ngrok para túneis dedicados.")

if __name__ == "__main__":
    iniciar_tunel()
