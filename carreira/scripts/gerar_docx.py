#!/usr/bin/env python3
"""
Gerador de Documentos Word (.docx) — Ecossistema NOVA
Módulo de Carreira: Exportação de Currículos e Cover Letters em formato Microsoft Word.

Padrões de Design:
- Tipografia: Calibri / Arial corporativo
- Margens: 2.54 cm (1 polegada - Padrão Harvard / ABNT)
- ATS-Friendly: Tabela e formatação em coluna única sem caixas de texto flutuantes
- Hierarquia Visual: Cores sóbrias (#1A2530, #2C3E50, #555555)
- Injeção Automática de Links Oficiais por Especialidade da Vaga
"""

import os
import sys
import re
import argparse
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

# ==============================================================================
# MATRIZ OFICIAL E PERMANENTE DE LINKS POR ESPECIALIDADE (NOVA)
# ==============================================================================
LINK_PORTFOLIO_AUDIOVISUAL = "https://drive.google.com/drive/folders/1fhmqNSZG9h7Tv4pFzqysuuBcIY4Sw-ri?usp=sharing"
LINK_PORTFOLIO_MARKETING = "https://drive.google.com/drive/folders/1Mz7BoxVzmUnZd24H7n9zrvByGN_bzFxm?usp=sharing"
LINK_LINKEDIN = "https://linkedin.com/in/fabiorodrigues-dev"
LINK_GITHUB = "https://github.com/fabiorodrigues-tech-dev/NOVA"

def classify_job_specialty(text_or_path: str, explicit_category: str = None) -> str:
    """
    Classifica a especialidade da vaga em uma das 4 categorias oficiais:
    1. 'filmmaker_audiovisual': Filmmaker, Edição de Vídeo, Audiovisual, Direção Criativa, Criação Audiovisual.
    2. 'marketing_campanhas': Marketing, Campanhas, Growth, CRM, E-mail Marketing, Endomarketing, Branding.
    3. 'suporte_operacoes': Suporte SaaS/ERP, Help Desk, Operações, Administrativo, CX.
    4. 'tech_dev': Java, Spring, Backend, Dev, Engenharia de Software, Full Stack.
    """
    if explicit_category:
        cat_lower = explicit_category.lower().strip()
        if any(k in cat_lower for k in ["film", "audio", "video", "vídeo", "edicao", "edição", "cinema"]):
            return "filmmaker_audiovisual"
        if any(k in cat_lower for k in ["mkt", "market", "campanh", "growth", "crm", "brand", "endo", "email", "e-mail", "social"]):
            return "marketing_campanhas"
        if any(k in cat_lower for k in ["suport", "operac", "operaç", "admin", "cx", "help"]):
            return "suporte_operacoes"
        if any(k in cat_lower for k in ["tech", "dev", "back", "java", "spring", "soft"]):
            return "tech_dev"

    content_lower = text_or_path.lower()

    if "suporte_operacoes" in content_lower or "administrativo_suporte" in content_lower:
        return "suporte_operacoes"
    if "tech_dev" in content_lower or "dev/" in content_lower:
        return "tech_dev"

    is_filmmaker_keywords = any(k in content_lower for k in [
        "filmmaker", "audiovisual", "edição de vídeo", "edicao de video", "videomaker",
        "diretor criativo", "motion", "color grading", "final cut", "capcut", "davinci resolve",
        "logic pro", "prores", "captação", "camera", "câmera"
    ])

    is_marketing_keywords = any(k in content_lower for k in [
        "marketing", "campanha", "growth", "crm", "e-mail marketing", "email marketing",
        "endomarketing", "branding", "ga4", "google analytics", "direct mail", "mala direta",
        "comunicação interna", "social media", "tráfego", "performance", "publicidade",
        "marketing_campanhas", "marketing_digital", "marketing_design"
    ])

    is_suporte_keywords = any(k in content_lower for k in [
        "suporte", "atendimento", "help desk", "service desk", "nps", "csat", "erp", "qyon", "icp-brasil"
    ])

    is_tech_keywords = any(k in content_lower for k in [
        "java", "spring", "backend", "back-end", "rest", "junit", "postgresql", "docker", "clean architecture"
    ])

    if "filmmaker" in content_lower or "audiovisual" in content_lower:
        return "filmmaker_audiovisual"
    if is_marketing_keywords and not is_filmmaker_keywords:
        return "marketing_campanhas"
    if is_filmmaker_keywords:
        return "filmmaker_audiovisual"
    if is_marketing_keywords:
        return "marketing_campanhas"
    if is_suporte_keywords:
        return "suporte_operacoes"
    if is_tech_keywords:
        return "tech_dev"

    return "tech_dev"

def strip_emojis(text: str) -> str:
    """Remove emojis e caracteres gráficos não-ASCII."""
    custom_symbols = [
        "■", "▪", "▫", "🔹", "🔸", "📍", "📧", "📱", "💼", "💻", "🚀", "🌌",
        "🎙️", "🎙", "🎓", "🎯", "🛠️", "🛠", "🔍", "⚡", "📅", "📝", "📊",
        "💡", "⚪", "🟢", "🟡", "❌", "🌟", "✨", "🔗", "⭐", "🏷️", "🏷", "✉️"
    ]
    for sym in custom_symbols:
        text = text.replace(sym, "")
    emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
    text = emoji_pattern.sub('', text)
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\|\s*\|', '|', text)
    return text.strip()

def add_bottom_border(paragraph, color_hex="1A2530", size="6"):
    """Adiciona uma linha horizontal sutil abaixo do parágrafo no Word."""
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="{size}" w:space="4" w:color="{color_hex}"/></w:pBdr>')
    pPr.append(pBdr)

def add_hyperlink(paragraph, url: str, text: str, color="2980B9", underline=True, font_size=Pt(8.5)):
    """Insere um hyperlink clicável nativo em um parágrafo do Word."""
    part = paragraph.part
    r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
    hyperlink = parse_xml(f'<w:hyperlink {nsdecls("w", "r")} r:id="{r_id}" w:history="1"/>')
    new_run = parse_xml(
        f'<w:r {nsdecls("w")}><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:color w:val="{color}"/>' +
        ('<w:u w:val="single"/>' if underline else '') +
        f'<w:sz w:val="{int(font_size.pt * 2)}"/></w:rPr><w:t>{text}</w:t></w:r>'
    )
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)

def add_formatted_text(paragraph, text: str, base_font_size=Pt(10), base_color=RGBColor(44, 62, 80), default_bold=False, default_italic=False):
    """
    Processa formatação inline básica de markdown (**negrito**, *itálico*, `código`) e insere runs.
    """
    text = strip_emojis(text)
    # Remove markdown links [texto](url) -> texto
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)

    # Tokeniza partes de negrito e itálico
    tokens = re.split(r'(\*\*[^\*]+\*\*|\*[^\*]+\*|`[^`]+`)', text)
    for token in tokens:
        if not token:
            continue
        run = paragraph.add_run()
        run.font.name = 'Calibri'
        run.font.size = base_font_size
        run.font.color.rgb = base_color
        run.bold = default_bold
        run.italic = default_italic

        if token.startswith('**') and token.endswith('**'):
            run.text = token[2:-2]
            run.bold = True
        elif token.startswith('*') and token.endswith('*'):
            run.text = token[1:-1]
            run.italic = True
        elif token.startswith('`') and token.endswith('`'):
            run.text = token[1:-1]
            run.font.name = 'Consolas'
            run.font.size = Pt(9)
            run.font.color.rgb = RGBColor(30, 30, 30)
        else:
            run.text = token

def render_contact_paragraph(paragraph, raw_contact: str, specialty: str):
    """Renderiza a linha de contatos com texto limpo e hyperlinks clicáveis."""
    loc_part = "Recife, PE — Brasil"
    mail_part = "fabioandre777@gmail.com"
    phone_part = "(81) 98992-0040"

    if raw_contact:
        parts = [p.strip() for p in raw_contact.split("|")]
        for p in parts:
            clean_p = strip_emojis(p)
            if "recife" in clean_p.lower() or "brasil" in clean_p.lower() or "remoto" in clean_p.lower():
                loc_part = clean_p
            elif "@" in clean_p:
                mail_part = clean_p
            elif re.search(r'\(\d{2}\)', clean_p) or "98992" in clean_p:
                phone_part = clean_p

    # Adiciona texto base
    run_base = paragraph.add_run(f"{loc_part}  |  {mail_part}  |  {phone_part}  |  ")
    run_base.font.name = 'Calibri'
    run_base.font.size = Pt(8.5)
    run_base.font.color.rgb = RGBColor(100, 100, 100)

    if specialty == "filmmaker_audiovisual":
        add_hyperlink(paragraph, LINK_PORTFOLIO_AUDIOVISUAL, "Portfólio no Google Drive", color="2980B9", font_size=Pt(8.5))
    elif specialty == "marketing_campanhas":
        add_hyperlink(paragraph, LINK_PORTFOLIO_MARKETING, "Portfólio no Google Drive", color="2980B9", font_size=Pt(8.5))
    elif specialty == "suporte_operacoes":
        add_hyperlink(paragraph, LINK_LINKEDIN, "LinkedIn", color="2980B9", font_size=Pt(8.5))
    else:  # tech_dev
        add_hyperlink(paragraph, LINK_LINKEDIN, "LinkedIn", color="2980B9", font_size=Pt(8.5))
        run_sep = paragraph.add_run("  |  ")
        run_sep.font.name = 'Calibri'
        run_sep.font.size = Pt(8.5)
        run_sep.font.color.rgb = RGBColor(100, 100, 100)
        add_hyperlink(paragraph, LINK_GITHUB, "GitHub", color="2980B9", font_size=Pt(8.5))

def gerar_cv_docx(markdown_path: str, output_docx_path: str, category: str = None):
    """
    Converte um currículo Markdown em um documento Word (.docx) no padrão Harvard Tech ATS.
    Injeta automaticamente o cabeçalho e hyperlinks com base na especialidade da vaga.
    """
    if not os.path.exists(markdown_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {markdown_path}")

    with open(markdown_path, "r", encoding="utf-8") as f:
        content = f.read()

    os.makedirs(os.path.dirname(os.path.abspath(output_docx_path)), exist_ok=True)

    specialty = classify_job_specialty(markdown_path + " " + content, category)

    doc = Document()
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.6)
        section.bottom_margin = Inches(0.6)
        section.left_margin = Inches(0.65)
        section.right_margin = Inches(0.65)

    lines = content.splitlines()
    header_done = False
    i = 0

    while i < len(lines):
        line = lines[i]
        raw_line = line.strip()

        if not raw_line or raw_line == "---":
            i += 1
            continue

        # Cabeçalho Principal (Nome)
        if not header_done and raw_line.startswith("# "):
            name_text = raw_line[2:].strip()
            p_name = doc.add_paragraph()
            p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_name.paragraph_format.space_after = Pt(2)
            p_name.paragraph_format.space_before = Pt(0)
            run = p_name.add_run(strip_emojis(name_text))
            run.font.name = 'Calibri'
            run.font.size = Pt(18)
            run.font.bold = True
            run.font.color.rgb = RGBColor(26, 37, 48)

            i += 1
            # Subtítulo
            while i < len(lines) and not lines[i].strip():
                i += 1
            if i < len(lines) and lines[i].strip().startswith("**"):
                sub_text = lines[i].strip().replace("**", "")
                p_sub = doc.add_paragraph()
                p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_sub.paragraph_format.space_after = Pt(2)
                run_sub = p_sub.add_run(strip_emojis(sub_text))
                run_sub.font.name = 'Calibri'
                run_sub.font.size = Pt(10)
                run_sub.font.bold = True
                run_sub.font.color.rgb = RGBColor(41, 128, 185)
                i += 1

            # Contato
            while i < len(lines) and not lines[i].strip():
                i += 1
            if i < len(lines) and ("@" in lines[i] or "|" in lines[i]):
                contact_text = lines[i].strip()
                p_contact = doc.add_paragraph()
                p_contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_contact.paragraph_format.space_after = Pt(6)
                render_contact_paragraph(p_contact, contact_text, specialty)
                add_bottom_border(p_contact, color_hex="1A2530", size="8")
                i += 1

            header_done = True
            continue

        # Título de Seção (## RESUMO, ## COMPETÊNCIAS, etc.)
        if raw_line.startswith("## "):
            sec_text = raw_line[3:].strip()
            p_sec = doc.add_paragraph()
            p_sec.paragraph_format.space_before = Pt(8)
            p_sec.paragraph_format.space_after = Pt(2)
            p_sec.paragraph_format.keep_with_next = True
            run = p_sec.add_run(strip_emojis(sec_text).upper())
            run.font.name = 'Calibri'
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = RGBColor(26, 37, 48)
            add_bottom_border(p_sec, color_hex="BDC3C7", size="4")
            i += 1
            continue

        # Subtítulo de Cargo / Empresa (### ...)
        if raw_line.startswith("### "):
            role_text = raw_line[4:].strip()
            p_role = doc.add_paragraph()
            p_role.paragraph_format.space_before = Pt(5)
            p_role.paragraph_format.space_after = Pt(1)
            p_role.paragraph_format.keep_with_next = True
            add_formatted_text(p_role, role_text, base_font_size=Pt(9.5), base_color=RGBColor(26, 37, 48), default_bold=True)
            i += 1
            continue

        # Metadados de período (*Abril de 2026 – Atual | Recife, PE*)
        if raw_line.startswith("*") and raw_line.endswith("*") and len(raw_line) < 100:
            meta_text = raw_line[1:-1].strip()
            p_meta = doc.add_paragraph()
            p_meta.paragraph_format.space_after = Pt(2)
            p_meta.paragraph_format.keep_with_next = True
            run = p_meta.add_run(strip_emojis(meta_text))
            run.font.name = 'Calibri'
            run.font.size = Pt(8.5)
            run.font.italic = True
            run.font.color.rgb = RGBColor(120, 120, 120)
            i += 1
            continue

        # Bullet point (- ... ou • ... ou * ...)
        if raw_line.startswith("- ") or raw_line.startswith("• ") or (raw_line.startswith("* ") and not raw_line.endswith("*")):
            bullet_text = raw_line[2:].strip()
            p_bullet = doc.add_paragraph(style='List Bullet')
            p_bullet.paragraph_format.space_after = Pt(2)
            p_bullet.paragraph_format.left_indent = Inches(0.2)
            add_formatted_text(p_bullet, bullet_text, base_font_size=Pt(9), base_color=RGBColor(44, 62, 80))
            i += 1
            continue

        # Parágrafo comum
        p_body = doc.add_paragraph()
        p_body.paragraph_format.space_after = Pt(4)
        p_body.paragraph_format.line_spacing = 1.15
        add_formatted_text(p_body, raw_line, base_font_size=Pt(9), base_color=RGBColor(44, 62, 80))
        i += 1

    doc.save(output_docx_path)
    print(f"✅ Documento Word do Currículo gerado em: {output_docx_path} (Especialidade: {specialty})")

def gerar_cover_letter_docx(markdown_path: str, output_docx_path: str, category: str = None):
    """
    Converte uma Cover Letter Markdown em um documento Word (.docx) timbrado e formal.
    Injeta cabeçalho e contatos oficiais baseados na especialidade.
    """
    if not os.path.exists(markdown_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {markdown_path}")

    with open(markdown_path, "r", encoding="utf-8") as f:
        content = f.read()

    os.makedirs(os.path.dirname(os.path.abspath(output_docx_path)), exist_ok=True)

    specialty = classify_job_specialty(markdown_path + " " + content, category)

    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    lines = content.splitlines()
    header_done = False
    i = 0

    while i < len(lines):
        line = lines[i]
        raw_line = line.strip()

        if not raw_line or raw_line == "---":
            i += 1
            continue

        # Título da Carta (# ✉️ Carta de Apresentação ...)
        if not header_done and raw_line.startswith("# "):
            title_text = raw_line[2:].strip()
            p_title = doc.add_paragraph()
            p_title.paragraph_format.space_after = Pt(4)
            run = p_title.add_run(strip_emojis(title_text))
            run.font.name = 'Calibri'
            run.font.size = Pt(14)
            run.font.bold = True
            run.font.color.rgb = RGBColor(26, 37, 48)

            # Extrai dados do candidato e contato
            i += 1
            while i < len(lines) and lines[i].strip().startswith("**"):
                c_line = lines[i].strip()
                p_c = doc.add_paragraph()
                p_c.paragraph_format.space_after = Pt(1)

                if "@" in c_line or "contato" in c_line.lower() or "98992" in c_line:
                    run_c_label = p_c.add_run("Contato: ")
                    run_c_label.bold = True
                    run_c_label.font.name = 'Calibri'
                    run_c_label.font.size = Pt(9)
                    run_c_label.font.color.rgb = RGBColor(80, 80, 80)

                    run_c_val = p_c.add_run("fabioandre777@gmail.com | (81) 98992-0040 | ")
                    run_c_val.font.name = 'Calibri'
                    run_c_val.font.size = Pt(9)
                    run_c_val.font.color.rgb = RGBColor(80, 80, 80)

                    if specialty == "filmmaker_audiovisual":
                        add_hyperlink(p_c, LINK_PORTFOLIO_AUDIOVISUAL, "Portfólio no Google Drive", color="2980B9", font_size=Pt(9))
                    elif specialty == "marketing_campanhas":
                        add_hyperlink(p_c, LINK_PORTFOLIO_MARKETING, "Portfólio no Google Drive", color="2980B9", font_size=Pt(9))
                    elif specialty == "suporte_operacoes":
                        add_hyperlink(p_c, LINK_LINKEDIN, "LinkedIn", color="2980B9", font_size=Pt(9))
                    else:
                        add_hyperlink(p_c, LINK_LINKEDIN, "LinkedIn", color="2980B9", font_size=Pt(9))
                else:
                    add_formatted_text(p_c, c_line, base_font_size=Pt(9), base_color=RGBColor(80, 80, 80))

                i += 1

            # Linha divisória timbrada
            p_div = doc.add_paragraph()
            p_div.paragraph_format.space_after = Pt(12)
            add_bottom_border(p_div, color_hex="1A2530", size="8")
            header_done = True
            continue

        # Destinatário ou Assunto (**À Equipe...** ou **Assunto:...**)
        if raw_line.startswith("**À") or raw_line.startswith("**Assunto"):
            p_rec = doc.add_paragraph()
            p_rec.paragraph_format.space_after = Pt(4)
            add_formatted_text(p_rec, raw_line, base_font_size=Pt(10), base_color=RGBColor(26, 37, 48), default_bold=True)
            i += 1
            continue

        # Itens numerados (1. NOVA, 2. Sofia, etc.)
        if re.match(r'^\d+\.\s+', raw_line):
            num_match = re.match(r'^(\d+\.\s+)(.+)', raw_line)
            num_prefix = num_match.group(1)
            item_text = num_match.group(2)

            p_item = doc.add_paragraph()
            p_item.paragraph_format.left_indent = Inches(0.25)
            p_item.paragraph_format.space_after = Pt(4)
            p_item.paragraph_format.line_spacing = 1.15
            run_num = p_item.add_run(num_prefix)
            run_num.font.name = 'Calibri'
            run_num.font.size = Pt(9.5)
            run_num.font.bold = True
            run_num.font.color.rgb = RGBColor(41, 128, 185)
            add_formatted_text(p_item, item_text, base_font_size=Pt(9.5), base_color=RGBColor(44, 62, 80))
            i += 1
            continue

        # Saudação / Fechamento
        if raw_line.startswith("Prezada") or raw_line.startswith("Atenciosamente") or raw_line.startswith("**Fábio Rodrigues**"):
            p_salut = doc.add_paragraph()
            p_salut.paragraph_format.space_before = Pt(8)
            p_salut.paragraph_format.space_after = Pt(4)
            add_formatted_text(p_salut, raw_line, base_font_size=Pt(10), base_color=RGBColor(26, 37, 48))
            i += 1
            continue

        # Parágrafo padrão da carta
        p_body = doc.add_paragraph()
        p_body.paragraph_format.space_after = Pt(6)
        p_body.paragraph_format.line_spacing = 1.15
        p_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        if "portfólio" in raw_line.lower() or "drive.google.com" in raw_line:
            if specialty == "filmmaker_audiovisual":
                raw_line = re.sub(r'https?://drive\.google\.com[^\s\)]+', LINK_PORTFOLIO_AUDIOVISUAL, raw_line)
            elif specialty == "marketing_campanhas":
                raw_line = re.sub(r'https?://drive\.google\.com[^\s\)]+', LINK_PORTFOLIO_MARKETING, raw_line)

        add_formatted_text(p_body, raw_line, base_font_size=Pt(10), base_color=RGBColor(44, 62, 80))
        i += 1

    doc.save(output_docx_path)
    print(f"✅ Documento Word da Cover Letter gerado em: {output_docx_path} (Especialidade: {specialty})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Conversor de Markdown para Word DOCX (NOVA)")
    parser.add_argument("--type", choices=["cv", "cover_letter"], default="cv", help="Tipo de documento a gerar")
    parser.add_argument("--input", required=True, help="Caminho do arquivo markdown de entrada")
    parser.add_argument("--output", required=True, help="Caminho do arquivo DOCX de saída")
    parser.add_argument("--category", default=None, help="Especialidade da vaga (filmmaker, marketing, suporte, dev/tech)")

    args = parser.parse_args()
    if args.type == "cover_letter":
        gerar_cover_letter_docx(args.input, args.output, category=args.category)
    else:
        gerar_cv_docx(args.input, args.output, category=args.category)
