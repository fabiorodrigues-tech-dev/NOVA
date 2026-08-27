#!/usr/bin/env python3
"""
Gerador de Currículo, Cover Letter e Relatório de Match em PDF — Padrão Harvard Tech / Clean Modern (ReportLab)
Ecossistema NOVA - Módulo de Carreira & Motor Central de Gráficos

Suporta:
1. --type cv: Geração de Currículo ATS-friendly executivo.
2. --type cover_letter: Geração de Carta de Apresentação formal timbrada.
3. --type match_report: Geração de Relatório Visual de Match com gráficos integrados (chart_engine).
"""

import os
import sys
import re
import argparse
import tempfile
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether, Table, TableStyle, Image, PageBreak
)

# Adiciona o diretório scripts ao path para importar o chart_engine
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../scripts")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
try:
    import chart_engine
except ImportError:
    try:
        import scripts.chart_engine as chart_engine
    except ImportError:
        chart_engine = None

def strip_emojis_and_symbols(text: str) -> str:
    """Remove emojis, blocos geométricos e símbolos não-ASCII que quebram fontes padrão."""
    custom_symbols = [
        "■", "▪", "▫", "🔹", "🔸", "📍", "📧", "📱", "💼", "💻", "🚀", "🌌",
        "🎙️", "🎙", "🎓", "🎯", "🛠️", "🛠", "🔍", "⚡", "📅", "📝", "📊",
        "💡", "⚪", "🟢", "🟡", "❌", "🌟", "✨", "🔗", "⭐", "🏷️", "🏷", "🍩", "💰", "✉️"
    ]
    for sym in custom_symbols:
        text = text.replace(sym, "")

    emoji_pattern = re.compile(
        "["
        "\U0001F1E0-\U0001F1FF"
        "\U0001F300-\U0001F5FF"
        "\U0001F600-\U0001F64F"
        "\U0001F680-\U0001F6FF"
        "\U0001F700-\U0001F77F"
        "\U0001F780-\U0001F7FF"
        "\U0001F800-\U0001F8FF"
        "\U0001F900-\U0001F9FF"
        "\U0001FA00-\U0001FA6F"
        "\U0001FA70-\U0001FAFF"
        "\U00002702-\U000027B0"
        "\U000025A0-\U000025FF"
        "\U00002600-\U000026FF"
        "]+",
        flags=re.UNICODE
    )
    text = emoji_pattern.sub("", text)
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\|\s*\|', '|', text)
    text = re.sub(r'^\s*\|\s*', '', text)
    text = re.sub(r'\s*\|\s*$', '', text)
    return text.strip()

def clean_markdown_inline(text: str) -> str:
    """Converte formatação inline básica de markdown para tags HTML suportadas pelo ReportLab."""
    text = strip_emojis_and_symbols(text)
    # Links markdown [texto](url) -> link clicavel no PDF
    text = re.sub(r'\[([^\]]+)\]\((https?://[^\)]+)\)', r'<a href="\2"><font color="#2980B9"><u>\1</u></font></a>', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Negrito e Itálico combinados
    text = re.sub(r'\*\*\*([^\*]+)\*\*\*', r'<b><i>\1</i></b>', text)
    text = re.sub(r'___([^_]+)___', r'<b><i>\1</i></b>', text)
    # Negrito
    text = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__([^_]+)__', r'<b>\1</b>', text)
    # Itálico
    text = re.sub(r'\*([^\*]+)\*', r'<i>\1</i>', text)
    text = re.sub(r'_([^_]+)_', r'<i>\1</i>', text)
    # Código inline `code`
    text = re.sub(r'`([^`]+)`', r'<font face="Courier" color="#1a1a1a">\1</font>', text)
    return text.strip()

def parse_markdown_to_pdf(markdown_path: str, output_pdf_path: str):
    """
    Lê o arquivo Markdown de currículo e compila um PDF no padrão Harvard Tech.
    """
    if not os.path.exists(markdown_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {markdown_path}")

    with open(markdown_path, "r", encoding="utf-8") as f:
        content = f.read()

    os.makedirs(os.path.dirname(os.path.abspath(output_pdf_path)), exist_ok=True)

    margin = 42.5  # 15mm
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=margin,
        bottomMargin=margin
    )

    styles = getSampleStyleSheet()

    name_style = ParagraphStyle(
        'HarvardName',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#111111'),
        alignment=1,
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'HarvardSubtitle',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#2C3E50'),
        alignment=1,
        spaceAfter=3
    )

    contact_style = ParagraphStyle(
        'HarvardContact',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#555555'),
        alignment=1,
        spaceAfter=12
    )

    section_style = ParagraphStyle(
        'HarvardSection',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#1A2530'),
        spaceBefore=10,
        spaceAfter=3,
        keepWithNext=True
    )

    role_style = ParagraphStyle(
        'HarvardRole',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#111111'),
        spaceBefore=6,
        spaceAfter=1,
        keepWithNext=True
    )

    meta_style = ParagraphStyle(
        'HarvardMeta',
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#666666'),
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'HarvardBody',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#222222'),
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'HarvardBullet',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#222222'),
        leftIndent=11,
        firstLineIndent=-7,
        spaceAfter=3
    )

    lines = content.splitlines()
    story = []

    header_extracted = False
    i = 0
    while i < len(lines):
        line = lines[i]
        raw_line = line.strip()

        if not raw_line:
            i += 1
            continue

        if not header_extracted and raw_line.startswith("# "):
            name_text = clean_markdown_inline(raw_line[2:])
            story.append(Paragraph(name_text, name_style))

            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1

            if i < len(lines) and lines[i].strip().startswith("**"):
                sub_text = clean_markdown_inline(lines[i].strip())
                story.append(Paragraph(sub_text, subtitle_style))
                i += 1

            while i < len(lines) and not lines[i].strip():
                i += 1

            if i < len(lines) and ("@" in lines[i] or "|" in lines[i]):
                contact_text = clean_markdown_inline(lines[i].strip())
                story.append(Paragraph(contact_text, contact_style))
                i += 1

            story.append(HRFlowable(width="100%", thickness=1.0, color=colors.HexColor("#1A2530"), spaceAfter=8))
            header_extracted = True
            continue

        if raw_line.startswith("## "):
            sec_text = clean_markdown_inline(raw_line[3:]).upper()
            sec_heading = KeepTogether([
                Paragraph(sec_text, section_style),
                HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#BDC3C7"), spaceAfter=5)
            ])
            story.append(sec_heading)
            i += 1
            continue

        if raw_line.startswith("### "):
            role_text = clean_markdown_inline(raw_line[4:])
            story.append(Paragraph(role_text, role_style))
            i += 1
            continue

        if raw_line.startswith("*") and raw_line.endswith("*") and len(raw_line) < 100:
            meta_text = clean_markdown_inline(raw_line)
            story.append(Paragraph(meta_text, meta_style))
            i += 1
            continue

        if raw_line == "---":
            i += 1
            continue

        if raw_line.startswith("- ") or raw_line.startswith("• ") or (raw_line.startswith("* ") and not raw_line.endswith("*")):
            bullet_text = clean_markdown_inline(raw_line[2:].strip())
            formatted_bullet = f'<font color="#2C3E50">&bull;</font> {bullet_text}'
            story.append(Paragraph(formatted_bullet, bullet_style))
            i += 1
            continue

        p_text = clean_markdown_inline(raw_line)
        story.append(Paragraph(p_text, body_style))
        i += 1

    doc.build(story)
    print(f"✅ PDF de Currículo gerado com sucesso em: {output_pdf_path}")

def parse_cover_letter_to_pdf(markdown_path: str, output_pdf_path: str):
    """
    Converte o Markdown da Cover Letter em um documento PDF formal e timbrado.
    """
    if not os.path.exists(markdown_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {markdown_path}")

    with open(markdown_path, "r", encoding="utf-8") as f:
        content = f.read()

    os.makedirs(os.path.dirname(os.path.abspath(output_pdf_path)), exist_ok=True)

    margin = 42.5  # 15mm
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=margin,
        bottomMargin=margin
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CLTitle', fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=colors.HexColor('#1A2530'), spaceAfter=4)
    contact_style = ParagraphStyle('CLContact', fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor('#555555'), spaceAfter=2)
    recip_style = ParagraphStyle('CLRecip', fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=colors.HexColor('#1A2530'), spaceBefore=6, spaceAfter=3)
    body_style = ParagraphStyle('CLBody', fontName='Helvetica', fontSize=9, leading=13.5, textColor=colors.HexColor('#222222'), spaceAfter=6, alignment=4)
    num_style = ParagraphStyle('CLNum', fontName='Helvetica', fontSize=9, leading=13.5, textColor=colors.HexColor('#222222'), leftIndent=12, spaceAfter=4)
    sign_style = ParagraphStyle('CLSign', fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=colors.HexColor('#1A2530'), spaceBefore=6, spaceAfter=2)

    lines = content.splitlines()
    story = []
    header_done = False
    i = 0

    while i < len(lines):
        line = lines[i]
        raw_line = line.strip()

        if not raw_line or raw_line == "---":
            i += 1
            continue

        if not header_done and raw_line.startswith("# "):
            title_text = clean_markdown_inline(raw_line[2:])
            story.append(Paragraph(title_text, title_style))

            i += 1
            while i < len(lines) and lines[i].strip().startswith("**"):
                c_text = clean_markdown_inline(lines[i].strip())
                story.append(Paragraph(c_text, contact_style))
                i += 1

            story.append(Spacer(1, 4))
            story.append(HRFlowable(width="100%", thickness=1.0, color=colors.HexColor("#1A2530"), spaceAfter=10))
            header_done = True
            continue

        if raw_line.startswith("**À") or raw_line.startswith("**Assunto"):
            rec_text = clean_markdown_inline(raw_line)
            story.append(Paragraph(rec_text, recip_style))
            i += 1
            continue

        if re.match(r'^\d+\.\s+', raw_line):
            num_text = clean_markdown_inline(raw_line)
            story.append(Paragraph(num_text, num_style))
            i += 1
            continue

        if raw_line.startswith("Atenciosamente") or raw_line.startswith("**Fábio Rodrigues**"):
            s_text = clean_markdown_inline(raw_line)
            story.append(Paragraph(s_text, sign_style))
            i += 1
            continue

        p_text = clean_markdown_inline(raw_line)
        story.append(Paragraph(p_text, body_style))
        i += 1

    doc.build(story)
    print(f"✅ PDF da Cover Letter gerado em: {output_pdf_path}")

def parse_match_report_to_pdf(markdown_path: str, output_pdf_path: str):
    """
    Gera um Relatório de Match Técnico Executivo em PDF com gráficos do chart_engine embutidos.
    Suporta dinamicamente vagas de Tecnologia (Dev/TI) e de Marketing/Audiovisual/Criação.
    """
    if not os.path.exists(markdown_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {markdown_path}")

    with open(markdown_path, "r", encoding="utf-8") as f:
        content = f.read()

    os.makedirs(os.path.dirname(os.path.abspath(output_pdf_path)), exist_ok=True)

    # Extrai informações principais
    empresa_match = re.search(r'>\s*\*\*Empresa:\*\*\s*(.+)', content)
    empresa = empresa_match.group(1).strip() if empresa_match else "Empresa Alvo"

    vaga_match = re.search(r'#\s*🎯\s*Análise de Vaga & Match Técnico:\s*(.+)', content)
    if not vaga_match:
        vaga_match = re.search(r'#\s*(.+)', content)
    vaga_titulo = vaga_match.group(1).split("—")[0].strip() if vaga_match else "Analista / Especialista"

    score_match = re.search(r'SCORE DE ADERÊNCIA TÉCNICA:\s*(\d+)%', content)
    score_val = score_match.group(1) if score_match else "92"

    # 1. Parsing dinâmico de Competências / Skills
    import json
    skills_map = None
    skills_json_match = re.search(r'<!--\s*SKILLS_JSON:\s*(\{.+?\})\s*-->', content, re.DOTALL)
    if skills_json_match:
        try:
            skills_map = json.loads(skills_json_match.group(1))
        except Exception:
            skills_map = None

    if not skills_map:
        # Detecta se é perfil Marketing/Audiovisual ou Tech
        if any(k in content.lower() for k in ["endomarketing", "audiovisual", "filmmaker", "edição", "marketing", "conteúdo", "vídeo"]):
            skills_map = {
                'Design & Identidade Visual': (100, 95),
                'Pós-Produção & Edição de Vídeo': (100, 90),
                'Storytelling & Redação': (95, 90),
                'Comunicação Interna & CSC': (95, 90),
                'Employer Branding & Cultura': (90, 85),
                'Automação & IA Criativa': (100, 75),
                'Photoshop / Illustrator / Premiere': (100, 95),
                'Captação & Áudio / Foto': (90, 85)
            }
        else:
            skills_map = {
                'Java 21 / Spring Boot 3': (100, 100),
                'Clean Architecture / SOLID': (100, 95),
                'TDD (JUnit 5 / Mockito)': (100, 95),
                'Bancos Relacionais (SQL/ACID)': (95, 90),
                'APIs RESTful / Swagger': (95, 90),
                'Spring AI (MCP Server)': (100, 75),
                'TypeScript / Prototipagem': (90, 85),
                'Inglês Avançado': (95, 90)
            }

    # 2. Parsing dinâmico de Faixa Salarial
    sal_match = re.search(r'<!--\s*SALARIO:\s*([\d\.]+)\s*,\s*([\d\.]+)\s*,\s*([\d\.]+)\s*,\s*([\d\.]+)\s*-->', content)
    if sal_match:
        sal_min = float(sal_match.group(1))
        sal_med = float(sal_match.group(2))
        sal_pret = float(sal_match.group(3))
        sal_teto = float(sal_match.group(4))
    else:
        if any(k in content.lower() for k in ["endomarketing", "audiovisual", "filmmaker", "marketing"]):
            sal_min, sal_med, sal_pret, sal_teto = 3500.0, 4200.0, 4800.0, 6000.0
        else:
            sal_min, sal_med, sal_pret, sal_teto = 6500.0, 8500.0, 9000.0, 12000.0

    # 3. Parsing dinâmico de KPIs
    kpi_match = re.search(r'<!--\s*KPIS:\s*([^,]+)\s*,\s*([^,]+)\s*,\s*([^,]+)\s*,\s*([^,]+)\s*-->', content)
    if kpi_match:
        kpi3_title = kpi_match.group(1).strip()
        kpi3_val = kpi_match.group(2).strip()
        kpi4_title = kpi_match.group(3).strip()
        kpi4_val = kpi_match.group(4).strip()
    else:
        if any(k in content.lower() for k in ["endomarketing", "audiovisual", "filmmaker", "marketing"]):
            kpi3_title = "DESIGN & VÍDEO"
            kpi3_val = "100% Coberto"
            kpi4_title = "DIFERENCIAL IA"
            kpi4_val = "Automação / LLM"
        else:
            kpi3_title = "CORE BACKEND"
            kpi3_val = "100% Coberto"
            kpi4_title = "DIFERENCIAL IA"
            kpi4_val = "Spring AI / MCP"

    # 4. Parsing dinâmico de Parecer & Argumentos
    parecer_custom = []
    sec3_match = re.search(r'##\s*💼\s*3\.\s*Argumentos de Impacto[^\n]*\n([\s\S]+?)(?=\n##|\Z)', content)
    if sec3_match:
        raw_bullets = sec3_match.group(1).strip().splitlines()
        for b in raw_bullets:
            b = b.strip()
            if b.startswith("1.") or b.startswith("2.") or b.startswith("3.") or b.startswith("-"):
                # Limpa markdown e adiciona bullet
                cleaned_b = clean_markdown_inline(b)
                parecer_custom.append(f"&bull; {cleaned_b}")

    if not parecer_custom:
        parecer_custom = [
            f"&bull; <b>Alinhamento do Domínio:</b> O portfólio e histórico profissional cobrem plenamente os requisitos exigidos pela {empresa}.",
            f"&bull; <b>Vantagem Competitiva:</b> A união de formação em Design (UniFBV), maestria em produção audiovisual e domínio de ferramentas de IA posiciona o candidato no topo do processo seletivo.",
            f"&bull; <b>Recomendação de Abordagem:</b> Enviar currículo oficial compilado no padrão Harvard Tech/ATS, cover letter timbrada e realizar abordagem ativa com recrutadores e lideranças no LinkedIn."
        ]

    is_marketing = any(k in content.lower() for k in ["endomarketing", "audiovisual", "filmmaker", "edição", "marketing", "conteúdo", "vídeo", "luck"])

    # 1.1 Parsing dinâmico de Cases de Portfólio
    portfolio_cases = None
    port_json_match = re.search(r'<!--\s*PORTFOLIO_CASES:\s*(\{.+?\})\s*-->', content, re.DOTALL)
    if port_json_match:
        try:
            portfolio_cases = json.loads(port_json_match.group(1))
        except Exception:
            portfolio_cases = None

    if not portfolio_cases:
        portfolio_cases = {
            'Institucional & Obras (DER-PE)': 95,
            'Viral, Retenção & Humor (Gildo Lanches)': 96,
            'Collabs & Cultura Regional (Quintal dos Primos)': 92,
            'Processos Gráficos & B2B (Gráfica do Parque)': 90,
            'Motion Graphics & Comunidade (Unigames)': 88,
            'Inovação & Voice AI (Infinit Tecnologia)': 94
        }

    margin = 36  # ~12.7mm
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=margin,
        bottomMargin=margin
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('RepTitle', fontName='Helvetica-Bold', fontSize=15, leading=19, textColor=colors.HexColor('#1A2530'), alignment=1)
    subtitle_style = ParagraphStyle('RepSub', fontName='Helvetica', fontSize=9, leading=12, textColor=colors.HexColor('#5D6D7E'), alignment=1)
    sec_style = ParagraphStyle('RepSec', fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=colors.HexColor('#1A2530'), spaceBefore=6, spaceAfter=3)
    body_style = ParagraphStyle('RepBody', fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor('#2C3E50'))

    with tempfile.TemporaryDirectory() as tmpdir:
        chart_match_path = os.path.join(tmpdir, "match_chart.png")
        chart_sal_path = os.path.join(tmpdir, "salario_chart.png")
        chart_port_path = os.path.join(tmpdir, "portfolio_chart.png")

        if chart_engine:
            chart_engine.gerar_grafico_match(skills_map, chart_match_path)
            chart_engine.gerar_grafico_salario(sal_min, sal_med, sal_pret, sal_teto, chart_sal_path, cargo=vaga_titulo)
            if is_marketing and hasattr(chart_engine, 'gerar_grafico_portfolio_match'):
                chart_engine.gerar_grafico_portfolio_match(portfolio_cases, chart_port_path)

        story = []

        # Cabeçalho
        story.append(Paragraph(f"NOVA &bull; RELATÓRIO DE MATCH TÉCNICO & PORTFÓLIO", title_style))
        story.append(Paragraph(f"Vaga: <b>{vaga_titulo}</b> | Empresa: <b>{empresa}</b> | Match: <b>{score_val}%</b>", subtitle_style))
        story.append(Spacer(1, 4))
        story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#1A2530"), spaceAfter=6))

        # KPI Banner
        kpi_data = [
            [
                Paragraph("SCORE DE MATCH", ParagraphStyle('K1', fontName='Helvetica', fontSize=7.5, alignment=1, textColor=colors.HexColor('#5D6D7E'))),
                Paragraph("CLASSIFICAÇÃO", ParagraphStyle('K2', fontName='Helvetica', fontSize=7.5, alignment=1, textColor=colors.HexColor('#5D6D7E'))),
                Paragraph(kpi3_title, ParagraphStyle('K3', fontName='Helvetica', fontSize=7.5, alignment=1, textColor=colors.HexColor('#5D6D7E'))),
                Paragraph(kpi4_title, ParagraphStyle('K4', fontName='Helvetica', fontSize=7.5, alignment=1, textColor=colors.HexColor('#5D6D7E')))
            ],
            [
                Paragraph(f"<font color='#27AE60'><b>{score_val}%</b></font>", ParagraphStyle('V1', fontName='Helvetica-Bold', fontSize=12, alignment=1)),
                Paragraph("<b>Alta Aderência</b>", ParagraphStyle('V2', fontName='Helvetica-Bold', fontSize=10.5, alignment=1, textColor=colors.HexColor('#1A2530'))),
                Paragraph(f"<b>{kpi3_val}</b>", ParagraphStyle('V3', fontName='Helvetica-Bold', fontSize=10.5, alignment=1, textColor=colors.HexColor('#2980B9'))),
                Paragraph(f"<b>{kpi4_val}</b>", ParagraphStyle('V4', fontName='Helvetica-Bold', fontSize=10.5, alignment=1, textColor=colors.HexColor('#E67E22')))
            ]
        ]
        kpi_table = Table(kpi_data, colWidths=[130, 130, 130, 130])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F9F9')),
            ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#BDC3C7')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E8E8')),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        story.append(kpi_table)
        story.append(Spacer(1, 8))

        # Seção 1: Gráfico de Competências
        if os.path.exists(chart_match_path):
            story.append(Paragraph("<b>1. Análise Visual de Aderência por Competência</b>", sec_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#BDC3C7"), spaceAfter=5))
            story.append(Image(chart_match_path, width=520, height=210))
            story.append(Spacer(1, 6))

        # Seção 2: Gráfico Salarial
        if os.path.exists(chart_sal_path):
            story.append(Paragraph("<b>2. Posicionamento de Pretensão Salarial & Regime</b>", sec_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#BDC3C7"), spaceAfter=5))
            story.append(Image(chart_sal_path, width=520, height=130))
            story.append(Spacer(1, 6))

        if is_marketing:
            # Quebra para a Página 2 (Auditoria de Portfólio + Parecer)
            story.append(PageBreak())

            # Seção 3: Auditoria de Portfólio
            story.append(Paragraph("<b>3. Auditoria de Portfólio & Cases Recomendados</b>", sec_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#BDC3C7"), spaceAfter=5))

            if os.path.exists(chart_port_path):
                story.append(Image(chart_port_path, width=520, height=175))
                story.append(Spacer(1, 6))

            # Destaques dos Cases
            case_box_data = [
                [
                    Paragraph("<b>Case Institucional Recomendado (DER-PE):</b> Cobertura de obras rodoviárias e comunicação pública com rigor institucional. Demonstra capacidade técnica para alinhar diretrizes com a diretoria do CSC e produzir comunicados executivos de prestação de contas.", body_style)
                ],
                [
                    Paragraph("<b>Case de Engajamento Recomendado (Gildo Lanches):</b> Produção de vídeos dinâmicos de alta retenção (Reels/Shorts), ganchos visuais e Sound Design apurado. Demonstra habilidade para criar rituais de cultura vibrantes e engajar colaboradores das filiais.", body_style)
                ],
                [
                    Paragraph("<b>Link Oficial do Portfólio:</b> <a href='https://drive.google.com/file/d/1zPwDU9HHxqn5CoDZGHbq7KSjOfZfnOox/view'><font color='#2980B9'><u>https://drive.google.com/file/d/1zPwDU9HHxqn5CoDZGHbq7KSjOfZfnOox/view</u></font></a> (Final Cut Pro, Logic Pro, DaVinci Resolve, Mac M1 e iPhone 14 Pro Max em 4K ProRes).", body_style)
                ]
            ]
            case_table = Table(case_box_data, colWidths=[520])
            case_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F9F9')),
                ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#BDC3C7')),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E8E8')),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(case_table)
            story.append(Spacer(1, 8))

            # Seção 4: Parecer & Argumentos
            story.append(Paragraph("<b>4. Parecer Estratégico & Argumentos de Entrevista</b>", sec_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#BDC3C7"), spaceAfter=5))
            for p_item in parecer_custom[:4]:
                story.append(Paragraph(p_item, body_style))
                story.append(Spacer(1, 3))
        else:
            # Tech: Seção 3 Parecer
            story.append(Paragraph("<b>3. Parecer Estratégico & Argumentos de Entrevista</b>", sec_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#BDC3C7"), spaceAfter=5))
            for p_item in parecer_custom[:4]:
                story.append(Paragraph(p_item, body_style))
                story.append(Spacer(1, 3))

        doc.build(story)
        print(f"✅ Relatório Visual de Match gerado com sucesso em: {output_pdf_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Conversor de Currículo e Relatórios de Carreira em PDF (NOVA)")
    parser.add_argument("--type", choices=["cv", "match_report", "cover_letter"], default="cv", help="Tipo de documento a gerar (cv, match_report ou cover_letter)")
    parser.add_argument("--input", default="carreira/base/curriculo_base.md", help="Caminho do arquivo markdown de entrada")
    parser.add_argument("--output", default="carreira/base/pdf/curriculo_fabio_rodrigues_pt.pdf", help="Caminho do arquivo PDF de saída")

    args = parser.parse_args()
    if args.type == "match_report":
        parse_match_report_to_pdf(args.input, args.output)
    elif args.type == "cover_letter":
        parse_cover_letter_to_pdf(args.input, args.output)
    else:
        parse_markdown_to_pdf(args.input, args.output)
