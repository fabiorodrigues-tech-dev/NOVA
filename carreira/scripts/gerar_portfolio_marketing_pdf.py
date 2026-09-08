#!/usr/bin/env python3
"""
Gerador de Portfólio Executivo de Marketing Estratégico, Audiovisual & Design em PDF
Módulo de Carreira & Motor Central de Gráficos

Dossiê visual executivo de 3 páginas devidamente preenchidas e diagramadas:
- Página 1: Capa Executiva, Perfil Estratégico, KPIs Globais e Tabela Síntese dos 6 Cases Reais.
- Página 2: TODOS os 6 Cases Reais Unificados com cards nobres, links diretos e métricas.
- Página 3: Engenharia de Campanhas & E-mail Responsivo, Gráficos Ampliados, Especificações Técnicas e Matriz de Ferramentas.
100% livre de marca d'água NOVA, sem blocos pretos e sem menção ao LinkedIn.
"""

import os
import sys
import tempfile
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, Image, PageBreak
)
from reportlab.pdfgen import canvas

# Paleta Visual Corporativa
C_PRIMARY = colors.HexColor("#1A2530")     # Navy Escuro
C_SECONDARY = colors.HexColor("#2C3E50")   # Charcoal
C_ACCENT_BLUE = colors.HexColor("#2980B9") # Azul Royal
C_ACCENT_PURPLE = colors.HexColor("#6C5CE7")# Roxo Moderno
C_ACCENT_GREEN = colors.HexColor("#27AE60")# Verde Sucesso
C_ACCENT_ORANGE = colors.HexColor("#E67E22")# Laranja Alerta
C_MUTED = colors.HexColor("#7F8C8D")       # Cinza Médio
C_LIGHT_BG = colors.HexColor("#F8F9FA")    # Fundo Suave
C_BORDER = colors.HexColor("#CBD5E1")      # Borda Estruturada
C_CARD_HEADER = colors.HexColor("#E2E8F0") # Header Card Sólido
C_WHITE = colors.white

DRIVE_PORTFOLIO_URL = "https://drive.google.com/drive/folders/1fhmqNSZG9h7Tv4pFzqysuuBcIY4Sw-ri?usp=share_link"

class NumberedCanvas(canvas.Canvas):
    """Canvas com numeração total de páginas e cabeçalho/rodapé executivo sem marca d'água NOVA."""
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
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))

        # Cabeçalho a partir da página 2
        if self._pageNumber > 1:
            self.drawString(38, 815, "FÁBIO RODRIGUES  |  PORTFÓLIO DE MARKETING ESTRATÉGICO, AUDIOVISUAL & DESIGN")
            self.setStrokeColor(C_BORDER)
            self.setLineWidth(0.6)
            self.line(38, 808, 557, 808)

        # Rodapé em todas as páginas
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.6)
        self.line(38, 36, 557, 36)
        self.setFont("Helvetica", 7.5)
        self.drawString(38, 24, "Fábio Rodrigues  •  Recife/PE  •  fabioandre777@gmail.com  •  (81) 98992-0040")
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(557, 24, page_str)
        self.restoreState()

def gerar_grafico_email_benchmark(output_path: str):
    """Gera gráfico comparativo de performance de E-mail Marketing vs Mercado."""
    metrics = ['Taxa de Abertura', 'Cliques (CTR)', 'Entregabilidade']
    fabio_perf = [38.4, 6.2, 99.2]
    market_avg = [21.5, 2.6, 95.0]

    x = np.arange(len(metrics))
    width = 0.32

    fig, ax = plt.subplots(figsize=(3.5, 2.1), dpi=300)
    rects1 = ax.bar(x - width/2, market_avg, width, label='Média Mercado', color="#BDC3C7", alpha=0.7)
    rects2 = ax.bar(x + width/2, fabio_perf, width, label='Fábio Rodrigues', color="#2980B9")

    ax.set_ylabel('Porcentagem (%)', fontsize=7.5, fontweight='bold', color="#2C3E50")
    ax.set_title('E-mail Marketing vs Benchmarks Globais', fontsize=8.5, fontweight='bold', color="#1A2530", pad=6)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=7.5, fontweight='medium')
    ax.legend(loc='upper left', fontsize=7, frameon=True, facecolor="#F8F9FA", edgecolor="#BDC3C7")
    ax.set_ylim(0, 115)
    ax.grid(axis='y', linestyle='--', alpha=0.4)

    for rect in rects1:
        h = rect.get_height()
        ax.annotate(f'{h}%', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 1.5),
                    textcoords="offset points", ha='center', va='bottom', fontsize=6.8, color="#7F8C8D")

    for rect in rects2:
        h = rect.get_height()
        ax.annotate(f'{h}%', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 1.5),
                    textcoords="offset points", ha='center', va='bottom', fontsize=7.2, fontweight='bold', color="#1A2530")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def gerar_grafico_ab_uplift(output_path: str):
    """Gera gráfico de barras horizontais com os uplifts de Testes A/B."""
    tests = ['Assunto (Open Rate)', 'Posição CTA (Clicks)', 'Layout (Mobile)', 'Custo/Lead (CPL)']
    uplifts = [42.0, 28.5, 35.0, 18.0]
    cores = ['#27AE60', '#2980B9', '#6C5CE7', '#E67E22']

    fig, ax = plt.subplots(figsize=(3.5, 2.1), dpi=300)
    y_pos = np.arange(len(tests))

    bars = ax.barh(y_pos, uplifts, height=0.45, color=cores)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(tests, fontsize=7.5, fontweight='medium')
    ax.invert_yaxis()
    ax.set_xlabel('Otimização / Ganho (%)', fontsize=7.5, fontweight='bold', color="#2C3E50")
    ax.set_title('Uplifts de Testes A/B & Conversão', fontsize=8.5, fontweight='bold', color="#1A2530", pad=6)
    ax.set_xlim(0, 52)
    ax.grid(axis='x', linestyle='--', alpha=0.4)

    for bar in bars:
        w = bar.get_width()
        ax.text(w + 1.0, bar.get_y() + bar.get_height()/2, f'+{w:.1f}%' if w != 18.0 else f'-{w:.1f}%',
                ha='left', va='center', fontsize=7, fontweight='bold', color="#1A2530")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def criar_card_kpi(titulo: str, valor: str, subtitulo: str, cor_destaque="#2980B9"):
    """Cria um card visual de KPI com destaque estético."""
    styles = getSampleStyleSheet()
    t_style = ParagraphStyle('KPITitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.2, textColor=colors.HexColor("#64748B"), alignment=1)
    v_style = ParagraphStyle('KPIVal', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=13.5, textColor=colors.HexColor(cor_destaque), alignment=1, spaceBefore=1.5, spaceAfter=1.5)
    s_style = ParagraphStyle('KPISub', parent=styles['Normal'], fontName='Helvetica', fontSize=6.5, textColor=colors.HexColor("#334155"), alignment=1)

    p_title = Paragraph(titulo.upper(), t_style)
    p_val = Paragraph(valor, v_style)
    p_sub = Paragraph(subtitulo, s_style)

    tbl = Table([[p_title], [p_val], [p_sub]], colWidths=[124])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 0.8, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    return tbl

def gerar_portfolio_pdf(output_pdf_path: str):
    os.makedirs(os.path.dirname(os.path.abspath(output_pdf_path)), exist_ok=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        chart_email_path = os.path.join(tmpdir, "chart_email.png")
        chart_ab_path = os.path.join(tmpdir, "chart_ab.png")

        gerar_grafico_email_benchmark(chart_email_path)
        gerar_grafico_ab_uplift(chart_ab_path)

        doc = SimpleDocTemplate(
            output_pdf_path,
            pagesize=A4,
            leftMargin=38,
            rightMargin=38,
            topMargin=38,
            bottomMargin=42
        )

        styles = getSampleStyleSheet()

        h1_style = ParagraphStyle('H1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10.5, textColor=C_PRIMARY, leading=13.5, spaceBefore=5, spaceAfter=3)
        body_style = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=7.6, textColor=C_SECONDARY, leading=10.5)
        body_bold = ParagraphStyle('BodyBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.6, textColor=C_PRIMARY, leading=10.5)
        meta_style = ParagraphStyle('DocMeta', parent=styles['Normal'], fontName='Helvetica', fontSize=7.8, textColor=C_SECONDARY, leading=10.5)

        story = []

        # ==========================================
        # PÁGINA 1: CAPA EXECUTIVA, PERFIL, KPIS & SÍNTESE
        # ==========================================
        banner_data = [
            [
                Paragraph("<b>PORTFÓLIO EXECUTIVO 360°</b><br/><font size=14 color='#FFFFFF'><b>Marketing Estratégico, Audiovisual & Design</b></font>", ParagraphStyle('BannerH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#AED6F1"), leading=16)),
                Paragraph("<b>FÁBIO RODRIGUES</b><br/><font size=7.5 color='#E2E8F0'>Bacharel em Design (UniFBV)<br/>Recife - PE | (81) 98992-0040<br/>fabioandre777@gmail.com</font>", ParagraphStyle('BannerMeta', parent=styles['Normal'], fontName='Helvetica', fontSize=8.2, textColor=C_WHITE, leading=10.5, alignment=2))
            ]
        ]
        banner_tbl = Table(banner_data, colWidths=[340, 179])
        banner_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), C_PRIMARY),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(banner_tbl)
        story.append(Spacer(1, 6))

        # Link Oficial do Portfólio (Sem LinkedIn e sem marca d'água NOVA)
        links_data = [[
            Paragraph(f"<b>Portfólio Oficial no Google Drive:</b> <a href='{DRIVE_PORTFOLIO_URL}'><font color='#2980B9'><u>drive.google.com/drive/folders/1fhmqNSZG9h7Tv4pFzqysuuBcIY4Sw-ri?usp=share_link</u></font></a>", meta_style)
        ]]
        links_tbl = Table(links_data, colWidths=[519])
        links_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), C_LIGHT_BG),
            ('BOX', (0,0), (-1,-1), 0.7, C_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(links_tbl)
        story.append(Spacer(1, 6))

        # Perfil Profissional
        story.append(Paragraph("<b>1. Perfil Profissional & Diferencial Multidisciplinar</b>", h1_style))
        story.append(HRFlowable(width="100%", thickness=0.8, color=C_ACCENT_BLUE, spaceAfter=4))
        story.append(Paragraph(
            "Graduado em <b>Design pela Faculdade Boa Viagem (UniFBV)</b> com sólida atuação como <b>Gestor de Marketing, Diretor Criativo e Filmmaker</b>. Diferencial competitivo único fundamentado na convergência entre: <b>(1) Direção de Arte e Design Systems no Figma/Canva/Adobe</b>; <b>(2) Audiovisual cinematográfico em Apple Silicon M1 (Final Cut Pro, CapCut e Sound Design no Logic Pro)</b>; <b>(3) Codificação de E-mails Responsivos em HTML/CSS</b> com testes multiplataforma; e <b>(4) Produção Gráfica Industrial e Marketing Analytics orientado a ROI</b>.",
            body_style
        ))
        story.append(Spacer(1, 6))

        # Cards de KPIs Globais (Case 1 com +40.000+ views)
        kpi1 = criar_card_kpi("Collab Recife Ord.", "+40k", "Views Orgânicas (Dia do Sorvete)", "#2980B9")
        kpi2 = criar_card_kpi("Viralidade TikTok", "+6.140", "Curtidas Orgânicas (Gildo Lanches)", "#27AE60")
        kpi3 = criar_card_kpi("Open Rate E-mail", "38.4%", "Abertura (+78% vs benchmark)", "#6C5CE7")
        kpi4 = criar_card_kpi("SLA Gráfica & Mala", "100%", "No Prazo / 0% Retrabalho", "#E67E22")

        kpis_row = Table([[kpi1, kpi2, kpi3, kpi4]], colWidths=[129, 129, 129, 129])
        kpis_row.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('LEFTPADDING', (0,0), (-1,-1), 1),
            ('RIGHTPADDING', (0,0), (-1,-1), 1),
        ]))
        story.append(kpis_row)
        story.append(Spacer(1, 8))

        # Tabela Síntese dos 6 Cases Reais
        story.append(Paragraph("<b>2. Síntese dos 6 Cases Reais em Destaque no Portfólio</b>", h1_style))
        story.append(HRFlowable(width="100%", thickness=0.8, color=C_ACCENT_BLUE, spaceAfter=4))

        cases_summary_data = [
            [
                Paragraph("<b>Caso / Empresa</b>", ParagraphStyle('TH', parent=body_bold, textColor=C_WHITE, fontSize=7.8)),
                Paragraph("<b>Ação & Escopo Metodológico</b>", ParagraphStyle('TH', parent=body_bold, textColor=C_WHITE, fontSize=7.8)),
                Paragraph("<b>Impacto & Métricas</b>", ParagraphStyle('TH', parent=body_bold, textColor=C_WHITE, fontSize=7.8))
            ],
            [
                Paragraph("<b>Case 1: Quintal dos Primos</b>", body_bold),
                Paragraph("Collab Dia do Sorvete com <b>Recife Ordinário</b> (Rafa), direção criativa e roteiro de alta retenção.", body_style),
                Paragraph("<b>+40.000+</b> views orgânicas / <b>100%</b> ocupação no fim de semana", body_style)
            ],
            [
                Paragraph("<b>Case 2: Gildo Lanches</b>", body_bold),
                Paragraph("Vídeos verticais de Food Appeal, captação 4K, cortes rápidos e <b>Sound Design no Logic Pro</b>.", body_style),
                Paragraph("<b>+6.140</b> curtidas orgânicas no TikTok / <b>68%</b> completion", body_style)
            ],
            [
                Paragraph("<b>Case 3: Infinit (FuturePrint)</b>", body_bold),
                Paragraph("Cobertura corporativa nacional em tempo real na feira Expo Center Norte SP (edição *same-day*).", body_style),
                Paragraph("<b>+120</b> leads B2B qualificados gerados na feira", body_style)
            ],
            [
                Paragraph("<b>Case 4: DER-PE / Wolf</b>", body_bold),
                Paragraph("Audiovisual institucional e transparência de obras rodoviárias públicas governamentais.", body_style),
                Paragraph("<b>100%</b> de conformidade e aprovação governamental", body_style)
            ],
            [
                Paragraph("<b>Case 5: Gráfica do Parque & Unigames</b>", body_bold),
                Paragraph("Fechamento técnico PDF/X-1a, CMYK 300 DPI, mala direta e sinalização de varejo/PDV.", body_style),
                Paragraph("<b>0%</b> erro gráfico / <b>100%</b> pontualidade de entrega", body_style)
            ],
            [
                Paragraph("<b>Case 6: Olimac PE & Wolf</b>", body_bold),
                Paragraph("Branding 360°, Brand Guidelines e bibliotecas de Design System no Figma e Canva Pro.", body_style),
                Paragraph("<b>3x</b> mais agilidade / Consistência em 100% dos canais", body_style)
            ]
        ]
        cases_tbl = Table(cases_summary_data, colWidths=[130, 249, 140])
        cases_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
            ('BOX', (0,0), (-1,-1), 0.7, C_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_LIGHT_BG]),
            ('TOPPADDING', (0,0), (-1,-1), 3.8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3.8),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(cases_tbl)

        story.append(PageBreak())

        # ==========================================
        # PÁGINA 2: TODOS OS 6 CASES REAIS UNIFICADOS (CASES 1 A 6)
        # ==========================================
        story.append(Paragraph("<b>3. Detalhamento Executivo dos 6 Cases Reais (Cases 1 a 6)</b>", h1_style))
        story.append(HRFlowable(width="100%", thickness=0.8, color=C_ACCENT_BLUE, spaceAfter=4))

        # CASE 1
        case1_box_data = [
            [Paragraph("<b>CASE 1: COLLAB ESTRATÉGICA COM RECIFE ORDINÁRIO — QUINTAL DOS PRIMOS</b>", ParagraphStyle('CH', parent=body_bold, textColor=C_PRIMARY, fontSize=8.2))],
            [Paragraph(
                "<b>Contexto & Ação:</b> Campanha de marketing de influência para o <i>'Dia do Sorvete'</i> no <b>Quintal dos Primos</b>, co-produzida com o <b>Recife Ordinário</b>. O vídeo contou com apresentação de <b>Rafa</b> em entrevista com a diretoria, apresentando a sobremesa exclusiva.<br/>"
                "<b>Atuação de Fábio Rodrigues:</b> Como <b>Gerente Geral & Gestor de Marketing</b>, conduziu a direção criativa, idealizou o roteiro com gancho de alta retenção, planejou a infraestrutura operacional e alinhou a distribuição de mídia conjunta.<br/>"
                "<b>Link do Reel no Instagram:</b> <a href='https://www.instagram.com/quintal_dos_primos_/reel/Cxig4_xKxpN/'><font color='#2980B9'><u>instagram.com/quintal_dos_primos_/reel/Cxig4_xKxpN/</u></font></a> &nbsp;&nbsp;|&nbsp;&nbsp; <b>Impacto:</b> <b>+40.000+ views orgânicas</b> e <b>100% de ocupação</b> no final de semana.",
                body_style
            )]
        ]
        case1_tbl = Table(case1_box_data, colWidths=[519])
        case1_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), C_CARD_HEADER),
            ('BACKGROUND', (0,1), (-1,-1), C_WHITE),
            ('BOX', (0,0), (-1,-1), 0.7, C_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(case1_tbl)
        story.append(Spacer(1, 4))

        # CASE 2
        case2_box_data = [
            [Paragraph("<b>CASE 2: VIRALIDADE, FOOD APPEAL & SOUND DESIGN — GILDO LANCHES & WOLF</b>", ParagraphStyle('CH', parent=body_bold, textColor=C_PRIMARY, fontSize=8.2))],
            [Paragraph(
                "<b>Contexto & Ação:</b> Conteúdos verticais de altíssimo dinamismo e apelo visual (<i>food porn / food appeal</i>) para a tradicional hamburgueria <b>Gildo Lanches</b>, explorando cortes sincronizados com a trilha e micro-detalhes de preparação.<br/>"
                "<b>Atuação de Fábio Rodrigues:</b> Direção de cena e captação 4K com iluminação de estúdio; montagem acelerada no <b>Final Cut Pro</b> e <b>CapCut Pro</b>; e pós-produção de áudio imersiva no <b>Logic Pro</b> com efeitos ASMR de chapa, queijo derretido e texturas crocantes.<br/>"
                "<b>Link Instagram Reel:</b> <a href='https://www.instagram.com/gildolanchespe/reel/DTtNBIjDULw/'><font color='#2980B9'><u>instagram.com/gildolanchespe/reel/DTtNBIjDULw/</u></font></a> &nbsp;|&nbsp; <b>TikTok Viral:</b> <a href='https://www.tiktok.com/@wolfprintdesign/video/7501065386398403846'><font color='#2980B9'><u>tiktok.com/@wolfprintdesign/video/7501065386398403846</u></font></a> &nbsp;|&nbsp; <b>Impacto:</b> <b>+6.140 curtidas TikTok</b> e <b>68%</b> completion.",
                body_style
            )]
        ]
        case2_tbl = Table(case2_box_data, colWidths=[519])
        case2_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), C_CARD_HEADER),
            ('BACKGROUND', (0,1), (-1,-1), C_WHITE),
            ('BOX', (0,0), (-1,-1), 0.7, C_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(case2_tbl)
        story.append(Spacer(1, 4))

        # CASE 3
        case3_box_data = [
            [Paragraph("<b>CASE 3: COBERTURA CORPORATIVA NACIONAL — INFINIT NA FUTUREPRINT 2026 SP</b>", ParagraphStyle('CH', parent=body_bold, textColor=C_PRIMARY, fontSize=8.2))],
            [Paragraph(
                "<b>Contexto & Ação:</b> Cobertura audiovisual em tempo real da participação da <b>Infinit Tecnologia</b> na <b>FuturePrint 2026</b> (Expo Center Norte, São Paulo/SP) — maior feira de impressão digital, serigrafia e comunicação visual da América Latina.<br/>"
                "<b>Atuação de Fábio Rodrigues:</b> Produção executiva completa no pavilhão da feira; captação dinâmica de estande e maquinário industrial; entrevistas com clientes e parceiros; e edição ágil <i>same-day</i> no <b>Final Cut Pro</b> para publicação diária nas redes.<br/>"
                "<b>Impacto Institucional B2B:</b> Posicionamento de liderança nacional &nbsp;|&nbsp; <b>Métrica:</b> <b>+120 leads B2B qualificados</b> gerados durante o evento.",
                body_style
            )]
        ]
        case3_tbl = Table(case3_box_data, colWidths=[519])
        case3_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), C_CARD_HEADER),
            ('BACKGROUND', (0,1), (-1,-1), C_WHITE),
            ('BOX', (0,0), (-1,-1), 0.7, C_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(case3_tbl)
        story.append(Spacer(1, 4))

        # CASE 4
        case4_box_data = [
            [Paragraph("<b>CASE 4: AUDIOVISUAL INSTITUCIONAL & OBRAS PÚBLICAS — DER-PE / WOLF AGENCY</b>", ParagraphStyle('CH', parent=body_bold, textColor=C_PRIMARY, fontSize=8.2))],
            [Paragraph(
                "<b>Contexto & Ação:</b> Documentação audiovisual institucional e prestação de contas de obras rodoviárias estaduais para o <b>Departamento de Estradas de Rodagem de Pernambuco (DER-PE)</b>, através da <b>Wolf Agency</b>.<br/>"
                "<b>Atuação de Fábio Rodrigues:</b> Captação técnica em campo em frentes de pavimentação, terraplanagem e sinalização; edição de relatórios em vídeo e peças informativas para redes sociais unindo rigor técnico, transparência governamental e linguagem acessível ao cidadão.<br/>"
                "<b>Conformidade Governamental:</b> <b>100% de conformidade técnica e editorial</b> &nbsp;|&nbsp; Alcance estadual com prestação de contas transparente.",
                body_style
            )]
        ]
        case4_tbl = Table(case4_box_data, colWidths=[519])
        case4_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), C_CARD_HEADER),
            ('BACKGROUND', (0,1), (-1,-1), C_WHITE),
            ('BOX', (0,0), (-1,-1), 0.7, C_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(case4_tbl)
        story.append(Spacer(1, 4))

        # CASE 5
        case5_box_data = [
            [Paragraph("<b>CASE 5: PRODUÇÃO GRÁFICA, MALA DIRETA & VAREJO — GRÁFICA DO PARQUE & UNIGAMES</b>", ParagraphStyle('CH', parent=body_bold, textColor=C_PRIMARY, fontSize=8.2))],
            [Paragraph(
                "<b>Contexto & Atuação:</b> Projetos de engenharia gráfica editorial e mala direta de alta tiragem para a <b>Gráfica do Parque</b> e sinalização/PDV para a <b>Unigames</b>. Fechamento de arquivos em <b>PDF/X-1a</b> (CMYK, 300 DPI, sangria 3mm e facas especiais); seleção de papéis (Couché 300g, Offset 120g) e acabamentos nobres (Verniz UV Localizado, Soft Touch); além de vídeos da indústria gráfica.<br/>"
                "<b>Link Reel Gráfica:</b> <a href='https://www.instagram.com/graficadoparque/reel/DKSCxNSN776/'><font color='#2980B9'><u>instagram.com/graficadoparque/reel/DKSCxNSN776/</u></font></a> &nbsp;|&nbsp; <b>Link PDV Unigames:</b> <a href='https://www.instagram.com/asafeuni/p/DLYdqDtxHV1/'><font color='#2980B9'><u>instagram.com/asafeuni/p/DLYdqDtxHV1/</u></font></a> &nbsp;|&nbsp; <b>Impacto:</b> <b>0% erro gráfico</b> e <b>100% pontualidade</b>.",
                body_style
            )]
        ]
        case5_tbl = Table(case5_box_data, colWidths=[519])
        case5_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), C_CARD_HEADER),
            ('BACKGROUND', (0,1), (-1,-1), C_WHITE),
            ('BOX', (0,0), (-1,-1), 0.7, C_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(case5_tbl)
        story.append(Spacer(1, 4))

        # CASE 6
        case6_box_data = [
            [Paragraph("<b>CASE 6: BRANDING 360°, DESIGN SYSTEMS & IDENTIDADE — OLIMAC PE & WOLF</b>", ParagraphStyle('CH', parent=body_bold, textColor=C_PRIMARY, fontSize=8.2))],
            [Paragraph(
                "<b>Contexto & Atuação:</b> Brand Guidelines e Design Systems completos para a <b>Olimac PE</b> e para a <b>Wolf Agency / Infinit Sublimação</b>, padronizando aplicações digitais, impressas e frotas. Manuais de identidade corporativa (tipografia, paletas de cores, grafismos institucionais); componentes reutilizáveis no <b>Figma e Canva Pro</b> com Auto Layout; e diagramação de catálogos técnicos.<br/>"
                "<b>Link Instagram Olimac PE:</b> <a href='https://www.instagram.com/olimacpe/'><font color='#2980B9'><u>instagram.com/olimacpe/</u></font></a> &nbsp;|&nbsp; <b>Link Infinit / Wolf:</b> <a href='https://www.instagram.com/infinit.sublimacao/'><font color='#2980B9'><u>instagram.com/infinit.sublimacao/</u></font></a> &nbsp;|&nbsp; <b>Impacto:</b> <b>3x mais agilidade</b> e consistência 100%.",
                body_style
            )]
        ]
        case6_tbl = Table(case6_box_data, colWidths=[519])
        case6_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), C_CARD_HEADER),
            ('BACKGROUND', (0,1), (-1,-1), C_WHITE),
            ('BOX', (0,0), (-1,-1), 0.7, C_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(case6_tbl)

        story.append(PageBreak())

        # ==========================================
        # PÁGINA 3: ENGENHARIA DE CAMPANHAS, GRÁFICOS & MATRIZ
        # ==========================================
        story.append(Paragraph("<b>4. Metodologia de E-mail Marketing Responsivo, Lifecycle & Testes A/B</b>", h1_style))
        story.append(HRFlowable(width="100%", thickness=0.8, color=C_ACCENT_BLUE, spaceAfter=4))
        story.append(Paragraph(
            "Desenvolvimento de templates em HTML/CSS fluido (*fluid-hybrid*), testes em +30 clientes de e-mail (Outlook/Apple/Gmail), tags de personalização dinâmica, conformidade SPF/DKIM e testes A/B estruturados de assunto e CTA.",
            body_style
        ))
        story.append(Spacer(1, 4))

        # Dois Gráficos Lado a Lado (Proporção expandida)
        img_email = Image(chart_email_path, width=256, height=154)
        img_ab = Image(chart_ab_path, width=256, height=154)
        charts_row = Table([[img_email, img_ab]], colWidths=[259, 260])
        charts_row.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(charts_row)
        story.append(Spacer(1, 6))

        # Box de Especificações Técnicas de Engenharia de E-mail e Produção Gráfica
        specs_box_data = [
            [
                Paragraph("<b>Padrões de E-mail Responsivo & Lifecycle:</b><br/>• Arquitetura HTML5 Tables com estilos inline compilados.<br/>• Suporte nativo a Dark Mode via media queries avançadas.<br/>• VML (Vector Markup Language) para renderização no Outlook.<br/>• Tags dinâmicas de substituição (Salesforce, Braze, Hubspot).<br/>• Entregabilidade e conformidade com protocolos SPF, DKIM e DMARC.", body_style),
                Paragraph("<b>Engenharia de Pré-Impressão & Mala Direta:</b><br/>• Fechamento em PDF/X-1a e PDF/X-4 com fontes em curvas.<br/>• Espaço de cores CMYK calibrado a 300 DPI de resolução.<br/>• Sangria técnica regulamentar de 3mm e margem de segurança de 5mm.<br/>• Especificação de substratos (Couché 300g, Offset 120g, Kraft).<br/>• Acabamentos nobres: Verniz UV Localizado, Soft Touch e Hot Stamping.", body_style)
            ]
        ]
        specs_box_tbl = Table(specs_box_data, colWidths=[256, 257])
        specs_box_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), C_LIGHT_BG),
            ('BOX', (0,0), (-1,-1), 0.7, C_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 4.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(specs_box_tbl)
        story.append(Spacer(1, 6))

        # Matriz Completa de Ferramentas Dominadas
        story.append(Paragraph("<b>5. Matriz Geral de Tecnologias & Ferramentas Dominadas</b>", h1_style))
        story.append(HRFlowable(width="100%", thickness=0.8, color=C_ACCENT_BLUE, spaceAfter=3))

        tools_data = [
            [
                Paragraph("<b>Audiovisual & Som</b>", body_bold),
                Paragraph("Final Cut Pro, CapCut Pro, Logic Pro (Sound Design/ASMR), DaVinci Resolve, iPhone 14 Pro Max 4K, Apple Silicon M1.", body_style)
            ],
            [
                Paragraph("<b>Design & Layout</b>", body_bold),
                Paragraph("Figma (Design Systems/Auto Layout), Canva Pro, Adobe Photoshop, Adobe Illustrator, Adobe InDesign.", body_style)
            ],
            [
                Paragraph("<b>E-mail & Código</b>", body_bold),
                Paragraph("HTML5 Semântico, CSS3 Inline, Responsive Table Layouts, Liquid / Dynamic Tags, Git/GitHub.", body_style)
            ],
            [
                Paragraph("<b>Automação & CRM</b>", body_bold),
                Paragraph("Salesforce Marketing Cloud, Braze, Hubspot, Mailchimp, Qyon CRM, RD Station.", body_style)
            ],
            [
                Paragraph("<b>Analytics & Dados</b>", body_bold),
                Paragraph("Testes A/B Multivariáveis, Google Analytics 4 (GA4), Looker Studio, Google Sheets Avançado, Microsoft Excel.", body_style)
            ],
            [
                Paragraph("<b>Produção Gráfica</b>", body_bold),
                Paragraph("Fechamento PDF/X-1a, Gestão CMYK 300 DPI, Sangrias 3mm, Facas Especiais, Verniz UV Localizado, Papéis Especiais.", body_style)
            ]
        ]
        tools_tbl = Table(tools_data, colWidths=[120, 399])
        tools_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), C_LIGHT_BG),
            ('BOX', (0,0), (-1,-1), 0.6, C_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 2.8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.8),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(tools_tbl)

        doc.build(story, canvasmaker=NumberedCanvas)
        print(f"✅ Portfólio de Marketing em PDF gerado com sucesso em: {output_pdf_path}")

if __name__ == "__main__":
    output_path = "carreira/base/marketing_audiovisual/pdf/Portfolio_Fabio_Rodrigues_Marketing_Campanhas.pdf"
    if len(sys.argv) > 1:
        output_path = sys.argv[1]
    gerar_portfolio_pdf(output_path)
