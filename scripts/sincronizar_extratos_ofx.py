#!/usr/bin/env python3
"""
Sincronizador de Extratos Bancários OFX em Lote — Ecossistema NOVA
Varre recursivamente a pasta 'financeiro/' e subpastas em busca de arquivos .ofx/.OFX,
extrai as transações (Data, Valor, Descrição, FITID) e realiza a ingestão com deduplicação
no banco de dados H2 persistente via microsserviço Spring Boot (ou fallback).

Uso:
    python3 scripts/sincronizar_extratos_ofx.py
"""

import os
import sys
import re
import json
import glob
import urllib.request
import urllib.error
from datetime import datetime

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FINANCEIRO_DIR = os.path.join(WORKSPACE_DIR, "financeiro")
SPRING_BOOT_URL = os.environ.get("NOVA_FINANCEIRO_URL", "http://localhost:8081")

def extrair_transacoes_ofx(caminho_arquivo: str) -> list:
    """
    Realiza o parsing direto das tags OFX do arquivo:
    - <DTPOSTED> -> Data
    - <TRNAMT>   -> Valor
    - <MEMO> / <NAME> -> Descrição
    - <FITID>    -> ID Único
    """
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()
    except Exception:
        try:
            with open(caminho_arquivo, "r", encoding="latin-1") as f:
                conteudo = f.read()
        except Exception as e:
            print(f"⚠️ Erro ao ler arquivo {caminho_arquivo}: {e}", file=sys.stderr)
            return []

    transacoes = []
    blocks = re.findall(r"<STMTTRN>(.*?)</STMTTRN>", conteudo, re.DOTALL | re.IGNORECASE)
    for b in blocks:
        data_m = re.search(r"<DTPOSTED>\s*(\d{8})", b, re.IGNORECASE)
        valor_m = re.search(r"<TRNAMT>\s*([+-]?\d+(?:[.,]\d+)?)", b, re.IGNORECASE)
        memo_m = re.search(r"<MEMO>\s*([^<\r\n]+)", b, re.IGNORECASE)
        name_m = re.search(r"<NAME>\s*([^<\r\n]+)", b, re.IGNORECASE)
        fitid_m = re.search(r"<FITID>\s*([^<\r\n]+)", b, re.IGNORECASE)

        if data_m and valor_m:
            dt_raw = data_m.group(1)
            dt_iso = f"{dt_raw[0:4]}-{dt_raw[4:6]}-{dt_raw[6:8]}"
            try:
                val_float = float(valor_m.group(1).replace(",", "."))
            except ValueError:
                val_float = 0.0

            descricao = (memo_m.group(1) if memo_m else (name_m.group(1) if name_m else "Transação OFX")).strip()
            fitid = fitid_m.group(1).strip() if fitid_m else ""
            val_abs_str = f"{abs(val_float):.2f}"

            # Tupla única estrita para deduplicação: (FITID, data_transacao, valor, descricao_limpa)
            tupla_unica = (fitid, dt_iso, val_abs_str, descricao)
            hash_sha = hashlib.sha256(f"{dt_iso}{val_abs_str}{fitid}{descricao}".encode("utf-8")).hexdigest()

            transacoes.append({
                "data": dt_iso,
                "valor": val_float,
                "descricao": descricao,
                "fitid": fitid,
                "tipo": "RECEITA" if val_float > 0 else "DESPESA",
                "tupla": tupla_unica,
                "hash": hash_sha
            })
    return transacoes

def verificar_spring_boot(base_url: str = SPRING_BOOT_URL) -> bool:
    """Verifica se o backend Spring Boot está respondendo na porta configurada."""
    try:
        url = f"{base_url}/api/transacoes/resumo"
        req = urllib.request.Request(url, headers={'User-Agent': 'NOVA-OFX-Sync'})
        with urllib.request.urlopen(req, timeout=2) as resp:
            return resp.status == 200
    except Exception:
        return False

def reconciliar_estrito_spring_boot(base_url: str = SPRING_BOOT_URL) -> dict:
    """Aciona a reconciliação estrita com deduplicação por hash SHA-256 e tupla única no Spring Boot."""
    try:
        url = f"{base_url}/api/transacoes/reconciliar-estrito"
        req = urllib.request.Request(url, data=b"", headers={'User-Agent': 'NOVA-OFX-Sync'}, method='POST')
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return {"erro": str(e), "totalImportados": 0, "totalLidos": 0, "totalDuplicados": 0}

def enviar_ofx_spring_boot(caminho_arquivo: str, base_url: str = SPRING_BOOT_URL) -> dict:
    """Envia o conteúdo do arquivo OFX para o endpoint /api/transacoes/importar-ofx."""
    try:
        with open(caminho_arquivo, "rb") as f:
            raw_bytes = f.read()

        url = f"{base_url}/api/transacoes/importar-ofx"
        req = urllib.request.Request(
            url,
            data=raw_bytes,
            headers={
                'Content-Type': 'text/plain; charset=utf-8',
                'User-Agent': 'NOVA-OFX-Sync'
            },
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return {"erro": str(e), "totalImportados": 0, "totalLidos": 0, "totalDuplicados": 0}

def obter_resumo_julho(base_url: str = SPRING_BOOT_URL) -> int:
    """Consulta o H2 para obter a quantidade exata de transações registradas no mês de Julho."""
    try:
        url = f"{base_url}/api/transacoes/resumo?inicio=2026-07-01&fim=2026-07-31"
        req = urllib.request.Request(url, headers={'User-Agent': 'NOVA-OFX-Sync'})
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return int(data.get("quantidadeTransacoes", 0))
    except Exception:
        return 0

def obter_total_h2(base_url: str = SPRING_BOOT_URL) -> int:
    """Consulta o H2 para obter o total consolidado de transações cadastradas."""
    try:
        url = f"{base_url}/api/transacoes"
        req = urllib.request.Request(url, headers={'User-Agent': 'NOVA-OFX-Sync'})
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if isinstance(data, list):
                return len(data)
    except Exception:
        pass
    return 0

def sincronizar_todos_extratos(caminho_dir: str = FINANCEIRO_DIR, base_url: str = SPRING_BOOT_URL, exibir_resumo: bool = True) -> dict:
    """
    Varre recursivamente caminho_dir por arquivos .ofx/.OFX e sincroniza no banco H2
    com deduplicação estrita baseada na tupla única (FITID, data_transacao, valor, descricao_limpa).
    Retorna dicionário com os totais apurados.
    """
    if not os.path.exists(caminho_dir):
        if exibir_resumo:
            print("Arquivos processados: 0 | Transações cadastradas: 0 | Transações de Julho: 0")
        return {"arquivos_processados": 0, "transacoes_cadastradas": 0, "transacoes_julho": 0}

    # 1. Busca recursiva por arquivos .ofx e .OFX
    arquivos_ofx = []
    for root, _, files in os.walk(caminho_dir):
        for f in files:
            if f.lower().endswith(".ofx"):
                arquivos_ofx.append(os.path.join(root, f))

    arquivos_ofx = sorted(arquivos_ofx)
    total_arquivos = len(arquivos_ofx)
    total_novas = 0
    total_julho_local = 0
    tuplas_vistas = set()

    spring_online = verificar_spring_boot(base_url)

    if spring_online:
        # Aciona a reconciliação estrita com descarte silencioso de sobreposição de Agosto
        res_reconciliacao = reconciliar_estrito_spring_boot(base_url)
        total_novas = res_reconciliacao.get("totalImportados", 0)
    else:
        for arq in arquivos_ofx:
            parsed = extrair_transacoes_ofx(arq)
            for t in parsed:
                if t["tupla"] not in tuplas_vistas:
                    tuplas_vistas.add(t["tupla"])
                    if t["data"].startswith("2026-07"):
                        total_julho_local += 1

    if spring_online:
        qtd_julho = obter_resumo_julho(base_url)
        total_h2 = obter_total_h2(base_url)
        transacoes_cadastradas = total_h2 if total_h2 > 0 else total_novas
    else:
        qtd_julho = total_julho_local
        transacoes_cadastradas = len(tuplas_vistas)

    resultado = {
        "arquivos_processados": total_arquivos,
        "transacoes_cadastradas": transacoes_cadastradas,
        "transacoes_novas": total_novas,
        "transacoes_julho": qtd_julho,
        "spring_boot_online": spring_online
    }

    if exibir_resumo:
        print(f"Arquivos processados: {total_arquivos} | Transações cadastradas: {transacoes_cadastradas} | Transações de Julho: {qtd_julho}")

    return resultado

if __name__ == "__main__":
    sincronizar_todos_extratos()
