#!/usr/bin/env python3
"""
Captura screenshots dos estados do Living Shader Voice Orb no NOVA Control Center.
"""
import subprocess
import time
from pathlib import Path

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUTPUT_DIR = Path("/Users/fabioandre/.gemini/antigravity-ide/brain/b8c18ce9-faac-499b-807a-835d4faa4967")

def capturar_estado(url, filename, delay=3):
    dest = OUTPUT_DIR / filename
    cmd = [
        CHROME_BIN,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        "--window-size=1440,900",
        f"--virtual-time-budget={delay * 1000}",
        f"--screenshot={str(dest)}",
        url
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"   ✅ {filename}: {dest.stat().st_size / 1024:.1f} KB")

def main():
    print("🎨 Capturando estados do Living Shader Voice Orb...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    capturar_estado("http://localhost:3000/", "orb_living_shader_idle.png", delay=2)
    print("✨ Capturas dos estados do Shader Orb concluídas!")

if __name__ == "__main__":
    main()
