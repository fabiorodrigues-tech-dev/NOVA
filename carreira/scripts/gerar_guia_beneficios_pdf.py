#!/usr/bin/env python3
"""
Gerador de Guia Visual de Benefícios & Total Compensation em PDF — Padrão Executivo CI&T
Ecossistema NOVA — Módulo de Carreira & Engenharia Visual
"""

import os
import sys
import tempfile
import matplotlib.pyplot as plt
import numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether, Table, TableStyle, Image, PageBreak
)

def gerar_graficos_beneficios(tmpdir: str):
    """Gera gráficos visuais de alta fidelidade para o guia de benefícios."""
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    # 1. Gráfico Donut: Composição de Total Compensation Anual
    fig, ax = plt.subplots(figsize=(6.5, 3.2), subplot_kw=dict(aspect="equal"))
    labels = ['Salário Base Nominal\n(R$ 162.000)', '13º + 1/3 Férias\n(R$ 31.500)', 'PLR Estimada\n(R$ 20.250)', 'VR / VA Flexível\n(R$ 15.600)', 'FGTS Acumulado\n(R$ 12.960)', 'Saúde, Gym & Educ.\n(R$ 16.200)', 'Economia Remoto\n(R$ 12.000)']
    sizes = [162000, 31500, 20250, 15600, 12960, 16200, 12000]
    cores = ['#1A5276', '#2980B9', '#27AE60', '#E67E22', '#8E44AD', '#16A085', '#D35400']
    
    wedges, texts, autotexts = ax.pie(
        sizes, 
        autopct='%1.1f%%',
        pctdistance=0.78,
        colors=cores,
        startangle=140,
        wedgeprops=dict(width=0.42, edgecolor='white', linewidth=2)
    )
    plt.setp(autotexts, size=8, weight="bold", color="white")
    ax.set_title("Composição do Pacote de Total Compensation Anual (R$ 270.510 / ano)", fontsize=10.5, weight='bold', pad=10, color='#1A2530')
    
    # Legenda compacta
    ax.legend(wedges, labels, title="Componentes", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=7.5)
    plt.tight_layout()
    chart1_path = os.path.join(tmpdir, "donut_total_comp.png")
    plt.savefig(chart1_path, dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Gráfico de Barras Horizontais: Valoração Anual dos Benefícios e Vantagens
    fig, ax = plt.subplots(figsize=(6.5, 2.5))
    itens = [
        'Economia 100% Remoto',
        'Seguro & Clube Descontos',
        'Gympass & Saúde Mental',
        'CI&T University & Idiomas',
        'Plano Saúde & Odonto',
        'FGTS Depositado (8%)',
        'VR / VA Flexível (Swile)',
        '13º Salário Integral',
        'Férias + 1/3 Constitucional',
        'PLR (Bônus Semestral/Anual)'
    ]
    valores = [12000, 1200, 3000, 3600, 9600, 12960, 15600, 13500, 18000, 20250]
    y_pos = np.arange(len(itens))
    
    bars = ax.barh(y_pos, [v/1000 for v in valores], color='#2E86C1', edgecolor='#1B4F72', height=0.65)
    bars[-1].set_color('#27AE60') # Destaque PLR
    bars[-2].set_color('#16A085') # Destaque Férias
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(itens, fontsize=7.5, color='#2C3E50', weight='bold')
    ax.set_xlabel('Valor Anual Equivalente (em Milhares de R$)', fontsize=8, color='#5D6D7E')
    ax.set_title('Valoração Financeira Direta dos Benefícios & Aditivos (R$/Ano)', fontsize=9.5, weight='bold', color='#1A2530')
    
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.3, bar.get_y() + bar.get_height()/2, f'R$ {width*1000:,.0f}'.replace(',', '.'),
                ha='left', va='center', fontsize=7, color='#1A2530', weight='bold')
        
    ax.set_xlim(0, 26)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    chart2_path = os.path.join(tmpdir, "bar_beneficios.png")
    plt.savefig(chart2_path, dpi=300, bbox_inches='tight')
    plt.close()

    return chart1_path, chart2_path

def gerar_pdf_beneficios(output_pdf_path: str):
    os.makedirs(os.path.dirname(os.path.abspath(output_pdf_path)), exist_ok=True)
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
    title_style = ParagraphStyle('BTitle', fontName='Helvetica-Bold', fontSize=15, leading=19, textColor=colors.HexColor('#1A2530'), alignment=1)
    sub_style = ParagraphStyle('BSub', fontName='Helvetica', fontSize=9, leading=12, textColor=colors.HexColor('#5D6D7E'), alignment=1)
    sec_style = ParagraphStyle('BSec', fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=colors.HexColor('#1A2530'), spaceBefore=6, spaceAfter=3)
    body_style = ParagraphStyle('BBody', fontName='Helvetica', fontSize=8, leading=11.5, textColor=colors.HexColor('#2C3E50'))
    bullet_style = ParagraphStyle('BBullet', fontName='Helvetica', fontSize=8, leading=11.5, textColor=colors.HexColor('#2C3E50'), leftIndent=10, spaceAfter=2)
    card_title = ParagraphStyle('CTitle', fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=colors.HexColor('#1A5276'))

    with tempfile.TemporaryDirectory() as tmpdir:
        chart1_path, chart2_path = gerar_graficos_beneficios(tmpdir)
        story = []

        # ================= PÁGINA 1 =================
        story.append(Paragraph("NOVA &bull; DOSSIÊ EXECUTIVO DE BENEFÍCIOS & TOTAL COMPENSATION", title_style))
        story.append(Paragraph("Vaga: <b>[Job-31145] Senior Developer Java</b> | Empresa: <b>CI&T</b> | Modelo: <b>100% Remoto (Brasil)</b>", sub_style))
        story.append(Spacer(1, 4))
        story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#1A2530"), spaceAfter=6))

        # KPI Banner
        kpi_data = [
            [
                Paragraph("SALÁRIO BASE NOMINAL", ParagraphStyle('K1', fontName='Helvetica', fontSize=7, alignment=1, textColor=colors.HexColor('#5D6D7E'))),
                Paragraph("TOTAL ANUAL ESTIMADO", ParagraphStyle('K2', fontName='Helvetica', fontSize=7, alignment=1, textColor=colors.HexColor('#5D6D7E'))),
                Paragraph("PLR ANUAL ESTIMADA", ParagraphStyle('K3', fontName='Helvetica', fontSize=7, alignment=1, textColor=colors.HexColor('#5D6D7E'))),
                Paragraph("BENEFÍCIOS MENSAIS", ParagraphStyle('K4', fontName='Helvetica', fontSize=7, alignment=1, textColor=colors.HexColor('#5D6D7E')))
            ],
            [
                Paragraph("<b>R$ 13.500,00</b>", ParagraphStyle('V1', fontName='Helvetica-Bold', fontSize=11, alignment=1, textColor=colors.HexColor('#1A2530'))),
                Paragraph("<font color='#27AE60'><b>R$ 270.510,00</b></font>", ParagraphStyle('V2', fontName='Helvetica-Bold', fontSize=11, alignment=1)),
                Paragraph("<b>R$ 20.250,00</b>", ParagraphStyle('V3', fontName='Helvetica-Bold', fontSize=11, alignment=1, textColor=colors.HexColor('#2980B9'))),
                Paragraph("<b>R$ 2.450,00+</b>", ParagraphStyle('V4', fontName='Helvetica-Bold', fontSize=11, alignment=1, textColor=colors.HexColor('#E67E22')))
            ]
        ]
        kpi_table = Table(kpi_data, colWidths=[130, 130, 130, 130])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F9F9')),
            ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#BDC3C7')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E8E8')),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        story.append(kpi_table)
        story.append(Spacer(1, 6))

        # Gráfico Donut de Composição
        if os.path.exists(chart1_path):
            story.append(Image(chart1_path, width=520, height=205))
            story.append(Spacer(1, 4))

        # Gráfico de Barras Horizontais
        if os.path.exists(chart2_path):
            story.append(Image(chart2_path, width=520, height=195))
            story.append(Spacer(1, 4))

        # ================= PÁGINA 2 =================
        story.append(PageBreak())

        story.append(Paragraph("DETALHAMENTO DOS 5 PILARES DE VALOR & VANTAGENS CI&T", title_style))
        story.append(Paragraph("Análise aprofundada dos programas de saúde, desenvolvimento, flexibilidade e família.", sub_style))
        story.append(Spacer(1, 4))
        story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#1A2530"), spaceAfter=8))

        # Cards dos 5 Pilares
        cards_content = [
            [
                Paragraph("<b>1. Saúde Integral & Bem-Estar</b>", card_title),
                Paragraph("<b>2. Alimentação, Bônus & Finanças</b>", card_title)
            ],
            [
                Paragraph(
                    "&bull; <b>Plano de Saúde & Odonto Premium:</b> Bradesco/SulAmérica nacional sem coparticipação abusiva para titular e dependentes.<br/>"
                    "&bull; <b>Wellhub (Gympass) & TotalPass:</b> Acesso a redes de academias, estúdios, pilates e apps de nutrição e meditação.<br/>"
                    "&bull; <b>Saúde Mental Online:</b> Telepsicologia gratuita 24/7, telemedicina e programas de prevenção de burnout.",
                    body_style
                ),
                Paragraph(
                    "&bull; <b>VR & VA Flexível (Swile/Flash):</b> ~R$ 1.300,00/mês para restaurantes, supermercados e delivery.<br/>"
                    "&bull; <b>PLR Semestral/Anual:</b> Participação nos Lucros e Resultados média de 1.0 a 2.0 salários (~R$ 13.5k a R$ 27k).<br/>"
                    "&bull; <b>Seguro de Vida & Clube:</b> Proteção corporativa e descontos em centenas de marcas parceiras.",
                    body_style
                )
            ],
            [
                Paragraph("<b>3. Educação Contínua & Carreira Global</b>", card_title),
                Paragraph("<b>4. Família, Parentalidade & Inclusão</b>", card_title)
            ],
            [
                Paragraph(
                    "&bull; <b>CI&T University:</b> Plataforma própria de desenvolvimento contínuo em Agentic SDLC, Cloud e Arquitetura Java.<br/>"
                    "&bull; <b>Plataformas de Cursos & Idiomas:</b> Acesso gratuito a Coursera, Udemy, Alura e cursos de Inglês/Espanhol para projetos globais.<br/>"
                    "&bull; <b>Mentoria & Tech Leads:</b> Cultura colaborativa de code reviews e liderança técnica.",
                    body_style
                ),
                Paragraph(
                    "&bull; <b>Licença Parental Estendida:</b> Empresa Cidadã (maternidade 6 meses e paternidade ampliada).<br/>"
                    "&bull; <b>Auxílio-Creche:</b> Reembolso mensal para apoio na educação infantil dos filhos.<br/>"
                    "&bull; <b>Apoio à Diversidade & PCD:</b> Especialistas em inclusão e suporte humanizado para adaptações de trabalho.",
                    body_style
                )
            ]
        ]
        
        cards_table = Table(cards_content, colWidths=[255, 255])
        cards_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F9F9')),
            ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#BDC3C7')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E8E8')),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(cards_table)
        story.append(Spacer(1, 8))

        # Pilar 5 Destaque: 100% Remoto & ROI de Vida
        remoto_data = [
            [
                Paragraph("<b>5. O Diferencial do Trabalho 100% Remoto (Homeoffice Nacional)</b>", card_title)
            ],
            [
                Paragraph(
                    "&bull; <b>Liberdade Geográfica & Conforto:</b> Atuação direta de Recife/PE com setup personalizado no Apple Silicon M1.<br/>"
                    "&bull; <b>Economia Financeira Direta:</b> Mais de <b>R$ 1.000,00/mês economizados</b> em combustível, trânsito, estacionamento, alimentação na rua e vestuário formal.<br/>"
                    "&bull; <b>Ganho de Tempo Real:</b> Recuperação de 2 a 3 horas diárias que seriam perdidas em deslocamento, gerando maior foco em engenharia, saúde física e bem-estar pessoal.",
                    body_style
                )
            ]
        ]
        remoto_table = Table(remoto_data, colWidths=[520])
        remoto_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EAFAF1')),
            ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#27AE60')),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(remoto_table)
        story.append(Spacer(1, 8))

        # Conclusão e Prontidão
        story.append(Paragraph("<b>Síntese de Impacto para a Entrevista Digital (Digai.ai):</b>", sec_style))
        story.append(Paragraph(
            "Este pacote de remuneração e benefícios consolida uma oportunidade de transformação de patamar de carreira, unindo **estabilidade CLT de padrão internacional**, **rendimento anual superior a R$ 250k** e **posicionamento no epicentro de Agentic SDLC & IA com Java 21**. A preparação assertiva para a entrevista de áudio é o passo decisivo para concretizar essa conquista.",
            body_style
        ))

        doc.build(story)
        print(f"✅ Guia de Benefícios em PDF gerado com sucesso em: {output_pdf_path}")

if __name__ == "__main__":
    out = "carreira/vagas_analisadas/tech_dev/ciandt/guia_beneficios_ciandt.pdf"
    if len(sys.argv) > 1:
        out = sys.argv[1]
    gerar_pdf_beneficios(out)
