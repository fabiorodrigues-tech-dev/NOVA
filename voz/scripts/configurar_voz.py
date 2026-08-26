#!/usr/bin/env python3
"""
Menu Interativo de Configuração de Vozes Neurais — Ecossistema NOVA
Gerenciamento, teste sonoro e personalização das vozes do NOVA.
"""

import os
import sys
import json
import asyncio
import tempfile
import subprocess
import argparse

try:
    import edge_tts
except ImportError:
    print("❌ Erro: 'edge-tts' não encontrado. Execute: pip3 install edge-tts")
    sys.exit(1)

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config_voz.json"))

VOZES_CATALOGO = [
    {"chave": "antonio", "id": "pt-BR-AntonioNeural", "nome": "Antônio", "genero": "Masculino", "perfil": "Natural / Executiva (Padrão)"},
    {"chave": "francisca", "id": "pt-BR-FranciscaNeural", "nome": "Francisca", "genero": "Feminina", "perfil": "Fluida / Humanizada"},
    {"chave": "fabio", "id": "pt-BR-FabioNeural", "nome": "Fábio", "genero": "Masculino", "perfil": "Tom Direto / Ágil"},
    {"chave": "thalita", "id": "pt-BR-ThalitaNeural", "nome": "Thalita", "genero": "Feminina", "perfil": "Expressiva / Dinâmica"}
]

def carregar_config() -> dict:
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"voz_padrao": "pt-BR-AntonioNeural", "velocidade": "+0%", "tom": "+0Hz"}

def salvar_config(config: dict):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"✅ Configurações salvas com sucesso em: {CONFIG_PATH}")

async def demonstrar_voz_async(voz_id: str, taxa: str = "+0%"):
    texto = "Olá, Fábio! Esta é uma demonstração da minha voz neural humana no ecossistema NOVA. Como posso te ajudar hoje?"
    print(f"🔊 Reproduzindo amostra com a voz '{voz_id}'...")

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_mp3:
        temp_path = temp_mp3.name

    try:
        comunicador = edge_tts.Communicate(text=texto, voice=voz_id, rate=taxa)
        await comunicador.save(temp_path)
        subprocess.run(["afplay", temp_path], check=True)
    except Exception as e:
        print(f"⚠️ Erro ao reproduzir amostra: {e}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

def demonstrar_voz(voz_id: str, taxa: str = "+0%"):
    asyncio.run(demonstrar_voz_async(voz_id, taxa))

def exibir_menu():
    config = carregar_config()
    voz_atual = config.get("voz_padrao", "pt-BR-AntonioNeural")
    taxa_atual = config.get("velocidade", "+0%")

    while True:
        print("\n" + "=" * 65)
        print("🎙️ MENU DE CONFIGURAÇÃO DE VOZES NEURAIS — ECOSSISTEMA NOVA")
        print(f"📌 Voz Atual: [{voz_atual}] | Velocidade: [{taxa_atual}]")
        print("=" * 65)
        print("Opções de Vozes Disponíveis:")
        for idx, item in enumerate(VOZES_CATALOGO, start=1):
            marcador = " (ATIVADA)" if item["id"] == voz_atual else ""
            print(f"  [{idx}] {item['nome']} ({item['genero']}) — {item['perfil']}{marcador}")
            print(f"      ID: {item['id']}")

        print("\nComandos:")
        print("  [D] Demonstrar em áudio todas as vozes sequencialmente")
        print("  [V] Ajustar Velocidade da fala (+10%, -10%, +0%)")
        print("  [S] Sair")
        print("=" * 65)

        escolha = input("👉 Digite o número da voz para testar/ativar ou uma opção: ").strip().lower()

        if escolha == 's':
            print("👋 Configuração finalizada.")
            break
        elif escolha == 'd':
            for v in VOZES_CATALOGO:
                print(f"\n▶️ Testando {v['nome']}...")
                demonstrar_voz(v["id"], taxa_atual)
        elif escolha == 'v':
            nova_taxa = input("Digite o ajuste de velocidade (ex: +10%, -5%, +0%): ").strip()
            if nova_taxa:
                taxa_atual = nova_taxa
                config["velocidade"] = taxa_atual
                salvar_config(config)
                print(f"✅ Velocidade definida para: {taxa_atual}")
        elif escolha in ["1", "2", "3", "4"]:
            v_selecionada = VOZES_CATALOGO[int(escolha) - 1]
            print(f"\n🎯 Selecionado: {v_selecionada['nome']} ({v_selecionada['id']})")
            
            # Pergunta se deseja ouvir antes de salvar
            ouvir = input("Deseja ouvir uma amostra? (S/n): ").strip().lower()
            if ouvir != 'n':
                demonstrar_voz(v_selecionada["id"], taxa_atual)

            salvar = input(f"Definir '{v_selecionada['nome']}' como a voz padrão do NOVA? (S/n): ").strip().lower()
            if salvar != 'n':
                voz_atual = v_selecionada["id"]
                config["voz_padrao"] = voz_atual
                config["descricao"] = v_selecionada["perfil"]
                salvar_config(config)
                print(f"🎉 Voz padrão alterada para: {v_selecionada['nome']} ({voz_atual})")
        else:
            print("⚠️ Opção inválida. Tente novamente.")

def configurar_via_cli(nome_ou_chave: str, taxa: str = None, testar: bool = False):
    config = carregar_config()
    chave_busca = nome_ou_chave.lower().replace("pt-br-", "").replace("neural", "")
    
    voz_encontrada = None
    for item in VOZES_CATALOGO:
        if chave_busca in item["chave"] or chave_busca in item["nome"].lower() or item["id"].lower() == nome_ou_chave.lower():
            voz_encontrada = item
            break

    if not voz_encontrada:
        print(f"❌ Voz '{nome_ou_chave}' não encontrada. Escolha entre: antonio, francisca, fabio, thalita.")
        return

    if taxa:
        config["velocidade"] = taxa

    if testar:
        demonstrar_voz(voz_encontrada["id"], config.get("velocidade", "+0%"))

    config["voz_padrao"] = voz_encontrada["id"]
    config["descricao"] = voz_encontrada["perfil"]
    salvar_config(config)
    print(f"🎉 Voz do NOVA atualizada para: {voz_encontrada['nome']} ({voz_encontrada['id']})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Configurador de Vozes Neurais NOVA")
    parser.add_argument("--set-voz", help="Nome ou alias da voz para ativar (antonio, francisca, fabio, thalita)")
    parser.add_argument("--taxa", help="Velocidade da voz (ex: +10%, -5%)")
    parser.add_argument("--testar", help="Testa o áudio da voz informada")
    parser.add_argument("--listar", action="store_true", help="Lista as vozes disponíveis em formato tabular")

    args = parser.parse_args()

    if args.listar:
        config = carregar_config()
        print("\n📋 VOZES NEURAIS DISPONÍVEIS NO NOVA:")
        for v in VOZES_CATALOGO:
            ativo = " ⭐ (PADRÃO ATUAL)" if v["id"] == config.get("voz_padrao") else ""
            print(f"- {v['nome']} ({v['genero']}) -> ID: `{v['id']}` | Perfil: {v['perfil']}{ativo}")
        print()
    elif args.testar:
        demonstrar_voz(args.testar, args.taxa or "+0%")
    elif args.set-voz:
        configurar_via_cli(args.set_voz, args.taxa, testar=True)
    else:
        exibir_menu()
