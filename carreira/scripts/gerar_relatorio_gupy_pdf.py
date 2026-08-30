#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de Relatório Oficial de Avaliação Comportamental Gupy (PDF - 4 Páginas Exatas)
Mapeamento Psicométrico: Big Five + Future of Work (12 Dimensões)
Candidato: Fabio Andre | ID: ff953cd660cd40efa320383c725f2b2c
"""

import os
import sys
import json
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Paleta Executiva Moderna
PRIMARY_DARK = colors.HexColor("#0F172A")    # Slate 900
PRIMARY_BLUE = colors.HexColor("#1E40AF")    # Blue 800
SECONDARY_INDIGO = colors.HexColor("#4F46E5") # Indigo 600
ACCENT_CYAN = colors.HexColor("#0284C7")     # Sky 600
ACCENT_EMERALD = colors.HexColor("#059669")  # Emerald 600
ACCENT_AMBER = colors.HexColor("#D97706")    # Amber 600
ACCENT_ROSE = colors.HexColor("#E11D48")     # Rose 600
BG_LIGHT = colors.HexColor("#F8FAFC")        # Slate 50
BORDER_COLOR = colors.HexColor("#E2E8F0")    # Slate 200
TEXT_MUTED = colors.HexColor("#64748B")      # Slate 500
TEXT_MAIN = colors.HexColor("#1E293B")       # Slate 800

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # Header Top Bar
        self.setFillColor(colors.HexColor("#0F172A"))
        self.rect(0, 832, 595.27, 10, fill=True, stroke=False)
        
        self.setFillColor(colors.HexColor("#0284C7"))
        self.rect(0, 828, 595.27, 4, fill=True, stroke=False)
        
        # Header text
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))
        self.drawString(36, 816, "GUPY ASSESSMENTS — RELATÓRIO OFICIAL DE MAPEAMENTO COMPORTAMENTAL")
        self.drawRightString(595.27 - 36, 816, "ID: ff953cd660cd40efa320383c725f2b2c")
        
        # Bottom Line
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(36, 30, 595.27 - 36, 30)
        
        # Footer text
        self.setFont("Helvetica", 7.8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(36, 18, "Candidato: Fabio Andre | Modelo Psicométrico Científico (Big Five + Future of Work)")
        self.drawRightString(595.27 - 36, 18, f"Página {self._pageNumber} de {page_count}")
        self.restoreState()


def generate_charts(data, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. RADAR CHART (12 Dimensões)
    short_labels = [
        "Tecnologia", "Abertura", "Decisão Intuitiva", "Autodisciplina",
        "Decisão Racional", "Facilitação Interp.", "Amabilidade", "Assertividade",
        "Estabilidade Emoc.", "Iniciativa Indiv.", "Resiliência", "Extroversão"
    ]
    values = [d["percentile"] for d in data]
    
    num_vars = len(short_labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    
    values_radar = values + values[:1]
    angles_radar = angles + angles[:1]
    
    fig, ax = plt.subplots(figsize=(5.6, 5.6), subplot_kw=dict(polar=True), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#F8FAFC')
    
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    plt.xticks(angles, short_labels, color='#1E293B', size=8, weight='bold')
    ax.set_rlabel_position(0)
    plt.yticks([25, 50, 75, 100], ["25%", "50%", "75%", "100%"], color="#64748B", size=7)
    plt.ylim(0, 100)
    
    ax.grid(color='#CBD5E1', linestyle='--', linewidth=0.75, alpha=0.8)
    ax.spines['polar'].set_color('#94A3B8')
    
    ax.plot(angles_radar, values_radar, color='#4F46E5', linewidth=2.0, linestyle='solid')
    ax.fill(angles_radar, values_radar, color='#6366F1', alpha=0.32)
    
    for a, v in zip(angles, values):
        color = '#059669' if v >= 75 else ('#0284C7' if v >= 50 else ('#D97706' if v >= 25 else '#E11D48'))
        ax.plot(a, v, marker='o', markersize=5.5, color=color, markeredgecolor='#FFFFFF', markeredgewidth=1.0)
    
    plt.title("MAPA RADAR COMPORTAMENTAL (12 DIMENSÕES)", size=10.5, color='#0F172A', weight='bold', y=1.08)
    plt.tight_layout()
    radar_path = os.path.join(output_dir, "radar_chart.png")
    plt.savefig(radar_path, dpi=220, bbox_inches='tight')
    plt.close()
    
    # 2. BAR CHART BY CLUSTER
    fig, ax = plt.subplots(figsize=(8.0, 4.0), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    
    sorted_data = sorted(data, key=lambda x: x["percentile"])
    y_labels = [d["label"] for d in sorted_data]
    scores = [d["percentile"] for d in sorted_data]
    
    colors_list = []
    for s in scores:
        if s >= 75: colors_list.append('#059669')
        elif s >= 51: colors_list.append('#0284C7')
        elif s >= 26: colors_list.append('#D97706')
        else: colors_list.append('#E11D48')
    
    y_pos = np.arange(len(y_labels))
    bars = ax.barh(y_pos, scores, color=colors_list, height=0.58, edgecolor='#CBD5E1', linewidth=0.5)
    
    for bar, score in zip(bars, scores):
        ax.text(score + 1.2, bar.get_y() + bar.get_height()/2, f"{score}%", 
                va='center', ha='left', fontsize=7.5, weight='bold', color='#1E293B')
        
    ax.set_yticks(y_pos)
    ax.set_yticklabels(y_labels, fontsize=7.5, weight='bold', color='#1E293B')
    ax.set_xlim(0, 105)
    
    ax.axvline(25, color='#CBD5E1', linestyle=':', linewidth=1, alpha=0.8)
    ax.axvline(50, color='#94A3B8', linestyle='--', linewidth=1, alpha=0.8)
    ax.axvline(75, color='#CBD5E1', linestyle=':', linewidth=1, alpha=0.8)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#94A3B8')
    ax.spines['bottom'].set_color('#94A3B8')
    ax.set_xlabel("Percentil Comportamental Gupy (0 a 100%)", fontsize=8, color='#64748B', weight='bold', labelpad=5)
    
    plt.title("DISTRIBUIÇÃO DE PERCENTIS POR COMPETÊNCIA", size=10, color='#0F172A', weight='bold', pad=8)
    plt.tight_layout()
    bars_path = os.path.join(output_dir, "bars_chart.png")
    plt.savefig(bars_path, dpi=220, bbox_inches='tight')
    plt.close()
    
    return radar_path, bars_path


def build_pdf(json_data_path, output_pdf_path):
    with open(json_data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    charts_dir = "/tmp/gupy_charts"
    radar_img, bars_img = generate_charts(data, charts_dir)
    
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=34,
        rightMargin=34,
        topMargin=38,
        bottomMargin=38
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        "GupyTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=PRIMARY_DARK,
        spaceAfter=2
    )
    
    subtitle_style = ParagraphStyle(
        "GupySubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=TEXT_MUTED,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        "GupyBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.2,
        leading=9.8,
        textColor=TEXT_MAIN
    )
    
    story = []
    
    # ---------------------------------------------------------
    # PÁGINA 1: SUMÁRIO EXECUTIVO & VISÃO GERAL
    # ---------------------------------------------------------
    story.append(Paragraph("Mapeamento do Perfil Comportamental", title_style))
    story.append(Paragraph("<b>Candidato:</b> Fabio Andre &nbsp;|&nbsp; <b>ID da Avaliação:</b> ff953cd660cd40efa320383c725f2b2c &nbsp;|&nbsp; <b>Plataforma:</b> Gupy Assessments", subtitle_style))
    
    archetype_html = """
    <b>ARQUÉTIPO COMPORTAMENTAL: ESTRATEGISTA INOVADOR, TECNOLÓGICO & ANALÍTICO</b><br/>
    <font color="#475569" size="7.5">
    Perfil caracterizado por <b>altíssimo entusiasmo tecnológico (95%)</b>, forte capacidade de <b>inovação e abertura criativa (80%)</b>, equilíbrio entre <b>decisão intuitiva (80%) e racional (75%)</b>, alta <b>autodisciplina (75%)</b> e preferência por <b>ambientes de alta concentração individual (Extroversão 1% / Foco Profundo)</b>.
    </font>
    """
    archetype_table = Table(
        [[Paragraph(archetype_html, body_style)]],
        colWidths=[527]
    )
    archetype_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1.1, colors.HexColor("#3B82F6")),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(archetype_table)
    story.append(Spacer(1, 6))
    
    radar_image_flow = Image(radar_img, width=245, height=245)
    
    quadrant_html = """
    <b>QUADRANTE DE CLASSIFICAÇÃO GUPY:</b><br/><br/>
    <b>🟢 NÍVEL ALTO (76% a 100%):</b><br/>
    • Entusiasmo por Tecnologias: <b>95%</b> (Alto)<br/>
    • Abertura a Experiências: <b>80%</b> (Alto)<br/>
    • Estilo de Decisão Intuitivo: <b>80%</b> (Alto)<br/><br/>
    <b>🔵 NÍVEL MÉDIO-ALTO (51% a 75%):</b><br/>
    • Autodisciplina: <b>75%</b> (Médio-alto)<br/>
    • Estilo de Decisão Racional: <b>75%</b> (Médio-alto)<br/>
    • Facilitação Interpessoal: <b>65%</b> (Médio-alto)<br/>
    • Amabilidade: <b>65%</b> (Médio-alto)<br/><br/>
    <b>🟠 NÍVEL MÉDIO-BAIXO (26% a 50%):</b><br/>
    • Assertividade: <b>40%</b> (Médio-baixo)<br/>
    • Estabilidade Emocional: <b>30%</b> (Médio-baixo)<br/>
    • Iniciativa Individual: <b>30%</b> (Médio-baixo)<br/><br/>
    <b>🔴 NÍVEL BAIXO (1% a 25% - Foco & Preferência):</b><br/>
    • Resiliência a Estresse: <b>5%</b> (Baixo)<br/>
    • Extroversão (Foco Individual): <b>1%</b> (Baixo)
    """
    quadrant_table = Table(
        [[Paragraph(quadrant_html, body_style)]],
        colWidths=[255]
    )
    quadrant_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    
    grid_table = Table(
        [[radar_image_flow, quadrant_table]],
        colWidths=[255, 272]
    )
    grid_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(grid_table)
    story.append(Spacer(1, 6))
    
    bars_image_flow = Image(bars_img, width=527, height=195)
    story.append(bars_image_flow)
    
    # ---------------------------------------------------------
    # PÁGINA 2: CLUSTER 1 - BIG FIVE (TODAS AS 5 DIMENSÕES)
    # ---------------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("Cluster 1: Big Five — Traços Fundamentais de Personalidade", title_style))
    story.append(Paragraph("O modelo dos Cinco Grandes Fatores (Big Five) é o padrão ouro na psicologia científica para mapeamento de personalidade e padrões naturais de comportamento no trabalho.", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY_INDIGO, spaceBefore=1, spaceAfter=4))
    
    big_five_items = [d for d in data if d["key"] in ["OPENNESS_TO_EXPERIENCE", "CONSCIENTIOUSNESS", "AGREEABLENESS", "NEUROTICISM", "EXTROVERSION"]]
    
    for item in big_five_items:
        perc = item["percentile"]
        bg_badge = "#059669" if perc >= 76 else ("#0284C7" if perc >= 51 else ("#D97706" if perc >= 26 else "#E11D48"))
        
        card_header = f"""
        <table width="100%">
            <tr>
                <td width="70%"><b><font size="8.5" color="#0F172A">{item['label']}</font></b> &nbsp;|&nbsp; <font color="#64748B" size="7.2">Classificação: <b>{item['classification']}</b></font></td>
                <td width="30%" align="right"><font color="{bg_badge}" size="8"><b>PERCENTIL: {perc}%</b></font></td>
            </tr>
        </table>
        """
        
        # Keep text clean and compact
        desc_clean = item['description'].replace('\n', ' ')
        occ_clean = item['occupationArea'].replace('\n', ' ') if item['occupationArea'] else "Atividades compatíveis com o perfil analítico e criativo."
        
        content_html = f"""
        {card_header}
        <hr color="#CBD5E1" size="0.5"/>
        <font color="#334155" size="7.2"><b>Descrição Comportamental:</b> {desc_clean}</font><br/><br/>
        <font color="#1E40AF" size="7.2"><b>💼 Ambiente & Atividades Indicadas:</b> {occ_clean}</font>
        """
        
        card_t = Table([[Paragraph(content_html, body_style)]], colWidths=[527])
        card_t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
            ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
            ('LINELEFT', (0,0), (-1,-1), 3.5, colors.HexColor(bg_badge)),
            ('PADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(card_t)
        story.append(Spacer(1, 3.5))
        
    # ---------------------------------------------------------
    # PÁGINA 3: CLUSTER 2 - FUTURE OF WORK (TODAS AS 7 DIMENSÕES)
    # ---------------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("Cluster 2: Future of Work — Estilo de Decisão & Competências", title_style))
    story.append(Paragraph("Mapeamento das habilidades essenciais para a economia digital: velocidade tecnológica, raciocínio decisório, facilitação interpessoal, assertividade e resiliência.", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT_CYAN, spaceBefore=1, spaceAfter=4))
    
    fow_items = [d for d in data if d["key"] not in ["OPENNESS_TO_EXPERIENCE", "CONSCIENTIOUSNESS", "AGREEABLENESS", "NEUROTICISM", "EXTROVERSION"]]
    
    for item in fow_items:
        perc = item["percentile"]
        bg_badge = "#059669" if perc >= 76 else ("#0284C7" if perc >= 51 else ("#D97706" if perc >= 26 else "#E11D48"))
        
        card_header = f"""
        <table width="100%">
            <tr>
                <td width="70%"><b><font size="8.5" color="#0F172A">{item['label']}</font></b> &nbsp;|&nbsp; <font color="#64748B" size="7.2">Classificação: <b>{item['classification']}</b></font></td>
                <td width="30%" align="right"><font color="{bg_badge}" size="8"><b>PERCENTIL: {perc}%</b></font></td>
            </tr>
        </table>
        """
        
        desc_clean = item['description'].replace('\n', ' ')
        occ_clean = item['occupationArea'].replace('\n', ' ') if item['occupationArea'] else "Atividades com foco em entrega técnica e inovação."
        
        content_html = f"""
        {card_header}
        <hr color="#CBD5E1" size="0.5"/>
        <font color="#334155" size="7.2"><b>Descrição Comportamental:</b> {desc_clean}</font><br/><br/>
        <font color="#1E40AF" size="7.2"><b>💼 Ambiente & Atividades Indicadas:</b> {occ_clean}</font>
        """
        
        card_t = Table([[Paragraph(content_html, body_style)]], colWidths=[527])
        card_t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
            ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
            ('LINELEFT', (0,0), (-1,-1), 3.5, colors.HexColor(bg_badge)),
            ('PADDING', (0,0), (-1,-1), 3.5),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(card_t)
        story.append(Spacer(1, 2.5))

    # ---------------------------------------------------------
    # PÁGINA 4: GUIA ESTRATÉGICO PARA RECRUTADORES & LIDERANÇAS
    # ---------------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("Guia Estratégico para Recrutadores & Liderança", title_style))
    story.append(Paragraph("Diretrizes práticas de alocação, gestão de desempenho e maximização do potencial produtivo do candidato.", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY_DARK, spaceBefore=1, spaceAfter=6))
    
    guide_sections = [
        ("🌟 1. Principais Forças & Vantagens Competitivas", [
            ("Pioneirismo Tecnológico (Percentil 95%)", "Facilidade extrema para aprender, dominar e integrar novas tecnologias, softwares e ferramentas de IA no fluxo de trabalho."),
            ("Raciocínio Decisório Dual (Intuitivo 80% + Racional 75%)", "Capacidade rara de aliar intuição e visão criativa rápida com embasamento analítico, lógico e orientado a dados."),
            ("Criatividade & Abertura à Inovação (Percentil 80%)", "Excelente desempenho em projetos que demandam originalidade, quebra de padrões e proposição de soluções fora da caixa."),
            ("Autodisciplina & Organização (Percentil 75%)", "Comprometimento com métodos, atenção a detalhes complexos e disciplina para cumprir metas e diretrizes estabelecidas.")
        ], "#059669"),
        
        ("🎯 2. Ambiente de Trabalho Ideal", [
            ("Autonomia e Foco Profundo (Deep Work)", "Rendimento máximo em tarefas que permitem concentração individual sem interrupções frequentes ou sobrecarga de reuniões protocolares."),
            ("Clareza de Expectativas e Métricas", "Ambientes que definem com precisão o que é esperado, com metas transparentes e liberdade técnica para escolher as melhores ferramentas."),
            ("Cultura de Inovação & Experimentação", "Espaço para testar hipóteses, utilizar novas tecnologias e implementar melhorias contínuas sem burocracia excessiva.")
        ], "#0284C7"),
        
        ("💡 3. Recomendações Práticas para Gestores & Líderes", [
            ("Comunicação Direta & Canais Assíncronos", "Privilegiar alinhamentos objetivos e documentação assíncrona, respeitando o estilo focado e introspectivo do profissional."),
            ("Alocação em Desafios Complexos de Criação e Dados", "Aproveitar a combinação única de Design + Lógica para projetos de ponta (mídia paga, direção criativa, esteiras de automação e engenharia de software)."),
            ("Gestão de Carga e Prevenção de Estresse", "Manter um ambiente psicologicamente seguro e previsível para mitigar picos de ansiedade em transições muito abruptas.")
        ], "#4F46E5")
    ]
    
    for title, points, color_hex in guide_sections:
        points_html = "".join([f"• <b>{p[0]}:</b> {p[1]}<br/>" for p in points])
        sec_html = f"""
        <b><font size="8.5" color="{color_hex}">{title}</font></b><br/><br/>
        <font size="7.5" color="#334155">{points_html}</font>
        """
        sec_table = Table([[Paragraph(sec_html, body_style)]], colWidths=[527])
        sec_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
            ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
            ('LINELEFT', (0,0), (-1,-1), 3.5, colors.HexColor(color_hex)),
            ('PADDING', (0,0), (-1,-1), 6),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(sec_table)
        story.append(Spacer(1, 6))
        
    conclusion_html = """
    <b>SÍNTESE DO DIAGNÓSTICO PSICOMÉTRICO (GUPY ASSESSMENTS):</b><br/>
    O perfil de <b>Fabio Andre</b> destaca-se fortemente em papéis que exigem <b>integração tecnológica, pensamento estratégico-criativo e precisão técnica individual</b>. Possui equilíbrio ideal para carreiras que unem <b>Engenharia / Análise de Dados</b> e <b>Criação / Estratégia Visual</b>, com altíssima capacidade de entrega autônoma.
    """
    conclusion_table = Table([[Paragraph(conclusion_html, body_style)]], colWidths=[527])
    conclusion_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1.2, PRIMARY_DARK),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(conclusion_table)
    
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✅ Relatório Comportamental Gupy (4 Páginas Exatas) gerado com sucesso em: {output_pdf_path}")

if __name__ == "__main__":
    json_path = "/Users/fabioandre/.gemini/antigravity-ide/brain/d2b13c03-bb1d-4e4d-95dd-2b98ffea2c98/scratch/exact_gupy_fabio_data.json"
    output_pdf = "/Users/fabioandre/Downloads/nova:/carreira/base/relatorio_comportamental_gupy_fabio_andre.pdf"
    build_pdf(json_path, output_pdf)
