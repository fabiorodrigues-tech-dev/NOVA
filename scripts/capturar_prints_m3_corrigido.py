#!/usr/bin/env python3
"""
Captura screenshots do Dashboard NOVA com Anatomia M3 Corrigida:
1. Modo Claro (M3 Light)
2. Modo Escuro (M3 Dark)
"""

import subprocess
import os

ARTIFACTS_DIR = "/Users/fabioandre/.gemini/antigravity-ide/brain/b8c18ce9-faac-499b-807a-835d4faa4967"
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

os.makedirs(ARTIFACTS_DIR, exist_ok=True)

telas = [
    ("dashboard_m3_anatomia_light.png", "http://localhost:3000?theme=light"),
    ("dashboard_m3_anatomia_dark.png", "http://localhost:3000?theme=dark")
]

print("🎨 Capturando screenshots do Dashboard NOVA com Anatomia M3 Corrigida...")

for filename, url in telas:
    out_path = os.path.join(ARTIFACTS_DIR, filename)
    cmd = [
        CHROME_BIN,
        "--headless=new",
        "--hide-scrollbars",
        "--window-size=1440,1100",
        "--virtual-time-budget=2500",
        f"--screenshot={out_path}",
        url
    ]
    try:
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        size_kb = os.path.getsize(out_path) / 1024
        print(f"   ✅ {filename}: {size_kb:.1f} KB")
    except Exception as e:
        print(f"   ❌ Erro ao capturar {filename}: {e}")

print("✨ Todas as capturas de anatomia M3 foram concluídas!")
