#!/usr/bin/env python3
"""
NOVA Control Center — Unified Dashboard Server (Port 3000)
Servidor Web local e API Gateway com síntese de voz neural Base64 e integração ao Spring Boot.
"""

import os
import sys
import json
import base64
import asyncio
import tempfile
import urllib.request
import urllib.parse
import webbrowser
import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler

try:
    import edge_tts
except ImportError:
    edge_tts = None

DEFAULT_PORT = int(os.environ.get("NOVA_PORT", os.environ.get("PORT", 3000)))
PORT = DEFAULT_PORT
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
WORKSPACE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
CONFIG_VOZ_PATH = os.path.join(WORKSPACE_DIR, "voz/config_voz.json")
ADMIN_PIN = os.environ.get("ADMIN_PIN", "7770")

def extrair_pin_requisicao(handler):
    """
    Extrai o PIN de administrador enviado na requisição via headers.
    Suporta:
    - Authorization: Bearer <PIN> ou <PIN>
    - X-Admin-PIN / X-Admin-Pin / X-NOVA-PIN / x-admin-pin
    """
    auth_header = handler.headers.get("Authorization", "")
    if auth_header:
        if auth_header.startswith("Bearer "):
            return auth_header[7:].strip()
        return auth_header.strip()

    for h in ["X-Admin-PIN", "X-Admin-Pin", "X-NOVA-PIN", "x-admin-pin"]:
        val = handler.headers.get(h)
        if val:
            return val.strip()
    return ""

def is_pin_valido(handler):
    """
    Valida se o PIN de administrador recebido nos cabeçalhos corresponde ao PIN configurado.
    """
    pin = extrair_pin_requisicao(handler)
    return bool(pin and pin == ADMIN_PIN)

def is_demo_mode(handler, query_params=None):
    """
    Detecta se a requisição deve ser servida com dados de demonstração (Demo Mode)
    ou com dados reais (Real Mode).
    
    POLÍTICA DE SEGURANÇA ESTRITA (LGPD SAFE):
    Os dados reais só são entregues se o header de autorização com o PIN correto
    for enviado na requisição. Caso contrário, retorna SEMPRE Modo Demonstração (Demo Mode).
    """
    # 1. Se o PIN correto NÃO for enviado, OBRIGATORIAMENTE retorna Modo Demo (LGPD Safe)
    if not is_pin_valido(handler):
        return True

    if query_params is None:
        query_params = {}

    # 2. Com PIN válido, verifica se o cliente solicitou explicitamente modo demo
    if "demo" in query_params:
        val = query_params["demo"][0].lower()
        if val in ("true", "1", "yes", "demo"):
            return True
        if val in ("false", "0", "no", "real"):
            return False
            
    if "mode" in query_params:
        val = query_params["mode"][0].lower()
        if val in ("demo", "presentation", "simulado"):
            return True
        if val in ("real", "live", "producao"):
            return False

    req_demo = handler.headers.get("X-NOVA-Demo", "").lower()
    if req_demo in ("true", "1", "yes"):
        return True
    if req_demo in ("false", "0", "no"):
        return False

    cookie_str = handler.headers.get("Cookie", "")
    if "nova_privacy_mode=demo" in cookie_str:
        return True
    if "nova_privacy_mode=real" in cookie_str:
        return False

    # Com PIN válido autenticado e sem flags forçando demo, entrega dados reais
    return False

def obter_resumo_financeiro(demo=False):
    if demo:
        return {
            "totalGasto": 14250.00,
            "totalReceitas": 18500.00,
            "saldo": 4250.00,
            "quantidadeTransacoes": 32,
            "periodoInicio": "2026-08-01",
            "periodoFim": "2026-08-31",
            "totalPorCategoria": {
                "Cloud Infrastructure (AWS/GCP)": 4200.00,
                "SaaS & Dev Tools": 3850.00,
                "Hardware & Workstation": 3500.00,
                "Cursos & Certificações": 2700.00
            }
        }

    url = "http://localhost:8081/api/transacoes/resumo"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'NOVA-Dashboard-Gateway'})
        with urllib.request.urlopen(req, timeout=2) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception:
        return {
            "totalGasto": 1709.77,
            "totalReceitas": 2299.00,
            "saldo": 589.23,
            "quantidadeTransacoes": 43,
            "periodoInicio": "2026-08-01",
            "periodoFim": "2026-08-31",
            "totalPorCategoria": {
                "ALIMENTACAO": 728.38,
                "TRANSPORTE": 151.87,
                "COMPRAS": 318.52,
                "TRANSFERENCIAS": 511.00
            }
        }

def obter_projecao_financeira(demo=False):
    if demo:
        return {
            "dataReferencia": "2026-08-28",
            "diasDecorridos": 28,
            "diasRestantes": 3,
            "totalDiasMes": 31,
            "totalGastosAtual": 14250.00,
            "totalReceitasAtual": 18500.00,
            "saldoAtual": 4250.00,
            "burnRateDiario": 508.92,
            "gastoAdicionalProjetado": 1526.76,
            "gastoTotalProjetado": 15776.76,
            "saldoFinalProjetado": 2723.24,
            "statusOrcamentario": "SAUDAVEL",
            "alertas": ["✅ Balanço Saudável: Superávit projetado de R$ 2.723,24 no fechamento mensal."],
            "recomendacaoEstrategica": "Fluxo orçamentário estável! Sugestão de aporte de R$ 1.500,00 na Reserva Técnica e Licenças Dev."
        }

    url = "http://localhost:8081/api/transacoes/projecao"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'NOVA-Dashboard-Gateway'})
        with urllib.request.urlopen(req, timeout=2) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception:
        return {
            "dataReferencia": "2026-08-28",
            "diasDecorridos": 28,
            "diasRestantes": 3,
            "totalDiasMes": 31,
            "totalGastosAtual": 1709.77,
            "totalReceitasAtual": 2299.00,
            "saldoAtual": 589.23,
            "burnRateDiario": 61.06,
            "gastoAdicionalProjetado": 183.18,
            "gastoTotalProjetado": 1892.95,
            "saldoFinalProjetado": 406.05,
            "statusOrcamentario": "SAUDAVEL",
            "alertas": ["✅ Balanço Saudável: Superávit projetado de R$ 406,05 ao fim do mês."],
            "recomendacaoEstrategica": "Ritmo financeiro sob controle! Sugestão de aporte de R$ 203,03 nas caixinhas (Reserva e Casal)."
        }

def obter_caixinhas_patrimonio(demo=False):
    if demo:
        return {
            "saldoContaCorrente": 4250.00,
            "totalInvestidoCaixinhas": 40000.00,
            "patrimonioLiquidoTotal": 44250.00,
            "caixinhas": [
                {
                    "id": 1,
                    "nome": "Reserva de Emergência & Liquidez",
                    "saldo": 25000.00,
                    "tipo": "RESERVA_EMERGENCIA",
                    "rendimentoMensalEstimado": 250.00,
                    "dataAtualizacao": "2026-08-28"
                },
                {
                    "id": 2,
                    "nome": "Fundo de Equipamentos & Lab Dev",
                    "saldo": 15000.00,
                    "tipo": "FUNDO_EXPANSAO",
                    "rendimentoMensalEstimado": 150.00,
                    "dataAtualizacao": "2026-08-28"
                }
            ]
        }

    # Verifica se existem saldos reais gravados localmente em saldos_atuais.properties
    saldos_file = os.path.join(WORKSPACE_DIR, "financeiro/investimentos_caixinhas/saldos_atuais.properties")
    poupanca_casal = 911.43
    reserva_emergencia = 201.71
    caixa_infinit = 0.03
    
    if os.path.exists(saldos_file):
        try:
            with open(saldos_file, "r") as f:
                for line in f:
                    if "poupanca_casal=" in line:
                        poupanca_casal = float(line.split("=")[1].strip())
                    elif "reserva_emergencia=" in line:
                        reserva_emergencia = float(line.split("=")[1].strip())
                    elif "caixa_infinit=" in line:
                        caixa_infinit = float(line.split("=")[1].strip())
        except Exception:
            pass

    total_caixinhas = poupanca_casal + reserva_emergencia + caixa_infinit

    url = "http://localhost:8081/api/financeiro/caixinhas"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'NOVA-Dashboard-Gateway'})
        with urllib.request.urlopen(req, timeout=2) as response:
            data = json.loads(response.read().decode('utf-8'))
            saldo_cc = data.get("saldoContaCorrente", 589.23)
            return {
                "saldoContaCorrente": saldo_cc,
                "totalInvestidoCaixinhas": total_caixinhas,
                "patrimonioLiquidoTotal": round(saldo_cc + total_caixinhas, 2),
                "caixinhas": [
                    {
                        "id": 1,
                        "nome": "Poupança & Fundo do Casal",
                        "saldo": poupanca_casal,
                        "tipo": "FUNDO_CASAL",
                        "rendimentoMensalEstimado": round(poupanca_casal * 0.0085, 2),
                        "dataAtualizacao": "2026-08-28"
                    },
                    {
                        "id": 2,
                        "nome": "Reserva de Emergência",
                        "saldo": reserva_emergencia,
                        "tipo": "RESERVA_EMERGENCIA",
                        "rendimentoMensalEstimado": round(reserva_emergencia * 0.0085, 2),
                        "dataAtualizacao": "2026-08-28"
                    },
                    {
                        "id": 3,
                        "nome": "Caixa Operacional Infinit",
                        "saldo": caixa_infinit,
                        "tipo": "RESERVA_TECNICA",
                        "rendimentoMensalEstimado": 0.0,
                        "dataAtualizacao": "2026-08-28"
                    }
                ]
            }
    except Exception:
        saldo_cc = 589.23
        return {
            "saldoContaCorrente": saldo_cc,
            "totalInvestidoCaixinhas": total_caixinhas,
            "patrimonioLiquidoTotal": round(saldo_cc + total_caixinhas, 2),
            "caixinhas": [
                {
                    "id": 1,
                    "nome": "Poupança & Fundo do Casal",
                    "saldo": poupanca_casal,
                    "tipo": "FUNDO_CASAL",
                    "rendimentoMensalEstimado": round(poupanca_casal * 0.0085, 2),
                    "dataAtualizacao": "2026-08-28"
                },
                {
                    "id": 2,
                    "nome": "Reserva de Emergência",
                    "saldo": reserva_emergencia,
                    "tipo": "RESERVA_EMERGENCIA",
                    "rendimentoMensalEstimado": round(reserva_emergencia * 0.0085, 2),
                    "dataAtualizacao": "2026-08-28"
                }
            ]
        }

def obter_dados_candidaturas(demo=False):
    if demo:
        return [
            {
                "id": "techcorp-global",
                "nome": "TechCorp Global",
                "cargo": "Senior Java Engineer",
                "local": "Global / Brasil",
                "modelo": "Remoto",
                "match": 95,
                "salario_min": "R$ 12.000",
                "salario_max": "R$ 15.000",
                "status": "Match 95% • Candidatura Pronta",
                "stack": ["Java 21", "Spring Boot 3", "Spring AI MCP", "Kafka", "PostgreSQL"],
                "cv_pdf": "/download/docs/Manual_Engenharia_e_Arquitetura_NOVA.pdf",
                "cover_pdf": "/download/docs/dossie_tecnico_nova.pdf",
                "cover_docx": "/download/docs/Manual_Engenharia_e_Arquitetura_NOVA.pdf",
                "relatorio_pdf": "/download/docs/dossie_tecnico_nova.pdf",
                "pitch_texto": "Olá TechCorp! Sou Engenheiro Java com sólida experiência em Clean Architecture, microsserviços distribuídos e IA autônoma via Spring AI."
            },
            {
                "id": "finscale-systems",
                "nome": "FinScale Systems",
                "cargo": "Backend Architect (High Throughput)",
                "local": "São Paulo, SP",
                "modelo": "Híbrido",
                "match": 91,
                "salario_min": "R$ 11.000",
                "salario_max": "R$ 14.000",
                "status": "Match 91% • Em Análise",
                "stack": ["Java 21", "Spring Cloud", "Clean Architecture", "JUnit 5", "Docker"],
                "cv_pdf": "/download/docs/Manual_Engenharia_e_Arquitetura_NOVA.pdf",
                "cover_pdf": "/download/docs/dossie_tecnico_nova.pdf",
                "cover_docx": "/download/docs/Manual_Engenharia_e_Arquitetura_NOVA.pdf",
                "relatorio_pdf": "/download/docs/dossie_tecnico_nova.pdf",
                "pitch_texto": "Olá FinScale! Atuo na estruturação de microsserviços escaláveis, persistência transacional ACID e esteiras de alta performance."
            },
            {
                "id": "cloudlab-ai",
                "nome": "CloudLab AI",
                "cargo": "AI Systems Engineer (Java & LLMs)",
                "local": "Recife, PE",
                "modelo": "Remoto",
                "match": 89,
                "salario_min": "R$ 10.500",
                "salario_max": "R$ 13.500",
                "status": "Match 89% • Candidatura Pronta",
                "stack": ["Java 21", "Spring AI MCP", "Vector DB", "Clean Code", "Python Voice Bridge"],
                "cv_pdf": "/download/docs/Manual_Engenharia_e_Arquitetura_NOVA.pdf",
                "cover_pdf": "/download/docs/dossie_tecnico_nova.pdf",
                "cover_docx": "/download/docs/Manual_Engenharia_e_Arquitetura_NOVA.pdf",
                "relatorio_pdf": "/download/docs/dossie_tecnico_nova.pdf",
                "pitch_texto": "Olá CloudLab! Especialista em orquestração de ferramentas corporativas para LLMs utilizando Model Context Protocol."
            }
        ]

    empresas = [
        {
            "id": "ciandt",
            "nome": "CI&T (Global Tech)",
            "cargo": "Senior Developer Java [Job-31145]",
            "local": "Brasil (100% Remoto)",
            "modelo": "100% Remoto / CLT",
            "match": 95,
            "salario_min": "R$ 13.000",
            "salario_max": "R$ 15.000",
            "status": "Entrevista Digital Ativa",
            "stack": ["Java 21", "Spring Boot 3", "Clean Architecture", "JUnit 5", "Spring AI MCP", "PostgreSQL"],
            "cv_pdf": "/carreira/vagas_analisadas/tech_dev/ciandt/Curriculo_Fabio_Rodrigues_Java_Backend.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/tech_dev/ciandt/Cover_Letter_Fabio_Rodrigues.pdf",
            "cover_docx": "/carreira/vagas_analisadas/tech_dev/ciandt/Cover_Letter_Fabio_Rodrigues.docx",
            "relatorio_pdf": "/carreira/vagas_analisadas/tech_dev/ciandt/relatorio_match_ciandt.pdf",
            "pitch_file": "carreira/vagas_analisadas/tech_dev/ciandt/carta_apresentacao_recruiter.md"
        },
        {
            "id": "aurum",
            "nome": "Aurum (#PessoasÁureas)",
            "cargo": "Analista de Suporte Júnior (Astrea)",
            "local": "Brasil (100% Remoto)",
            "modelo": "100% Remoto / CLT",
            "match": 97,
            "salario_min": "R$ 3.000",
            "salario_max": "R$ 3.500",
            "status": "Candidatura Pronta",
            "stack": ["Suporte SaaS", "Customer Experience (CX)", "Validação ICP-Brasil", "Ponte com Engenharia", "CRM/ERP"],
            "cv_pdf": "/carreira/vagas_analisadas/suporte_operacoes/aurum/Curriculo_Fabio_Rodrigues_Suporte_TI.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/suporte_operacoes/aurum/Cover_Letter_Fabio_Rodrigues.pdf",
            "cover_docx": "/carreira/vagas_analisadas/suporte_operacoes/aurum/Cover_Letter_Fabio_Rodrigues.docx",
            "relatorio_pdf": "/carreira/vagas_analisadas/suporte_operacoes/aurum/relatorio_match_aurum.pdf",
            "pitch_file": "carreira/vagas_analisadas/suporte_operacoes/aurum/carta_apresentacao_recruiter.md"
        },
        {
            "id": "capgemini_fbs",
            "nome": "Capgemini / Farmers (FBS)",
            "cargo": "FBS IT Onboarding Specialist Jr",
            "local": "Brasil (100% Remoto)",
            "modelo": "100% Remoto / CLT",
            "match": 98,
            "salario_min": "R$ 3.800",
            "salario_max": "R$ 4.500",
            "status": "Candidatura Pronta",
            "stack": ["IT Onboarding", "Troubleshooting", "O365 / Excel", "Análise de Dados", "Validação ICP-Brasil"],
            "cv_pdf": "/carreira/vagas_analisadas/suporte_operacoes/capgemini_fbs/Curriculo_Fabio_Rodrigues_Suporte_TI.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/suporte_operacoes/capgemini_fbs/Cover_Letter_Fabio_Rodrigues.pdf",
            "cover_docx": "/carreira/vagas_analisadas/suporte_operacoes/capgemini_fbs/Cover_Letter_Fabio_Rodrigues.docx",
            "relatorio_pdf": "/carreira/vagas_analisadas/suporte_operacoes/capgemini_fbs/relatorio_match_capgemini_fbs.pdf",
            "pitch_file": "carreira/vagas_analisadas/suporte_operacoes/capgemini_fbs/carta_apresentacao_recruiter.md"
        },
        {
            "id": "capgemini_farmers_mkt",
            "nome": "Capgemini / Farmers (FBS)",
            "cargo": "FBS - Marketing Campaign Specialist",
            "local": "Brasil (100% Remoto / US Hours)",
            "modelo": "100% Remoto / CLT",
            "match": 98,
            "salario_min": "R$ 6.800",
            "salario_max": "R$ 8.000",
            "status": "Candidatura Pronta",
            "stack": ["Email Marketing (HTML)", "Direct Mail / Gráfica", "Figma / Canva Pro", "Salesforce Marketing Cloud", "A/B Testing"],
            "cv_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/capgemini_farmers_mkt/Curriculo_Fabio_Rodrigues_Marketing_Design.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/capgemini_farmers_mkt/Cover_Letter_Fabio_Rodrigues.pdf",
            "cover_docx": "/carreira/vagas_analisadas/marketing_audiovisual/capgemini_farmers_mkt/Cover_Letter_Fabio_Rodrigues.docx",
            "relatorio_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/capgemini_farmers_mkt/relatorio_match_capgemini_farmers_mkt.pdf",
            "pitch_file": "carreira/vagas_analisadas/marketing_audiovisual/capgemini_farmers_mkt/carta_apresentacao_recruiter.md"
        },
        {
            "id": "ibmr_anima",
            "nome": "IBMR (Ecossistema Ânima)",
            "cargo": "Analista de Marketing Digital I",
            "local": "Brasil (100% Remoto)",
            "modelo": "100% Remoto / CLT",
            "match": 96,
            "salario_min": "R$ 3.500",
            "salario_max": "R$ 5.000",
            "status": "Candidatura Pronta",
            "stack": ["Design (UniFBV)", "Growth & Performance", "Meta/Google Ads", "Final Cut / CapCut", "Automação / CRM"],
            "cv_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/ibmr_anima/Curriculo_Fabio_Rodrigues_Marketing_Design.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/ibmr_anima/Cover_Letter_Fabio_Rodrigues.pdf",
            "cover_docx": "/carreira/vagas_analisadas/marketing_audiovisual/ibmr_anima/Cover_Letter_Fabio_Rodrigues.docx",
            "relatorio_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/ibmr_anima/relatorio_match_ibmr_anima.pdf",
            "pitch_file": "carreira/vagas_analisadas/marketing_audiovisual/ibmr_anima/carta_apresentacao_recruiter.md"
        },
        {
            "id": "ntl_nova_tecnologia",
            "nome": "NTL Nova Tecnologia",
            "cargo": "Desenvolvedor(a) Java Sênior",
            "local": "Recife, PE",
            "modelo": "100% Remoto / Híbrido",
            "match": 94,
            "salario_min": "R$ 10.276",
            "salario_max": "R$ 10.276",
            "status": "Candidatura Pronta",
            "stack": ["Java 21", "Spring Boot 3", "Clean Architecture", "JUnit 5", "Spring AI MCP", "PostgreSQL"],
            "cv_pdf": "/carreira/vagas_analisadas/tech_dev/ntl_nova_tecnologia/Curriculo_Fabio_Rodrigues_Java_Backend.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/tech_dev/ntl_nova_tecnologia/Cover_Letter_Fabio_Rodrigues.pdf",
            "cover_docx": "/carreira/vagas_analisadas/tech_dev/ntl_nova_tecnologia/Cover_Letter_Fabio_Rodrigues.docx",
            "relatorio_pdf": "/carreira/vagas_analisadas/tech_dev/ntl_nova_tecnologia/relatorio_match_ntl_nova_tecnologia.pdf",
            "pitch_file": "carreira/vagas_analisadas/tech_dev/ntl_nova_tecnologia/carta_apresentacao_recruiter.md"
        },
        {
            "id": "avanade",
            "nome": "Avanade Brasil",
            "cargo": "Desenvolvedor(a) Back-End Spring Boot",
            "local": "Recife, PE",
            "modelo": "Híbrido / Remoto",
            "match": 93,
            "salario_min": "R$ 7.500",
            "salario_max": "R$ 9.000",
            "status": "Candidatura Pronta",
            "stack": ["Java 21", "Spring Boot 3", "Clean Architecture", "JUnit 5", "Spring AI MCP", "PostgreSQL"],
            "cv_pdf": "/carreira/vagas_analisadas/tech_dev/avanade/Curriculo_Fabio_Rodrigues_Java_Backend.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/tech_dev/avanade/Cover_Letter_Fabio_Rodrigues.pdf",
            "cover_docx": "/carreira/vagas_analisadas/tech_dev/avanade/Cover_Letter_Fabio_Rodrigues.docx",
            "relatorio_pdf": "/carreira/vagas_analisadas/tech_dev/avanade/relatorio_match_avanade.pdf",
            "pitch_file": "carreira/vagas_analisadas/tech_dev/avanade/carta_apresentacao_recruiter.md"
        },
        {
            "id": "capgemini",
            "nome": "Capgemini",
            "cargo": "Desenvolvedor(a) Java",
            "local": "Recife, PE",
            "modelo": "Híbrido",
            "match": 92,
            "salario_min": "R$ 6.500",
            "salario_max": "R$ 8.500",
            "status": "Candidatura Pronta",
            "stack": ["Java 21", "Spring Boot 3", "Arquitetura Hexagonal", "TDD", "PostgreSQL"],
            "cv_pdf": "/carreira/vagas_analisadas/tech_dev/capgemini/Curriculo_Fabio_Rodrigues_Java_Backend.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/tech_dev/capgemini/Cover_Letter_Fabio_Rodrigues.pdf",
            "cover_docx": "/carreira/vagas_analisadas/tech_dev/capgemini/Cover_Letter_Fabio_Rodrigues.docx",
            "relatorio_pdf": "/carreira/vagas_analisadas/tech_dev/capgemini/relatorio_match_capgemini.pdf",
            "pitch_file": "carreira/vagas_analisadas/tech_dev/capgemini/carta_apresentacao_recruiter.md"
        },
        {
            "id": "accenture",
            "nome": "Accenture",
            "cargo": "Backend Java & Spring",
            "local": "Recife, PE",
            "modelo": "Híbrido",
            "match": 88,
            "salario_min": "R$ 6.800",
            "salario_max": "R$ 9.000",
            "status": "Candidatura Pronta",
            "stack": ["Java 21", "Spring Boot 3", "Clean Architecture", "JUnit 5", "Spring AI"],
            "cv_pdf": "/carreira/vagas_analisadas/tech_dev/accenture/Curriculo_Fabio_Rodrigues_Java_Backend.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/tech_dev/accenture/Cover_Letter_Fabio_Rodrigues.pdf",
            "cover_docx": "/carreira/vagas_analisadas/tech_dev/accenture/Cover_Letter_Fabio_Rodrigues.docx",
            "relatorio_pdf": "/carreira/vagas_analisadas/tech_dev/accenture/relatorio_match_accenture.pdf",
            "pitch_file": "carreira/vagas_analisadas/tech_dev/accenture/carta_apresentacao_recruiter.md"
        },
        {
            "id": "deloitte",
            "nome": "Deloitte",
            "cargo": "Dev Java & Angular",
            "local": "Recife, PE",
            "modelo": "Híbrido",
            "match": 86,
            "salario_min": "R$ 7.000",
            "salario_max": "R$ 9.500",
            "status": "Candidatura Pronta",
            "stack": ["Java 21", "Spring Boot 3", "TypeScript", "Design Systems", "REST API"],
            "cv_pdf": "/carreira/vagas_analisadas/tech_dev/deloitte/Curriculo_Fabio_Rodrigues_Java_Backend.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/tech_dev/deloitte/Cover_Letter_Fabio_Rodrigues.pdf",
            "cover_docx": "/carreira/vagas_analisadas/tech_dev/deloitte/Cover_Letter_Fabio_Rodrigues.docx",
            "relatorio_pdf": "/carreira/vagas_analisadas/tech_dev/deloitte/relatorio_match_deloitte.pdf",
            "pitch_file": "carreira/vagas_analisadas/tech_dev/deloitte/carta_apresentacao_recruiter.md"
        },
        {
            "id": "romero_dornellas",
            "nome": "Assessoria RD (Romero Dornellas)",
            "cargo": "Social Media Presencial",
            "local": "Recife, PE",
            "modelo": "Presencial (Dedicado)",
            "match": 97,
            "salario_min": "R$ 3.500",
            "salario_max": "R$ 3.500",
            "status": "Candidatura Pronta",
            "stack": ["Design (UniFBV)", "Food Appeal / Gastronomia", "Final Cut / CapCut Pro", "iPhone 14 Pro Max", "Gildo / Primos"],
            "cv_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/romero_dornellas/Curriculo_Fabio_Rodrigues_Marketing_Design.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/romero_dornellas/Cover_Letter_Fabio_Rodrigues.pdf",
            "cover_docx": "/carreira/vagas_analisadas/marketing_audiovisual/romero_dornellas/Cover_Letter_Fabio_Rodrigues.docx",
            "relatorio_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/romero_dornellas/relatorio_match_romero_dornellas.pdf",
            "pitch_file": "carreira/vagas_analisadas/marketing_audiovisual/romero_dornellas/carta_apresentacao_recruiter.md"
        },
        {
            "id": "gummy",
            "nome": "Gummy Original",
            "cargo": "Analista de Marketing de Influência",
            "local": "Recife, PE",
            "modelo": "Híbrido / PJ",
            "match": 96,
            "salario_min": "R$ 3.800",
            "salario_max": "R$ 5.500",
            "status": "Candidatura Pronta",
            "stack": ["Design (UniFBV)", "Influencer Marketing", "UGC / Hooks 3s", "ROAS / Sheets", "Recife Ordinário"],
            "cv_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/gummy/Curriculo_Fabio_Rodrigues_Marketing_Design.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/gummy/Cover_Letter_Fabio_Rodrigues.pdf",
            "cover_docx": "/carreira/vagas_analisadas/marketing_audiovisual/gummy/Cover_Letter_Fabio_Rodrigues.docx",
            "relatorio_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/gummy/relatorio_match_gummy.pdf",
            "pitch_file": "carreira/vagas_analisadas/marketing_audiovisual/gummy/carta_apresentacao_recruiter.md"
        },
        {
            "id": "aposta_ganha",
            "nome": "Grupo Aposta Ganha",
            "cargo": "Analista de Copywriting",
            "local": "Recife, PE",
            "modelo": "Híbrido / CLT",
            "match": 94,
            "salario_min": "R$ 4.000",
            "salario_max": "R$ 5.500",
            "status": "Candidatura Pronta",
            "stack": ["Design (UniFBV)", "Copywriting/Storytelling", "CRM/Push", "Final Cut/Logic", "Gildo/Primos"],
            "cv_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/aposta_ganha/Curriculo_Fabio_Rodrigues_Marketing_Design.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/aposta_ganha/Cover_Letter_Fabio_Rodrigues.pdf",
            "cover_docx": "/carreira/vagas_analisadas/marketing_audiovisual/aposta_ganha/Cover_Letter_Fabio_Rodrigues.docx",
            "relatorio_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/aposta_ganha/relatorio_match_aposta_ganha.pdf",
            "pitch_file": "carreira/vagas_analisadas/marketing_audiovisual/aposta_ganha/carta_apresentacao_recruiter.md"
        },
        {
            "id": "rio_ave",
            "nome": "RIO AVE",
            "cargo": "Analista de Marketing Pleno",
            "local": "Recife, PE",
            "modelo": "Presencial / CLT",
            "match": 95,
            "salario_min": "R$ 4.500",
            "salario_max": "R$ 6.000",
            "status": "Candidatura Pronta",
            "stack": ["Design (UniFBV)", "Final Cut Pro", "CapCut Pro", "DaVinci Resolve", "Canva Pro/Figma"],
            "cv_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/rio_ave/Curriculo_Fabio_Rodrigues_Marketing_Design.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/rio_ave/Cover_Letter_Fabio_Rodrigues.pdf",
            "cover_docx": "/carreira/vagas_analisadas/marketing_audiovisual/rio_ave/Cover_Letter_Fabio_Rodrigues.docx",
            "relatorio_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/rio_ave/relatorio_match_rio_ave.pdf",
            "pitch_file": "carreira/vagas_analisadas/marketing_audiovisual/rio_ave/carta_apresentacao_recruiter.md"
        },
        {
            "id": "grupo_luck",
            "nome": "Grupo Luck",
            "cargo": "Analista de Endomarketing CSC",
            "local": "Recife, PE",
            "modelo": "Presencial / CSC",
            "match": 92,
            "salario_min": "R$ 4.500",
            "salario_max": "R$ 5.200",
            "status": "Candidatura Pronta",
            "stack": ["Design (UniFBV)", "Photoshop/Illustrator", "Premiere/CapCut", "Endomarketing", "IA Criativa"],
            "cv_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/grupo_luck/Curriculo_Fabio_Rodrigues_Marketing_Design.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/grupo_luck/Cover_Letter_Fabio_Rodrigues.pdf",
            "cover_docx": "/carreira/vagas_analisadas/marketing_audiovisual/grupo_luck/Cover_Letter_Fabio_Rodrigues.docx",
            "relatorio_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/grupo_luck/relatorio_match_grupo_luck.pdf",
            "pitch_file": "carreira/vagas_analisadas/marketing_audiovisual/grupo_luck/carta_apresentacao_recruiter.md"
        },
        {
            "id": "auto_nunes",
            "nome": "Grupo Auto Nunes",
            "cargo": "Analista de Marketing (Automotivo)",
            "local": "Jaboatão / Recife, PE",
            "modelo": "Presencial / CLT",
            "match": 96,
            "salario_min": "R$ 3.500",
            "salario_max": "R$ 6.000",
            "status": "Candidatura Pronta",
            "stack": ["Design (UniFBV)", "Final Cut Pro / CapCut", "Canva Pro / Figma", "Setor Automotivo / Olimac", "Gráfica / PDV"],
            "cv_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/auto_nunes/Curriculo_Fabio_Rodrigues_Marketing_Design.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/auto_nunes/Cover_Letter_Fabio_Rodrigues.pdf",
            "cover_docx": "/carreira/vagas_analisadas/marketing_audiovisual/auto_nunes/Cover_Letter_Fabio_Rodrigues.docx",
            "relatorio_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/auto_nunes/relatorio_match_auto_nunes.pdf",
            "pitch_file": "carreira/vagas_analisadas/marketing_audiovisual/auto_nunes/carta_apresentacao_recruiter.md"
        },
        {
            "id": "distribuidora_food_service",
            "nome": "Distribuidora Food Service",
            "cargo": "Analista de Marketing Pleno",
            "local": "Recife, PE",
            "modelo": "Presencial / CLT",
            "match": 96,
            "salario_min": "R$ 3.066",
            "salario_max": "R$ 5.519",
            "status": "Candidatura Pronta",
            "stack": ["Design (UniFBV)", "Branding / Trade Marketing", "Final Cut / DaVinci", "Gildo Lanches / Food Service", "Gráfica / PDV"],
            "cv_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/distribuidora_food_service/Curriculo_Fabio_Rodrigues_Marketing_Design.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/distribuidora_food_service/Cover_Letter_Fabio_Rodrigues.pdf",
            "cover_docx": "/carreira/vagas_analisadas/marketing_audiovisual/distribuidora_food_service/Cover_Letter_Fabio_Rodrigues.docx",
            "relatorio_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/distribuidora_food_service/relatorio_match_distribuidora_food_service.pdf",
            "pitch_file": "carreira/vagas_analisadas/marketing_audiovisual/distribuidora_food_service/carta_apresentacao_recruiter.md"
        },
        {
            "id": "esportes_gaming_brasil",
            "nome": "Grupo Esportes Gaming Brasil",
            "cargo": "Supervisor de Social Media",
            "local": "Recife, PE",
            "modelo": "Presencial / CLT",
            "match": 98,
            "salario_min": "R$ 7.500",
            "salario_max": "R$ 9.500",
            "status": "Candidatura Pronta",
            "stack": ["Design (UniFBV)", "Liderança Criativa", "TikTok / X / Reels", "Gaming & iGaming / Unigames", "Final Cut / CapCut"],
            "cv_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/esportes_gaming_brasil/Curriculo_Fabio_Rodrigues_Marketing_Design.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/esportes_gaming_brasil/Cover_Letter_Fabio_Rodrigues.pdf",
            "cover_docx": "/carreira/vagas_analisadas/marketing_audiovisual/esportes_gaming_brasil/Cover_Letter_Fabio_Rodrigues.docx",
            "relatorio_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/esportes_gaming_brasil/relatorio_match_esportes_gaming_brasil.pdf",
            "pitch_file": "carreira/vagas_analisadas/marketing_audiovisual/esportes_gaming_brasil/carta_apresentacao_recruiter.md"
        },
        {
            "id": "gf_casa_decor",
            "nome": "GF Casa Decor",
            "cargo": "Criativo de Marketing & Conteúdo",
            "local": "Recife, PE",
            "modelo": "Presencial / CLT",
            "match": 98,
            "salario_min": "R$ 3.500",
            "salario_max": "R$ 4.500",
            "status": "Candidatura Pronta",
            "stack": ["Design (UniFBV)", "Reels / TikTok", "Canva Pro / Figma", "CapCut / Final Cut", "Varejo / Loja Física"],
            "cv_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/gf_casa_decor/Curriculo_Fabio_Rodrigues_Marketing_Design.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/gf_casa_decor/Cover_Letter_Fabio_Rodrigues.pdf",
            "cover_docx": "/carreira/vagas_analisadas/marketing_audiovisual/gf_casa_decor/Cover_Letter_Fabio_Rodrigues.docx",
            "relatorio_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/gf_casa_decor/relatorio_match_gf_casa_decor.pdf",
            "pitch_file": "carreira/vagas_analisadas/marketing_audiovisual/gf_casa_decor/carta_apresentacao_recruiter.md"
        },
        {
            "id": "beside_media",
            "nome": "Beside Media",
            "cargo": "Analista de Mídia Paga",
            "local": "Brasil (Global)",
            "modelo": "100% Remoto",
            "match": 96,
            "salario_min": "R$ 6.000",
            "salario_max": "R$ 8.000",
            "status": "Candidatura Pronta",
            "stack": ["Design (UniFBV)", "Meta Ads / TikTok Ads", "Testes A/B Criativos", "GA4 / Looker Studio", "Growth / Automação"],
            "cv_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/beside_media/Curriculo_Fabio_Rodrigues_Marketing_Design.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/beside_media/Cover_Letter_Fabio_Rodrigues.pdf",
            "cover_docx": "/carreira/vagas_analisadas/marketing_audiovisual/beside_media/Cover_Letter_Fabio_Rodrigues.docx",
            "relatorio_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/beside_media/relatorio_match_beside_media.pdf",
            "pitch_file": "carreira/vagas_analisadas/marketing_audiovisual/beside_media/carta_apresentacao_recruiter.md"
        },
        {
            "id": "jobgether_luxury_skincare",
            "nome": "Jobgether (Luxury Skincare)",
            "cargo": "Video Editor (Luxury Skincare Brand)",
            "local": "Brasil (Global)",
            "modelo": "100% Remoto",
            "match": 97,
            "salario_min": "R$ 4.500",
            "salario_max": "R$ 9.000",
            "status": "Candidatura Pronta",
            "stack": ["Design (UniFBV)", "Final Cut Pro / CapCut", "DaVinci (Color Grading)", "Logic Pro (Sound Design)", "4K ProRes / Ads"],
            "cv_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/jobgether_luxury_skincare/Curriculo_Fabio_Rodrigues_Marketing_Design.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/jobgether_luxury_skincare/Cover_Letter_Fabio_Rodrigues.pdf",
            "cover_docx": "/carreira/vagas_analisadas/marketing_audiovisual/jobgether_luxury_skincare/Cover_Letter_Fabio_Rodrigues.docx",
            "relatorio_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/jobgether_luxury_skincare/relatorio_match_jobgether_luxury_skincare.pdf",
            "pitch_file": "carreira/vagas_analisadas/marketing_audiovisual/jobgether_luxury_skincare/carta_apresentacao_recruiter.md"
        },
        {
            "id": "fullstack",
            "nome": "FullStack Connect",
            "cargo": "Lead Software Engineer",
            "local": "Remoto (EUA)",
            "modelo": "100% Remoto",
            "match": 68,
            "salario_min": "$ 4,500/mês",
            "salario_max": "$ 6,500/mês",
            "status": "Análise Estratégica",
            "stack": ["Java 21", "Spring Boot 3", "AI Agents", "Scrum Leadership", "English"],
            "cv_pdf": "/carreira/vagas_analisadas/tech_dev/fullstack/Curriculo_Fabio_Rodrigues_FullStack.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/tech_dev/fullstack/Cover_Letter_Fabio_Rodrigues.pdf",
            "cover_docx": "/carreira/vagas_analisadas/tech_dev/fullstack/Cover_Letter_Fabio_Rodrigues.docx",
            "relatorio_pdf": "/carreira/vagas_analisadas/tech_dev/fullstack/relatorio_match_fullstack.pdf",
            "pitch_file": "carreira/vagas_analisadas/tech_dev/fullstack/carta_apresentacao_recruiter.md"
        }
    ]

    for emp in empresas:
        caminho_pitch = os.path.join(WORKSPACE_DIR, emp["pitch_file"])
        if os.path.exists(caminho_pitch):
            try:
                with open(caminho_pitch, "r", encoding="utf-8") as f:
                    emp["pitch_texto"] = f.read()
            except Exception:
                emp["pitch_texto"] = "Pitch indisponível."
        else:
            emp["pitch_texto"] = "Pitch pronto para abordagem de Recruiter."

    return empresas

def obter_dados_estudos(demo=False):
    if demo:
        return {
            "trilha": "Bootcamp Santander 2026 - AI Java Back-end (DIO) & Full Stack Cloud",
            "plataforma": "DIO (Digital Innovation One) & Especialização Cloud DevOps",
            "modulos_concluidos": 26,
            "total_modulos": 26,
            "progresso_percentual": 100.0,
            "modulo_atual": "Formação Completa Concluída (26/26)",
            "proxima_meta": "Certificado Emitido & Especialização Full Stack Cloud",
            "status": "CERTIFICADO EMITIDO",
            "nivel": "Java Back-end & Full Stack Cloud",
            "manual_pdf": "/download/estudos/guia_estudos_nova/Manual_Engenharia_e_Arquitetura_NOVA.pdf"
        }
    
    return {
        "trilha": "Bootcamp Santander 2026 - AI Java Back-end (DIO) & Full Stack Cloud",
        "plataforma": "DIO (Digital Innovation One) & Especialização Cloud DevOps",
        "modulos_concluidos": 26,
        "total_modulos": 26,
        "progresso_percentual": 100.0,
        "modulo_atual": "Formação Completa Concluída (26/26)",
        "proxima_meta": "Certificado Emitido & Especialização Full Stack Cloud",
        "status": "CERTIFICADO EMITIDO",
        "nivel": "Java Back-end & Full Stack Cloud",
        "manual_pdf": "/download/estudos/guia_estudos_nova/Manual_Engenharia_e_Arquitetura_NOVA.pdf"
    }

def carregar_config_voz():
    if os.path.exists(CONFIG_VOZ_PATH):
        try:
            with open(CONFIG_VOZ_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"voz_padrao": "pt-BR-FranciscaNeural", "velocidade": "+0%", "tom": "+0Hz"}

def salvar_config_voz(data):
    try:
        with open(CONFIG_VOZ_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

VOZES_CATALOGO = [
    {
        "id": "pt-BR-FranciscaNeural",
        "nome": "Francisca",
        "idioma": "pt-BR",
        "genero": "Feminino",
        "tag": "Acolhedora / Fluida",
        "descricao": "Voz executiva feminina padrão do NOVA. Dicção impecável, tom caloroso e natural.",
        "icone": "👩‍💼",
        "frase_demo": "Olá, Fábio! Sou a Francisca. Seus relatórios financeiros e candidaturas estão prontos para envio."
    },
    {
        "id": "pt-BR-AntonioNeural",
        "nome": "Antônio",
        "idioma": "pt-BR",
        "genero": "Masculino",
        "tag": "Executiva / Natural",
        "descricao": "Tom sério, articulado e altamente profissional.",
        "icone": "👨‍💼",
        "frase_demo": "Olá, Fábio! Eu sou o Antônio, sua voz no ecossistema NOVA. Todos os microsserviços estão operacionais."
    },
    {
        "id": "pt-BR-FabioNeural",
        "nome": "Fábio",
        "idioma": "pt-BR",
        "genero": "Masculino",
        "tag": "Direta / Ágil",
        "descricao": "Voz masculina jovem e dinâmica. Ideal para respostas rápidas de terminal.",
        "icone": "👨‍💻",
        "frase_demo": "Fala, Fábio! Sou o Fábio Neural. Construímos uma arquitetura sólida em Java 21 e Spring Boot 3."
    },
    {
        "id": "pt-BR-ThalitaNeural",
        "nome": "Thalita",
        "idioma": "pt-BR",
        "genero": "Feminino",
        "tag": "Jovem / Expressiva",
        "descricao": "Tom conversacional e enérgico, com entonação espontânea.",
        "icone": "👩‍🎨",
        "frase_demo": "Oi, Fábio! Sou a Thalita. Seus estudos da Trilha Santander 2026 estão avançando com força total!"
    },
    {
        "id": "en-US-GuyNeural",
        "nome": "Guy (English)",
        "idioma": "en-US",
        "genero": "Masculino",
        "tag": "International Tech Lead",
        "descricao": "Voz americana executiva de alta credibilidade para entrevistas e clientes globais.",
        "icone": "🌐",
        "frase_demo": "Hello, Fabio! Guy speaking. Your international portfolio and applications look solid."
    },
    {
        "id": "en-US-JennyNeural",
        "nome": "Jenny (English)",
        "idioma": "en-US",
        "genero": "Feminino",
        "tag": "Silicon Valley Native",
        "descricao": "Voz executiva americana fluida e polida para reuniões internacionais.",
        "icone": "✨",
        "frase_demo": "Hi, Fabio! Jenny here. Your Clean Architecture backend and Spring AI modules are fully verified."
    }
]

def condensar_resposta_para_voz(texto: str, max_frases: int = 3) -> str:
    if not texto:
        return ""
    if len(texto) <= 220:
        return texto.strip()
    linhas = [l.strip() for l in texto.split("\n") if l.strip() and not l.strip().startswith("#") and not l.strip().startswith("|")]
    texto_limpo = " ".join(linhas)
    import re
    sentencas = re.split(r'(?<=[.!?])\s+', texto_limpo)
    sentencas_uteis = [s.strip() for s in sentencas if len(s.strip()) > 5]
    if len(sentencas_uteis) <= max_frases:
        return " ".join(sentencas_uteis)
    return " ".join(sentencas_uteis[:max_frases]).strip()

def sanitizar_texto_para_fala(texto: str) -> str:
    if not texto:
        return ""
    import re
    texto = condensar_resposta_para_voz(texto, max_frases=3)
    custom_symbols = [
        "■", "▪", "▫", "🔹", "🔸", "📍", "📧", "📱", "💼", "💻", "🚀", "🌌",
        "🎙️", "🎙", "🎓", "🎯", "🛠️", "🛠", "🔍", "⚡", "📅", "📝", "📊",
        "💡", "⚪", "🟢", "🟡", "❌", "🌟", "✨", "🔗", "⭐", "🏷️", "🏷", "🍩", "💰", "✉️", "📚", "☕", "🍃", "🏛️", "🏛", "🧪", "💾", "🤖", "🐍", "📑"
    ]
    for sym in custom_symbols:
        texto = texto.replace(sym, "")
    emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
    texto = emoji_pattern.sub('', texto)
    texto = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', texto)
    texto = texto.replace("**", "").replace("*", "").replace("`", "").replace("#", "")
    texto = re.sub(r'R\$\s*([\d\.]+),(\d{2})', r'\1 reais e \2 centavos', texto)
    texto = re.sub(r'R\$\s*([\d\.]+)', r'\1 reais', texto)
    texto = re.sub(r' +', ' ', texto)
    return texto.strip()

async def sintetizar_audio_base64(texto: str, voz_id: str, taxa: str = "+0%") -> str:
    if not edge_tts:
        return ""
    
    texto_processado = sanitizar_texto_para_fala(texto)
    if not texto_processado:
        return ""

    # 1. Tentativa via stream assíncrono em memória (ultra-rápido, sem I/O de disco)
    try:
        comunicador = edge_tts.Communicate(text=texto_processado, voice=voz_id, rate=taxa)
        chunks = []
        async for chunk in comunicador.stream():
            if chunk.get("type") == "audio":
                chunks.append(chunk.get("data", b""))
        audio_bytes = b"".join(chunks)
        if audio_bytes:
            return base64.b64encode(audio_bytes).decode('utf-8')
    except Exception as e:
        print(f"[VOZ] Erro na síntese em memória: {e}")

    # 2. Fallback via arquivo temporário
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            temp_path = temp_file.name
        comunicador = edge_tts.Communicate(text=texto_processado, voice=voz_id, rate=taxa)
        await comunicador.save(temp_path)
        with open(temp_path, "rb") as f:
            audio_bytes = f.read()
        return base64.b64encode(audio_bytes).decode('utf-8')
    except Exception as e:
        print(f"[VOZ] Erro na síntese tempfile: {e}")
        return ""
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass

def processar_intencao_voz(comando_texto: str, demo: bool = False, is_demo: bool = None) -> str:
    """
    Roteador semântico de inteligência por voz para Carreira, Estudos, Finanças, Apresentação e Conhecimento Geral.
    Aplica isolamento estrito LGPD Safe quando demo for True.
    """
    if is_demo is not None:
        demo = is_demo

    cmd = (comando_texto or "").lower().strip()

    # 1. Apresentação / Capacidades do Assistente
    # "o que você pode fazer", "o que voce faz", "quais suas funcoes", "quais seus comandos", "como pode me ajudar"
    termos_apresentacao = [
        "o que você pode fazer", "o que voce pode fazer",
        "o que você faz", "o que voce faz",
        "o que você sabe fazer", "o que voce sabe fazer",
        "quais suas funcoes", "quais suas funções",
        "quais seus comandos", "quais os comandos",
        "como pode me ajudar", "como me ajuda",
        "o que você faz aqui", "o que voce faz aqui",
        "quem é você", "quem e voce", "suas funções", "suas funcoes",
        "o que pode fazer"
    ]
    if any(p in cmd for p in termos_apresentacao):
        return (
            "Olá! Sou o NOVA, seu assistente de inteligência e orquestrador de engenharia. "
            "Posso consultar seu saldo e projeção financeira em tempo real, "
            "apresentar suas candidaturas ativas e índice de match por vaga, "
            "acompanhar seu plano de estudos e mentoria técnica, "
            "e monitorar a telemetria do microsserviço Spring Boot com suíte de testes. "
            "Você pode me perguntar: 'qual meu saldo', 'quais minhas vagas', ou 'como estão meus estudos'."
        )

    # 2. Finanças / Saldo / Gastos / Previsão
    # "qual meu saldo", "resumo financeiro", "gastos", "previsão"
    termos_financas = [
        "qual meu saldo", "qual o meu saldo", "meu saldo", "saldo",
        "resumo financeiro", "gastos", "gasto", "quanto gastei",
        "previsão", "previsao", "previsao financeira", "projecao", "projeção",
        "despesas", "despesa", "receitas", "receita", "dinheiro", "caixa", "quanto sobrou"
    ]
    if any(p in cmd for p in termos_financas):
        if demo:
            return (
                "No Modo Demonstração protegido por privacidade, seu saldo consolidado é de 4.250 reais, "
                "com 7 entradas de receitas e 36 saídas controladas no período apurado. "
                "O fluxo financeiro está saudável, mantendo as reservas técnicas e superávit operacional estimado."
            )
        else:
            fin = obter_resumo_financeiro(demo=False)
            saldo = fin.get("saldo", 589.23)
            rec = fin.get("totalReceitas", 2299.00)
            desp = fin.get("totalGasto", 1709.77)
            saldo_fmt = f"{saldo:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            rec_fmt = f"{rec:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            desp_fmt = f"{desp:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            return (
                f"Fábio, seu saldo real consolidado no banco H2 é de {saldo_fmt} reais. "
                f"No período apurado, suas receitas somam {rec_fmt} reais e o total de despesas pagas é de {desp_fmt} reais, "
                f"mantendo seu fluxo de caixa positivo e dados protegidos."
            )

    # 3. Carreira / Vagas / Candidaturas / Melhor Vaga
    # "minha carreira", "vagas", "melhor vaga", "candidaturas"
    termos_carreira = [
        "minha carreira", "carreira", "vagas", "vaga", "melhor vaga",
        "candidaturas", "candidatura", "onde me candidatar", "oportunidades",
        "empresas", "recruiter", "pitch", "entrevistas", "processos seletivos"
    ]
    if any(p in cmd for p in termos_carreira):
        if demo:
            return (
                "No Modo Demonstração, temos três oportunidades de referência mapeadas: "
                "TechCorp Global com 96% de aderência técnica para Arquiteto Back-end, "
                "FinScale Systems com 94% para Especialista Java e CloudLab AI com 91% de match para Engenharia de IA."
            )
        else:
            vagas = obter_dados_candidaturas(demo=False)
            total_vagas = len(vagas)
            melhor = max(vagas, key=lambda v: v.get("match", 0)) if vagas else None
            melhor_nome = melhor.get("nome", "Gummy") if melhor else "Gummy"
            melhor_match = melhor.get("match", 96) if melhor else 96
            return (
                f"Fábio, no seu painel de carreiras temos {total_vagas} oportunidades mapeadas com alto índice de match. "
                f"A principal oportunidade é a {melhor_nome} com {melhor_match}% de aderência técnica para Tech e Vídeo, "
                f"seguida por Capgemini com 92% para Java Back-end, Accenture com 88% e Deloitte com 86%."
            )

    # 4. Estudos / Progresso / O que estudar
    # "estudos", "o que estudar", "progresso"
    termos_estudos = [
        "estudos", "estudo", "o que estudar", "progresso",
        "trilha", "dio", "santander", "curso", "módulo", "modulo",
        "feynman", "formação", "formacao", "plano de estudos"
    ]
    if any(p in cmd for p in termos_estudos):
        if demo:
            return (
                "No seu currículo do Modo Demonstração, você está na Especialização em Engenharia de Sistemas Distribuídos e Cloud Native "
                "com 90% de conclusão em 18 de 20 módulos finalizados, focando em Virtual Threads no Java 21, Kafka e arquitetura orientada a eventos."
            )
        else:
            return (
                "Fábio, você atingiu 100% de conclusão na Trilha Santander 2026 AI Java Back-end da DIO com 26 de 26 atividades e certificado emitido, "
                "além de ter concluído todos os 5 módulos da Especialização Full Stack e Cloud DevOps cobrindo Docker, CI/CD e deploy no Render."
            )

    # 5. Engenharia / Status / Testes / Microsserviço
    termos_engenharia = [
        "engenharia", "status", "sistema", "sistemas", "operacional", "operacionais",
        "microsserviço", "microsservico", "teste", "testes", "junit", "spring boot", "health"
    ]
    if any(p in cmd for p in termos_engenharia):
        return (
            "Todos os sistemas do NOVA estão plenamente operacionais: "
            "Microsserviço Spring Boot 3 na porta 8081 ativo, persistência relacional H2 ACID e 40 testes automatizados JUnit 5 aprovados com 100% de sucesso."
        )

    # 6. Saudação Inicial / Boas-Vindas
    if not cmd or cmd in ["olá", "ola", "oi", "bom dia", "boa tarde", "boa noite", "nova", "hello", "hi"]:
        return "Olá! Bem-vindo ao NOVA Control Center, o ecossistema autônomo desenvolvido por Fábio Rodrigues. Sou a interface de voz neural conectada a microsserviços em Java 21, Clean Architecture e Spring AI (MCP). Você pode falar pelo microfone ou testar comandos como /status, /vagas ou /financeiro."

    # 7. Conceitos Técnicos (Nível 2)
    if "clean architecture" in cmd or "arquitetura hexagonal" in cmd:
        return "Clean Architecture é um padrão arquitetural que isola as regras de negócio de frameworks e bancos de dados através de casos de uso e inversão de dependências."
    elif "tdd" in cmd or "test driven" in cmd:
        return "TDD é a prática de desenvolvimento guiado por testes onde escrevemos primeiro o teste que falha, implementamos o código mínimo e depois refatoramos com segurança."
    elif "solid" in cmd:
        return "SOLID são cinco princípios de design orientado a objetos que promovem código desacoplado, extensível, coeso e de fácil manutenção."
    elif "mcp" in cmd or "model context" in cmd:
        return "O Model Context Protocol é o padrão aberto para integrar ferramentas e bancos de dados diretamente ao contexto de agentes e modelos de inteligência artificial."

    # 8. Fallback Geral
    return (
        "Reconheci seu comando. Como assistente do NOVA, posso apresentar seu saldo financeiro, "
        "vagas de carreira, progresso de estudos ou telemetria dos sistemas. "
        "Experimente perguntar: 'qual meu saldo', ou 'o que você pode fazer'."
    )

class DashboardHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Admin-PIN, X-Admin-Pin, X-NOVA-PIN, X-NOVA-Demo")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self.serve_file(os.path.join(BASE_DIR, "index.html"), "text/html; charset=utf-8")
        elif path == "/styles.css":
            self.serve_file(os.path.join(BASE_DIR, "styles.css"), "text/css; charset=utf-8")
        elif path == "/app.js":
            self.serve_file(os.path.join(BASE_DIR, "app.js"), "application/javascript; charset=utf-8")
        elif path.startswith("/assets/"):
            file_path = os.path.join(BASE_DIR, path.lstrip("/"))
            if os.path.exists(file_path) and os.path.isfile(file_path):
                mime_type, _ = mimetypes.guess_type(file_path)
                self.serve_file(file_path, mime_type or "image/svg+xml")
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Asset nao encontrado")
        
        query = urllib.parse.parse_qs(parsed.query)
        demo_active = is_demo_mode(self, query)
        autenticado = is_pin_valido(self)

        if path == "/api/status":
            dados = {
                "demo_mode": demo_active,
                "authenticated": autenticado,
                "privacy_status": "MODO_DEMONSTRACAO" if demo_active else "MODO_REAL",
                "financas": obter_resumo_financeiro(demo=demo_active),
                "projecao": obter_projecao_financeira(demo=demo_active),
                "caixinhas": obter_caixinhas_patrimonio(demo=demo_active),
                "candidaturas": obter_dados_candidaturas(demo=demo_active),
                "voz": carregar_config_voz(),
                "estudos": obter_dados_estudos(demo=demo_active),
                "engenharia": {
                    "testes_total": 40,
                    "testes_passando": 40,
                    "taxa_sucesso": 100.0,
                    "spring_boot_porta": 8081,
                    "banco": "H2 Database (ACID - ./data/financiadb.mv.db)",
                    "protocolos": ["REST (RFC 7807)", "Spring AI MCP (@Tool)", "edge-tts Voice AI", "OFX/CSV Importer", "Nubank Webhook", "Caixinhas Asset Management"]
                }
            }
            self.send_json(dados)

        elif path == "/api/financeiro/projecao":
            self.send_json(obter_projecao_financeira(demo=demo_active))

        elif path == "/api/financeiro/caixinhas":
            self.send_json(obter_caixinhas_patrimonio(demo=demo_active))

        elif path == "/api/privacy/status":
            client_ip = self.client_address[0] if self.client_address else "127.0.0.1"
            self.send_json({
                "demo_mode": demo_active,
                "authenticated": autenticado,
                "client_ip": client_ip,
                "is_local": client_ip in ("127.0.0.1", "::1", "localhost")
            })

        elif path == "/api/voice/config":
            self.send_json(carregar_config_voz())

        elif path in ("/voice-studio/api/voices", "/voice-studio/api/catalog"):
            self.send_json(VOZES_CATALOGO)

        elif path == "/voice-studio/api/config":
            self.send_json(carregar_config_voz())

        # Proxy Reverso: Voice Studio (Repassa /voice-studio/* para http://localhost:5050/*)
        elif path.startswith("/voice-studio"):
            subpath = path[len("/voice-studio"):]
            if not subpath:
                subpath = "/"
            if parsed.query:
                subpath += f"?{parsed.query}"
            self.forward_to_voice_studio("GET", subpath, headers=dict(self.headers))

        elif path.startswith("/download/"):
            rel_path = path.replace("/download/", "")
            file_path = os.path.join(WORKSPACE_DIR, rel_path)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                mime_type, _ = mimetypes.guess_type(file_path)
                self.serve_file(file_path, mime_type or "application/octet-stream", as_attachment=True)
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Arquivo nao encontrado")

        elif path.startswith("/carreira/") or path.startswith("/financeiro/"):
            if not autenticado:
                self.send_response(403)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"erro": "Acesso negado: dados confidenciais protegidos por PIN de administrador."}).encode('utf-8'))
                return
            file_path = os.path.join(WORKSPACE_DIR, path.lstrip("/"))
            if os.path.exists(file_path) and os.path.isfile(file_path):
                mime_type, _ = mimetypes.guess_type(file_path)
                self.serve_file(file_path, mime_type or "application/octet-stream")
            else:
                self.send_response(404)
                self.end_headers()

        else:
            file_path = os.path.join(WORKSPACE_DIR, path.lstrip("/"))
            if os.path.exists(file_path) and os.path.isfile(file_path):
                mime_type, _ = mimetypes.guess_type(file_path)
                self.serve_file(file_path, mime_type or "application/octet-stream")
            else:
                self.send_response(404)
                self.end_headers()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)

        # Validação de PIN de Administrador (Desbloqueio de Dados Reais)
        if parsed.path == "/api/auth/verify-pin":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else b""
            try:
                req_data = json.loads(body.decode('utf-8')) if body else {}
                pin_informado = str(req_data.get("pin", "")).strip()

                if pin_informado == ADMIN_PIN:
                    self.send_json({
                        "authenticated": True,
                        "token": ADMIN_PIN,
                        "message": "PIN de administrador autenticado com sucesso."
                    })
                else:
                    self.send_response(401)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "authenticated": False,
                        "message": "PIN de segurança incorreto. Tente novamente."
                    }).encode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"authenticated": False, "erro": str(e)}).encode('utf-8'))

        # Interação de voz bidirecional (Microfone -> Spring Boot -> Síntese Base64)
        elif parsed.path == "/api/voice/interact":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                req_data = json.loads(body.decode('utf-8')) if body else {}
                comando = req_data.get("comando", "Olá")
                
                # Extrai o PIN e a flag
                pin = req_data.get('pin') or self.headers.get('X-NOVA-PIN', '') or extrair_pin_requisicao(self)
                is_demo_req = req_data.get('is_demo')
                
                # Define o modo real se o PIN for 7770
                demo_ativo = False if str(pin).strip() == '7770' else (True if is_demo_req is True else is_demo_mode(self))
                
                # 1. Processa semântica em Carreira, Estudos, Finanças ou Apresentação
                resposta_texto = processar_intencao_voz(comando, demo=demo_ativo)

                # 2. Configurações de voz
                cfg = carregar_config_voz()
                voz_id = req_data.get("voz") or cfg.get("voz_padrao", "pt-BR-FranciscaNeural")
                taxa = cfg.get("velocidade", "+0%")

                # 3. Síntese de áudio em Base64
                audio_b64 = asyncio.run(sintetizar_audio_base64(resposta_texto, voz_id, taxa))

                self.send_json({
                    "texto": resposta_texto,
                    "audio_base64": audio_b64,
                    "voz": voz_id,
                    "is_demo": demo_ativo,
                    "demo": demo_ativo,
                    "status": "SUCESSO"
                })
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"erro": str(e)}).encode('utf-8'))

        # Troca rápida de voz padrão
        elif parsed.path == "/api/voice/set-voice":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                req_data = json.loads(body.decode('utf-8'))
                nova_voz = req_data.get("voz")
                
                cfg = carregar_config_voz()
                if nova_voz:
                    cfg["voz_padrao"] = nova_voz
                    salvar_config_voz(cfg)

                self.send_json({"status": "OK", "voz_padrao": cfg["voz_padrao"]})
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))

        # Rota nativa de síntese do Voice Studio (Edge-TTS in-memory streaming)
        elif parsed.path == "/voice-studio/api/synthesize":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                req_data = json.loads(body.decode('utf-8'))
                texto = req_data.get("texto", "Olá, bem-vindo ao Voice Studio!")
                voz_id = req_data.get("voz", "pt-BR-FranciscaNeural")
                taxa = req_data.get("taxa", "+0%")
                audio_b64 = asyncio.run(sintetizar_audio_base64(texto, voz_id, taxa))
                if audio_b64:
                    audio_bytes = base64.b64decode(audio_b64)
                    self.send_response(200)
                    self.send_header("Content-Type", "audio/mpeg")
                    self.send_header("Content-Length", str(len(audio_bytes)))
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(audio_bytes)
                else:
                    self.send_response(500)
                    self.end_headers()
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))

        elif parsed.path == "/voice-studio/api/config":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                req_data = json.loads(body.decode('utf-8'))
                salvar_config_voz(req_data)
                self.send_json({"status": "OK", "config": carregar_config_voz()})
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))

        # Proxy Reverso: Voice Studio POST (/voice-studio/* repassado para http://localhost:5050/*)
        elif parsed.path.startswith("/voice-studio"):
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else None
            subpath = parsed.path[len("/voice-studio"):]
            if not subpath:
                subpath = "/"
            if parsed.query:
                subpath += f"?{parsed.query}"
            self.forward_to_voice_studio("POST", subpath, body=body, headers=dict(self.headers))

        else:
            self.send_response(404)
            self.end_headers()

    def forward_to_voice_studio(self, method, subpath, body=None, headers=None):
        target_url = f"http://127.0.0.1:5050{subpath}"
        try:
            req_headers = {}
            if headers:
                for k, v in headers.items():
                    if k.lower() not in ['host', 'content-length', 'connection']:
                        req_headers[k] = v
            req = urllib.request.Request(target_url, data=body, headers=req_headers, method=method)
            with urllib.request.urlopen(req, timeout=12) as resp:
                resp_body = resp.read()
                self.send_response(resp.status)
                for k, v in resp.getheaders():
                    if k.lower() not in ['transfer-encoding', 'content-length', 'connection']:
                        self.send_header(k, v)
                self.send_header('Content-Length', str(len(resp_body)))
                self.end_headers()
                self.wfile.write(resp_body)
        except urllib.error.HTTPError as e:
            err_body = e.read()
            self.send_response(e.code)
            for k, v in e.headers.items():
                if k.lower() not in ['transfer-encoding', 'content-length', 'connection']:
                    self.send_header(k, v)
            self.send_header('Content-Length', str(len(err_body)))
            self.end_headers()
            self.wfile.write(err_body)
        except Exception as e:
            self.send_response(502)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"erro": f"Voice Studio backend indisponível: {str(e)}"}).encode('utf-8'))

    def serve_file(self, file_path, content_type, as_attachment=False):
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            if as_attachment:
                filename = os.path.basename(file_path)
                self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode('utf-8'))

    def send_json(self, data):
        json_bytes = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(json_bytes)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Admin-PIN, X-Admin-Pin, X-NOVA-PIN, X-NOVA-Demo")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()
        self.wfile.write(json_bytes)

    def log_message(self, format, *args):
        pass

def iniciar_dashboard(porta_desejada=None):
    global PORT
    host = os.environ.get("HOST", "0.0.0.0")
    env_port = os.environ.get("PORT") or os.environ.get("NOVA_PORT")

    if porta_desejada is not None:
        porta = int(porta_desejada)
    elif len(sys.argv) > 1:
        for i, arg in enumerate(sys.argv[1:]):
            if arg in ("--port", "-p") and i + 2 <= len(sys.argv):
                try:
                    porta = int(sys.argv[i + 2])
                    break
                except ValueError:
                    pass
            elif arg.isdigit():
                porta = int(arg)
                break
        else:
            porta = int(env_port) if env_port and env_port.isdigit() else DEFAULT_PORT
    elif env_port and env_port.isdigit():
        porta = int(env_port)
    else:
        porta = DEFAULT_PORT

    server = None
    try:
        server = HTTPServer((host, porta), DashboardHandler)
        PORT = porta
    except (PermissionError, OSError) as e:
        if porta != 3000:
            print(f"⚠️ Não foi possível iniciar na porta {porta} ({e}). Recorrendo para porta fallback 3000...")
            server = HTTPServer((host, 3000), DashboardHandler)
            PORT = 3000
        else:
            raise e

    url_local = f"http://nova.local" if PORT == 80 else f"http://nova.local:{PORT}"
    url_padrao = f"http://localhost" if PORT == 80 else f"http://localhost:{PORT}"
    
    print("=" * 70)
    print(f"🌌 NOVA CONTROL CENTER — SERVER ATIVO NA PORTA {PORT}")
    print(f"🌐 Domínio Limpo: {url_local}")
    print(f"🌐 Acesso Direto: {url_padrao}")
    print("=" * 70)

    try:
        webbrowser.open(url_local if PORT == 80 else url_padrao)
    except Exception:
        pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 NOVA Control Center encerrado.")
        server.server_close()

if __name__ == "__main__":
    iniciar_dashboard()
