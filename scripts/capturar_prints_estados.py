#!/usr/bin/env python3
"""
Captura screenshots em alta resolução do Dashboard NOVA em 3 estados:
1. Normal (Ao Vivo com dados H2, gráficos e novo logo)
2. Loading (Skeleton screens com shimmer animation)
3. Empty (Mensagens específicas e propositivas)
4. Splash / Error (Visão completa da identidade e resiliência)
"""

import subprocess
import os
import time

ARTIFACTS_DIR = "/Users/fabioandre/.gemini/antigravity-ide/brain/b8c18ce9-faac-499b-807a-835d4faa4967"
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

os.makedirs(ARTIFACTS_DIR, exist_ok=True)

estados = [
    ("dashboard_estado_normal.png", "http://localhost:3000?state=normal"),
    ("dashboard_estado_loading.png", "http://localhost:3000?state=loading"),
    ("dashboard_estado_empty.png", "http://localhost:3000?state=empty"),
    ("dashboard_estado_error.png", "http://localhost:3000?state=error")
]

print("📸 Iniciando captura de screenshots dos 3 estados do Dashboard NOVA...")

for nome_arquivo, url in estados:
    output_path = os.path.join(ARTIFACTS_DIR, nome_arquivo)
    print(f"   ↳ Capturando {nome_arquivo} ({url})...")
    
    cmd = [
        CHROME_BIN,
        "--headless=new",
        "--hide-scrollbars",
        "--window-size=1440,960",
        "--virtual-time-budget=2000",
        f"--screenshot={output_path}",
        url
    ]
    
    try:
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        if os.path.exists(output_path):
            size_kb = os.path.getsize(output_path) / 1024
            print(f"     ✅ Sucesso: {nome_arquivo} ({size_kb:.1f} KB)")
        else:
            print(f"     ❌ Arquivo não gerado: {nome_arquivo}")
    except Exception as e:
        print(f"     ❌ Erro na captura de {nome_arquivo}: {e}")

print("✨ Todas as capturas foram concluídas!")
