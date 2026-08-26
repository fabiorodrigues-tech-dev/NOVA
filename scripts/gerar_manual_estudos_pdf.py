#!/usr/bin/env python3
"""
Gerador de Manual / Dossiê Técnico em PDF — Ecossistema NOVA
Compila documentos didáticos e técnicos em PDFs estruturados com código formatado, tabelas e gráficos.
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
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether, Table, TableStyle, Preformatted, PageBreak
)
from reportlab.pdfgen import canvas

# Importa o chart_engine
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
try:
    import chart_engine
except ImportError:
    chart_engine = None

class NumberedCanvas(canvas.Canvas):
    """Adiciona numeração de páginas profissional (Página X de Y) e cabeçalho sutil."""
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
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#7F8C8D"))

        # Cabeçalho (a partir da página 2)
        if self._pageNumber > 1:
            self.drawString(42.5, 805, "NOVA • MANUAL DE ENGENHARIA & ARQUITETURA DE SOFTWARE")
            self.drawRightString(552.5, 805, "Trilha Santander 2026 DIO")
            self.setStrokeColor(colors.HexColor("#BDC3C7"))
            self.setLineWidth(0.5)
            self.line(42.5, 798, 552.5, 798)

        # Rodapé em todas as páginas
        self.setStrokeColor(colors.HexColor("#BDC3C7"))
        self.setLineWidth(0.5)
        self.line(42.5, 45, 552.5, 45)
        self.drawString(42.5, 32, "Ecossistema NOVA • Fábio Rodrigues | Java 21 • Spring Boot 3 • Clean Architecture • IA")
        self.drawRightString(552.5, 32, f"Página {self._pageNumber} de {page_count}")
        self.restoreState()

def clean_inline(text: str) -> str:
    """Converte marcações markdown inline para tags HTML do ReportLab."""
    # Remove emojis customizados
    custom_symbols = [
        "■", "▪", "▫", "🔹", "🔸", "📍", "📧", "📱", "💼", "💻", "🚀", "🌌",
        "🎙️", "🎙", "🎓", "🎯", "🛠️", "🛠", "🔍", "⚡", "📅", "📝", "📊",
        "💡", "⚪", "🟢", "🟡", "❌", "🌟", "✨", "🔗", "⭐", "🏷️", "🏷", "🍩", "💰", "✉️", "📚", "☕", "🍃", "🏛️", "🏛", "🧪", "💾", "🤖", "🐍", "📑", "🔴", "🔵"
    ]
    for sym in custom_symbols:
        text = text.replace(sym, "")
    
    emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
    text = emoji_pattern.sub('', text)
    
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'\*\*\*([^\*]+)\*\*\*', r'<b><i>\1</i></b>', text)
    text = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*([^\*]+)\*', r'<i>\1</i>', text)
    text = re.sub(r'`([^`]+)`', r'<font face="Courier" color="#1A2530"><b>\1</b></font>', text)
    return text.strip()

def compilar_manual_pdf(markdown_path: str, output_pdf_path: str):
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

    doc_title_style = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1A2530'),
        alignment=1,
        spaceAfter=4
    )
    doc_sub_style = ParagraphStyle(
        'DocSub',
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#2980B9'),
        alignment=1,
        spaceAfter=3
    )
    doc_meta_style = ParagraphStyle(
        'DocMeta',
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#7F8C8D'),
        alignment=1,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'H1',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#1A2530'),
        spaceBefore=14,
        spaceAfter=4,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'H2',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#2980B9'),
        spaceBefore=8,
        spaceAfter=2,
        keepWithNext=True
    )
    h3_style = ParagraphStyle(
        'H3',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#2C3E50'),
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=4
    )
    bullet_style = ParagraphStyle(
        'Bullet',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#2C3E50'),
        leftIndent=12,
        spaceAfter=3
    )
    code_style = ParagraphStyle(
        'CodeStyle',
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#1A2530')
    )

    lines = content.splitlines()
    story = []
    i = 0
    header_done = False

    while i < len(lines):
        line = lines[i]
        raw_line = line.strip()

        if not raw_line:
            i += 1
            continue

        # Cabeçalho Principal do Documento
        if not header_done and raw_line.startswith("# "):
            title_text = clean_inline(raw_line[2:])
            story.append(Paragraph(title_text, doc_title_style))

            i += 1
            if i < len(lines) and lines[i].strip().startswith("**"):
                sub_text = clean_inline(lines[i].strip())
                story.append(Paragraph(sub_text, doc_sub_style))
                i += 1

            if i < len(lines) and lines[i].strip().startswith("*"):
                meta_text = clean_inline(lines[i].strip())
                story.append(Paragraph(meta_text, doc_meta_style))
                i += 1

            story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#1A2530"), spaceAfter=10))
            header_done = True
            continue

        # Título de Capítulo H1 (# ...)
        if raw_line.startswith("# ") and header_done:
            chap_text = clean_inline(raw_line[2:])
            heading_elem = KeepTogether([
                Paragraph(chap_text, h1_style),
                HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#1A2530"), spaceAfter=6)
            ])
            story.append(heading_elem)
            i += 1
            continue

        # Subtítulo H2 (## ...)
        if raw_line.startswith("## "):
            sec_text = clean_inline(raw_line[3:])
            heading_elem = KeepTogether([
                Paragraph(sec_text, h2_style),
                HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#BDC3C7"), spaceAfter=4)
            ])
            story.append(heading_elem)
            i += 1
            continue

        # Subtítulo H3 (### ...)
        if raw_line.startswith("### "):
            sub_text = clean_inline(raw_line[4:])
            story.append(Paragraph(sub_text, h3_style))
            i += 1
            continue

        # Bloco de Código (```java, ```text, ```yaml, etc.)
        if raw_line.startswith("```"):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # pula o fecha ```

            code_text = "\n".join(code_lines)
            code_para = Preformatted(code_text, code_style)
            
            # Caixa estilizada para o código
            code_table = Table([[code_para]], colWidths=[510])
            code_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F4F6F7')),
                ('BOX', (0, 0), (-1, -1), 0.6, colors.HexColor('#D5D8DC')),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(Spacer(1, 2))
            story.append(code_table)
            story.append(Spacer(1, 4))
            continue

        # Linha Horizontal (---)
        if raw_line == "---":
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E5E8E8"), spaceBefore=4, spaceAfter=6))
            i += 1
            continue

        # Bullets (- ... ou • ... ou * ...)
        if raw_line.startswith("- ") or raw_line.startswith("• ") or (raw_line.startswith("* ") and not raw_line.endswith("*")):
            bullet_text = clean_inline(raw_line[2:])
            formatted = f'<font color="#2980B9">&bull;</font> {bullet_text}'
            story.append(Paragraph(formatted, bullet_style))
            i += 1
            continue

        # Parágrafo comum
        p_text = clean_inline(raw_line)
        story.append(Paragraph(p_text, body_style))
        i += 1

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✅ Manual Técnico em PDF gerado com sucesso em: {output_pdf_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compilador do Manual Técnico e Arquitetural NOVA em PDF")
    parser.add_argument("--input", default="estudos/guia_estudos_nova/dossie_tecnico_completo.md", help="Arquivo Markdown de entrada")
    parser.add_argument("--output", default="estudos/guia_estudos_nova/Manual_Engenharia_e_Arquitetura_NOVA.pdf", help="Arquivo PDF de saída")

    args = parser.parse_args()
    compilar_manual_pdf(args.input, args.output)
