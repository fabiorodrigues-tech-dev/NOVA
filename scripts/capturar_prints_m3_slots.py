#!/usr/bin/env python3
"""
Captura screenshots em alta resolução do NOVA Control Center renovado com Material 3 Design Kit & Slot Architecture.
"""

import subprocess
import os
import time

ARTIFACTS_DIR = "/Users/fabioandre/.gemini/antigravity-ide/brain/b8c18ce9-faac-499b-807a-835d4faa4967"
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

os.makedirs(ARTIFACTS_DIR, exist_ok=True)

telas = [
    ("dashboard_m3_slots_dark.png", "http://localhost:3000?theme=dark"),
    ("dashboard_m3_slots_light.png", "http://localhost:3000?theme=light"),
    ("voice_studio_m3_slots_dark.png", "http://localhost:3000?view=voice-studio&theme=dark"),
    ("voice_studio_m3_slots_light.png", "http://localhost:3000?view=voice-studio&theme=light")
]

print("🎨 Capturando screenshots do NOVA Control Center — Material 3 Design Kit & Slots Architecture...")

for filename, url in telas:
    out_path = os.path.join(ARTIFACTS_DIR, filename)
    cmd = [
        CHROME_BIN,
        "--headless=new",
        "--hide-scrollbars",
        "--window-size=1440,1050",
        "--virtual-time-budget=3000",
        f"--screenshot={out_path}",
        url
    ]
    try:
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        size_kb = os.path.getsize(out_path) / 1024
        print(f"   ✅ {filename}: {size_kb:.1f} KB")
    except Exception as e:
        print(f"   ❌ Erro ao capturar {filename}: {e}")

print("✨ Capturas do Material 3 Design Kit & Slots Architecture concluídas com sucesso!")
