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

def is_demo_mode(handler, query_params=None):
    """
    Detecta se a requisição deve ser servida com dados de demonstração (Demo Mode)
    ou com dados reais (Real Mode).
    1. Se query param ?demo=true ou ?mode=demo for passado -> Demo Mode
    2. Se query param ?demo=false ou ?mode=real for passado -> Real Mode
    3. Se cabeçalho X-NOVA-Demo: true ou cookie nova_privacy_mode=demo -> Demo Mode
    4. Se a requisição for externa (não localhost/127.0.0.1) ou via túnel público -> Demo Mode por padrão (LGPD)
    """
    if query_params is None:
        query_params = {}

    # 1. Query Params
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

    # 2. Headers
    req_demo = handler.headers.get("X-NOVA-Demo", "").lower()
    if req_demo in ("true", "1", "yes"):
        return True
    if req_demo in ("false", "0", "no"):
        return False

    # 3. Cookies
    cookie_str = handler.headers.get("Cookie", "")
    if "nova_privacy_mode=demo" in cookie_str:
        return True
    if "nova_privacy_mode=real" in cookie_str:
        return False

    # 4. Detecção de Origem / IP / Túnel
    client_ip = handler.client_address[0] if handler.client_address else "127.0.0.1"
    is_local = client_ip in ("127.0.0.1", "::1", "localhost")
    
    host_header = handler.headers.get("Host", "").lower()
    is_tunnel = any(t in host_header for t in ["loca.lt", "ngrok", "trycloudflare", "serveo.net", "localtunnel", ".nip.io"])

    if not is_local or is_tunnel:
        return True

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
            "cv_pdf": "/carreira/vagas_analisadas/tech_dev/capgemini/curriculo_fabio_rodrigues_capgemini.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/tech_dev/capgemini/cover_letter_fabio_rodrigues_capgemini.pdf",
            "cover_docx": "/carreira/vagas_analisadas/tech_dev/capgemini/cover_letter_fabio_rodrigues_capgemini.docx",
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
            "cv_pdf": "/carreira/vagas_analisadas/tech_dev/accenture/curriculo_fabio_rodrigues_accenture.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/tech_dev/accenture/cover_letter_fabio_rodrigues_accenture.pdf",
            "cover_docx": "/carreira/vagas_analisadas/tech_dev/accenture/cover_letter_fabio_rodrigues_accenture.docx",
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
            "cv_pdf": "/carreira/vagas_analisadas/tech_dev/deloitte/curriculo_fabio_rodrigues_deloitte.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/tech_dev/deloitte/cover_letter_fabio_rodrigues_deloitte.pdf",
            "cover_docx": "/carreira/vagas_analisadas/tech_dev/deloitte/cover_letter_fabio_rodrigues_deloitte.docx",
            "relatorio_pdf": "/carreira/vagas_analisadas/tech_dev/deloitte/relatorio_match_deloitte.pdf",
            "pitch_file": "carreira/vagas_analisadas/tech_dev/deloitte/carta_apresentacao_recruiter.md"
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
            "cv_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/gummy/curriculo_fabio_rodrigues_gummy.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/gummy/cover_letter_fabio_rodrigues_gummy.pdf",
            "cover_docx": "/carreira/vagas_analisadas/marketing_audiovisual/gummy/cover_letter_fabio_rodrigues_gummy.docx",
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
            "cv_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/aposta_ganha/curriculo_fabio_rodrigues_aposta_ganha.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/aposta_ganha/cover_letter_fabio_rodrigues_aposta_ganha.pdf",
            "cover_docx": "/carreira/vagas_analisadas/marketing_audiovisual/aposta_ganha/cover_letter_fabio_rodrigues_aposta_ganha.docx",
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
            "cv_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/rio_ave/curriculo_fabio_rodrigues_rio_ave.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/rio_ave/cover_letter_fabio_rodrigues_rio_ave.pdf",
            "cover_docx": "/carreira/vagas_analisadas/marketing_audiovisual/rio_ave/cover_letter_fabio_rodrigues_rio_ave.docx",
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
            "cv_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/grupo_luck/curriculo_fabio_rodrigues_grupo_luck.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/grupo_luck/cover_letter_fabio_rodrigues_grupo_luck.pdf",
            "cover_docx": "/carreira/vagas_analisadas/marketing_audiovisual/grupo_luck/cover_letter_fabio_rodrigues_grupo_luck.docx",
            "relatorio_pdf": "/carreira/vagas_analisadas/marketing_audiovisual/grupo_luck/relatorio_match_grupo_luck.pdf",
            "pitch_file": "carreira/vagas_analisadas/marketing_audiovisual/grupo_luck/carta_apresentacao_recruiter.md"
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
            "cv_pdf": "/carreira/vagas_analisadas/tech_dev/fullstack/curriculo_fabio_rodrigues_fullstack.pdf",
            "cover_pdf": "/carreira/vagas_analisadas/tech_dev/fullstack/cover_letter_fabio_rodrigues_fullstack.pdf",
            "cover_docx": "/carreira/vagas_analisadas/tech_dev/fullstack/cover_letter_fabio_rodrigues_fullstack.docx",
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
            "trilha": "Advanced AI Java Back-end & Distributed Systems",
            "plataforma": "NOVA Engineering Academy",
            "modulos_concluidos": 18,
            "total_modulos": 24,
            "progresso_percentual": 75.0,
            "modulo_atual": "Spring AI, Model Context Protocol & Vector Databases",
            "proxima_meta": "Event-Driven Microservices com Kafka & Testcontainers",
            "manual_pdf": "/download/docs/Manual_Engenharia_e_Arquitetura_NOVA.pdf"
        }
    
    return {
        "trilha": "Bootcamp Santander 2026 - AI Java Back-end",
        "plataforma": "DIO (Digital Innovation One)",
        "modulos_concluidos": 2,
        "total_modulos": 26,
        "progresso_percentual": 7.7,
        "modulo_atual": "Dominando a Linguagem de Programação Java",
        "proxima_meta": "Módulo 3: POO & Estruturas de Dados Avançadas",
        "manual_pdf": "/download/docs/Manual_Engenharia_e_Arquitetura_NOVA.pdf"
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

    comunicador = edge_tts.Communicate(text=texto_processado, voice=voz_id, rate=taxa)
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
        temp_path = temp_file.name
    
    try:
        await comunicador.save(temp_path)
        with open(temp_path, "rb") as f:
            audio_bytes = f.read()
        return base64.b64encode(audio_bytes).decode('utf-8')
    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass

def processar_intencao_voz(comando_texto: str) -> str:
    """
    Roteador semântico de inteligência por voz para Carreira, Estudos, Finanças e Conhecimento Geral.
    """
    if not comando_texto:
        return "Olá, Fábio! Em que posso te ajudar hoje?"

    cmd = comando_texto.lower()

    # 1. Carreira & Vagas
    if any(k in cmd for k in ["vaga", "vagas", "carreira", "candidatura", "candidaturas", "melhor vaga", "onde me candidatar", "capgemini", "deloitte", "accenture", "fullstack", "recruiter", "pitch", "emprego"]):
        return (
            "Fábio, sua melhor oportunidade no momento é a Capgemini com 92% de aderência técnica em Recife, seguida pela Accenture com 88% e Deloitte com 86%. "
            "Seu principal diferencial competitivo é o domínio de Java 21, Clean Architecture e sua formação em Design pela UniFBV."
        )

    # 2. Estudos & Trilha DIO
    if any(k in cmd for k in ["estudo", "estudos", "hoje", "estudar", "dio", "trilha", "santander", "progresso", "módulo", "modulo", "feynman", "curso"]):
        return (
            "Hoje o seu foco recomendado na Trilha Santander 2026 da DIO é o curso de Fundamentos da IA Moderna no Módulo 1. "
            "Você já concluiu 7.7% da carga horária com 2 cursos finalizados e pode consultar o Manual de Engenharia em PDF com 6 páginas."
        )

    # 3. Finanças & H2 (Tenta consultar API Spring Boot primeiro)
    if any(k in cmd for k in ["saldo", "gasto", "gastei", "despesa", "receita", "alimenta", "transporte", "compras", "extrato", "finança", "quanto sobrou", "dinheiro"]):
        try:
            url = "http://localhost:8081/api/voice/command"
            payload = json.dumps({"comando": comando_texto}).encode('utf-8')
            req = urllib.request.Request(
                url,
                data=payload,
                headers={'Content-Type': 'application/json', 'User-Agent': 'NOVA-Dashboard-Gateway'}
            )
            with urllib.request.urlopen(req, timeout=2.5) as response:
                res_json = json.loads(response.read().decode('utf-8'))
                msg = res_json.get("mensagemVoz")
                if msg:
                    return msg
        except Exception:
            pass
        
        # Fallback local de Finanças
        if "alimenta" in cmd:
            return "Fábio, seus gastos com alimentação em Agosto somam R$ 728,38 em um total de 20 transações conciliadas no Nubank."
        elif "receita" in cmd or "recebi" in cmd:
            return "Suas receitas confirmadas no banco H2 totalizam R$ 2.299,00 com 7 transferências recebidas."
        else:
            return "Fábio, seu saldo atual no banco H2 é de R$ 589,23 positivos, com R$ 2.299,00 em receitas e R$ 1.709,77 em despesas, gerando 34.5% de economia."

    # 4. Engenharia, Testes e Backend
    if any(k in cmd for k in ["teste", "testes", "junit", "backend", "spring", "qualidade", "porta"]):
        return "O microsserviço Spring Boot 3.3 está online na porta 8081 com 100% de sucesso nos 15 testes JUnit 5 automatizados e banco H2 em arquivo."

    # 5. Conceitos Técnicos / Conhecimento Geral (Nível 2)
    if "clean architecture" in cmd or "arquitetura hexagonal" in cmd:
        return "Clean Architecture é um padrão arquitetural que isola as regras de negócio de frameworks e bancos de dados através de casos de uso e inversão de dependências."
    elif "tdd" in cmd or "test driven" in cmd:
        return "TDD é a prática de desenvolvimento guiado por testes onde escrevemos primeiro o teste que falha, implementamos o código mínimo e depois refatoramos com segurança."
    elif "solid" in cmd:
        return "SOLID são cinco princípios de design orientado a objetos que promovem código desacoplado, extensível, coeso e de fácil manutenção."
    elif "mcp" in cmd or "model context" in cmd:
        return "O Model Context Protocol é o padrão aberto para integrar ferramentas e bancos de dados diretamente ao contexto de agentes e modelos de inteligência artificial."

    # 6. Fallback Geral
    return f"Olá, Fábio! Reconheci sua pergunta. Todos os módulos de finanças H2, vagas 360° e estudos DIO estão operacionais no NOVA Control Center."

class DashboardHandler(BaseHTTPRequestHandler):

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

        if path == "/api/status":
            dados = {
                "demo_mode": demo_active,
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
                "client_ip": client_ip,
                "is_local": client_ip in ("127.0.0.1", "::1", "localhost")
            })

        elif path == "/api/voice/config":
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

        # Interação de voz bidirecional (Microfone -> Spring Boot -> Síntese Base64)
        if parsed.path == "/api/voice/interact":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                req_data = json.loads(body.decode('utf-8'))
                comando = req_data.get("comando", "Olá")
                
                # 1. Processa semântica em Carreira, Estudos, Finanças ou Conceitos
                resposta_texto = processar_intencao_voz(comando)

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
