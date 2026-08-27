#!/usr/bin/env python3
"""
Captura a sequência de quadros (storyboard) da Splash Screen 3D do NOVA Control Center.
"""

import subprocess
import os
import time

ARTIFACTS_DIR = "/Users/fabioandre/.gemini/antigravity-ide/brain/b8c18ce9-faac-499b-807a-835d4faa4967"
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

os.makedirs(ARTIFACTS_DIR, exist_ok=True)

quadros = [
    ("splash_3d_frame1_convergence.png", 600, "http://localhost:3000"),
    ("splash_3d_frame2_wordmark.png", 1400, "http://localhost:3000"),
    ("splash_3d_frame3_dashboard.png", 2800, "http://localhost:3000")
]

print("🎬 Capturando sequência da Splash Screen 3D (~2.2s)...")

for filename, delay_ms, url in quadros:
    out_path = os.path.join(ARTIFACTS_DIR, filename)
    cmd = [
        CHROME_BIN,
        "--headless=new",
        "--hide-scrollbars",
        "--window-size=1440,960",
        f"--virtual-time-budget={delay_ms}",
        f"--screenshot={out_path}",
        url
    ]
    try:
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        size_kb = os.path.getsize(out_path) / 1024
        print(f"   ✅ Quadro {filename} (t={delay_ms}ms): {size_kb:.1f} KB")
    except Exception as e:
        print(f"   ❌ Erro ao capturar {filename}: {e}")

print("✨ Sequência de animação capturada com sucesso!")
