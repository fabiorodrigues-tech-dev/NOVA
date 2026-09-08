#!/usr/bin/env python3
"""
Gerador do Currículo de 1 Página — Fábio Rodrigues (Filmmaker & Diretor Criativo)
Ecossistema NOVA - Módulo de Carreira

Gera o arquivo PDF perfeitamente diagramado em página única A4,
com fontes Helvetica, cabeçalho executivo, links clicáveis e as atualizações
de Motion Graphics básico e Fotografia publicitária RAW.
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
)

def gerar_curriculo_filmmaker_pdf(output_pdf_path: str):
    os.makedirs(os.path.dirname(os.path.abspath(output_pdf_path)), exist_ok=True)
    margin = 32  # ~11.3mm

    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=28,
        bottomMargin=24
    )

    styles = getSampleStyleSheet()

    name_style = ParagraphStyle(
        'Name',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=21,
        textColor=colors.HexColor('#111827'),
        spaceAfter=2
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=3
    )

    contact_style = ParagraphStyle(
        'Contact',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#4b5563'),
        spaceAfter=2
    )

    portfolio_style = ParagraphStyle(
        'Portfolio',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#4b5563'),
        spaceAfter=6
    )

    section_style = ParagraphStyle(
        'SectionHeader',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.HexColor('#111827'),
        spaceBefore=7,
        spaceAfter=2
    )

    body_style = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.8,
        textColor=colors.HexColor('#1f2937'),
        spaceBefore=2,
        spaceAfter=2
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.8,
        textColor=colors.HexColor('#1f2937'),
        leftIndent=11,
        firstLineIndent=-11,
        spaceBefore=1.2,
        spaceAfter=1.2
    )

    role_left_style = ParagraphStyle(
        'RoleLeft',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11.5,
        textColor=colors.HexColor('#111827')
    )

    role_right_style = ParagraphStyle(
        'RoleRight',
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=11.5,
        textColor=colors.HexColor('#4b5563'),
        alignment=2
    )

    content_width = 595.275591 - 2 * margin

    def make_job_header(role, company, period):
        title_html = f'<b>{role}</b> <font face="Helvetica" color="#9ca3af">|</font> <b>{company}</b>'
        t = Table(
            [[Paragraph(title_html, role_left_style), Paragraph(period, role_right_style)]],
            colWidths=[content_width * 0.76, content_width * 0.24],
            spaceBefore=3,
            spaceAfter=1
        )
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        return t

    def make_hr(thick=False):
        if thick:
            return HRFlowable(width='100%', thickness=1.5, color=colors.HexColor('#1f2937'), spaceBefore=2, spaceAfter=4)
        else:
            return HRFlowable(width='100%', thickness=0.6, color=colors.HexColor('#d1d5db'), spaceBefore=1, spaceAfter=3)

    story = []

    # Cabeçalho
    story.append(Paragraph('FÁBIO RODRIGUES', name_style))
    subtitle_html = 'FILMMAKER <font face="Helvetica" color="#9ca3af">|</font> EDITOR DE VÍDEO <font face="Helvetica" color="#9ca3af">|</font> CRIADOR DE CONTEÚDO'
    story.append(Paragraph(subtitle_html, subtitle_style))
    contact_html = 'Recife - PE &nbsp;<font color="#9ca3af">|</font>&nbsp; (81) 98992-0040 &nbsp;<font color="#9ca3af">|</font>&nbsp; fabioandre777@gmail.com'
    story.append(Paragraph(contact_html, contact_style))
    story.append(Paragraph('<b>Portfólio:</b> <a href="https://drive.google.com/drive/folders/1rl-SPjOi4tisk2tACb2RcKKAmo6OmBrw"><font color="#2563eb"><u>drive.google.com/drive/folders/1rl-SPjOi4tisk2tACb2RcKKAmo6OmBrw</u></font></a>', portfolio_style))
    story.append(make_hr(thick=True))

    # Resumo Profissional
    story.append(Paragraph('RESUMO PROFISSIONAL', section_style))
    story.append(make_hr())
    story.append(Paragraph(
        'Graduado em Bacharelado em Design (UniFBV) com sólida atuação em edição de vídeo, produção audiovisual e gestão de marketing '
        'estratégico. Ampla experiência em todo o ciclo de criação de conteúdo: planejamento de pauta, roteirização com foco em storytelling e '
        'retenção, captação, edição diária e cobertura em tempo real de feiras corporativas de grande porte. Especialista em vídeos curtos de '
        'alto engajamento (Reels, TikTok e Shorts) e produções na horizontal (videoclipes e institucionais). Diferencial técnico em pós-produção '
        'sonora, realizando tratamento, limpeza de ruídos e masterização de áudio via Logic Pro (standalone e integração via plugins no Final '
        'Cut Pro). Co-fundador da Wolf Agency, com histórico comprovado na gestão de mídia para o varejo e marcas regionais.',
        body_style
    ))

    # Competências & Ferramentas
    story.append(Paragraph('COMPETÊNCIAS & FERRAMENTAS', section_style))
    story.append(make_hr())
    story.append(Paragraph('• <b>Edição de Vídeo & Software:</b> Final Cut Pro (Avançado), CapCut (Avançado), DaVinci Resolve (Intermediário / Rápida Aprendizagem), Motion Graphics básico.', bullet_style))
    story.append(Paragraph('• <b>Tratamento de Áudio:</b> Logic Pro (Tratamento, Limpeza de Ruído, Sound Design e Masterização — standalone e via plugins no Final Cut Pro).', bullet_style))
    story.append(Paragraph('• <b>Produção, Captação & Eventos:</b> Cobertura de feiras/eventos corporativos de grande porte (FuturePrint), bastidores (making of), Fotografia publicitária, edição e revelação digital de imagens (RAW), captação ágil em formatos Verticais e Horizontais, direção de cena e iluminação básica/natural.', bullet_style))
    story.append(Paragraph('• <b>Criação de Conteúdo & Mídia:</b> Storytelling Narrativo, Vídeos Verticais (Reels, TikTok, Shorts), Videoclipes, Mídias para WhatsApp, Comerciais para Web e Campanhas de Varejo/E-commerce.', bullet_style))
    story.append(Paragraph('• <b>Design & Gestão:</b> Fundamentos de Design, Identidade Visual, Liderança de Equipes, Canva, Gestão de Marketing e Branding.', bullet_style))

    # Experiência Profissional
    story.append(Paragraph('EXPERIÊNCIA PROFISSIONAL', section_style))
    story.append(make_hr())

    # Experiência 1: Infinit Tecnologia
    story.append(make_job_header('Produtor de Mídia & Operações', 'Infinit Tecnologia', 'Abr/2026 – Atual'))
    story.append(Paragraph('• Atuação estratégica no desenvolvimento de mídia, captação audiovisual e gerenciamento de redes sociais da empresa.', bullet_style))
    story.append(Paragraph('• <b>Destaque em Cobertura de Eventos:</b> Cobertura audiovisual completa da feira de negócios FuturePrint 2026 (São Paulo) — captação de fotos/vídeos, criação de conteúdo dinâmico em tempo real (Reels/Stories), bastidores (making of) e gestão do Instagram institucional durante todo o evento.', bullet_style))

    # Experiência 2: Unigames
    story.append(make_job_header('Criador de Conteúdo & Produtor Audiovisual', 'Unigames', 'Jul/2025 – Dez/2025'))
    story.append(Paragraph('• Responsável pela produção diária de conteúdos em vídeo e artes promocionais para redes sociais e canais diretos de vendas via WhatsApp.', bullet_style))
    story.append(Paragraph('• Criação de vídeos demonstrativos de produtos, coberturas de lançamentos e materiais em vídeo focados em alta conversão e engajamento.', bullet_style))
    story.append(Paragraph('• Edição completa, tratamento de áudio e finalização ágil adaptadas para o ritmo dinâmico do varejo tecnológico/games.', bullet_style))

    # Experiência 3: Wolf Agency
    story.append(make_job_header('Sócio & Diretor Criativo', 'Wolf Agency', 'Jan/2025 – Jun/2025'))
    story.append(Paragraph('• Liderança de operação criativa em parceria com estrutura gráfica, atuando no planejamento, gravação e edição de peças publicitárias, videoclipes e vídeos corporativos.', bullet_style))
    story.append(Paragraph('• Gestão e execução de projetos audiovisuais para clientes de grande porte regional, como Gráfica do Parque, DER-PE e Gildo Lanches.', bullet_style))
    story.append(Paragraph('• Planejamento e produção de ações de conteúdo e colabs em parceria com a página Recife Ordinário.', bullet_style))

    # Experiência 4: Quintal dos Primos
    story.append(make_job_header('Gerente Geral & Gestor de Marketing', 'Quintal dos Primos / Sorveteria Artesanal', 'Jun/2024 – Dez/2024'))
    story.append(Paragraph('• Gestão completa da operação, equipe e estratégias de marketing do estabelecimento.', bullet_style))
    story.append(Paragraph('• Captação e edição de conteúdos audiovisuais (fotos e vídeos) para divulgação de produtos, campanhas de delivery e mídias sociais.', bullet_style))

    # Experiência 5: Olimac
    story.append(make_job_header('Gestor de Marketing', 'Olimac / Olimac Express', 'Jan/2024 – Mai/2024'))
    story.append(Paragraph('• Planejamento e gestão completa das ações de marketing institucional e comercial da empresa.', bullet_style))
    story.append(Paragraph('• Coordenação de campanhas publicitárias, alinhando a identidade visual da marca com estratégias de comunicação e captação de clientes.', bullet_style))

    # Formação Acadêmica
    story.append(Paragraph('FORMAÇÃO ACADÊMICA', section_style))
    story.append(make_hr())
    story.append(Paragraph('• <b>Bacharelado em Design</b> — Faculdade Boa Viagem (UniFBV), Recife - PE', bullet_style))

    doc.build(story)
    print(f"✅ PDF gerado com sucesso em: {output_pdf_path}")

if __name__ == '__main__':
    target = "/Users/fabioandre/Downloads/Currículos/Curriculo_Fabio_Rodrigues_Filmmaker.pdf"
    if len(sys.argv) > 1:
        target = sys.argv[1]
    gerar_curriculo_filmmaker_pdf(target)
