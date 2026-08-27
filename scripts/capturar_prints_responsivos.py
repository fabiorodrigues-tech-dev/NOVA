#!/usr/bin/env python3
"""
Captura screenshots do Dashboard NOVA em 3 breakpoints responsivos:
1. Desktop (1440x960)
2. Tablet (768x1024)
3. Mobile (375x812)
"""

import subprocess
import os
import time

ARTIFACTS_DIR = "/Users/fabioandre/.gemini/antigravity-ide/brain/b8c18ce9-faac-499b-807a-835d4faa4967"
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

os.makedirs(ARTIFACTS_DIR, exist_ok=True)

breakpoints = [
    ("dashboard_responsivo_desktop_1440px.png", 1440, 960, "http://localhost:3000"),
    ("dashboard_responsivo_tablet_768px.png", 768, 1024, "http://localhost:3000"),
    ("dashboard_responsivo_mobile_375px.png", 375, 812, "http://localhost:3000")
]

print("📱 Capturando screenshots nos 3 breakpoints responsivos (Desktop, Tablet, Mobile)...")

for nome_arquivo, width, height, url in breakpoints:
    output_path = os.path.join(ARTIFACTS_DIR, nome_arquivo)
    print(f"   ↳ Capturando {nome_arquivo} ({width}x{height})...")
    
    cmd = [
        CHROME_BIN,
        "--headless=new",
        "--hide-scrollbars",
        f"--window-size={width},{height}",
        "--virtual-time-budget=2500",
        f"--screenshot={output_path}",
        url
    ]
    
    try:
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        if os.path.exists(output_path):
            size_kb = os.path.getsize(output_path) / 1024
            print(f"     ✅ Gerado com sucesso: {nome_arquivo} ({size_kb:.1f} KB)")
        else:
            print(f"     ❌ Arquivo não gerado: {nome_arquivo}")
    except Exception as e:
        print(f"     ❌ Erro na captura de {nome_arquivo}: {e}")

print("✨ Todas as capturas responsivas foram concluídas!")
