#!/usr/bin/env python3
"""
Compilador de Manual Técnico & Arquitetural em PDF — Ecossistema NOVA
Diagramação de nível sênior: Componentes nativos ReportLab, zero vazamento de margens,
tabelas dimensionadas com auto-wrap de texto, conversão de diagramas e equações formatadas.
"""

import os
import sys
import re
import argparse
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether, Table, TableStyle, Preformatted, PageBreak
)
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 42.5  # 15mm
USABLE_WIDTH = 510.0  # Largura útil estrita da página

class NumberedCanvas(canvas.Canvas):
    """Numeração de páginas executiva (Página X de Y) e cabeçalhos corporativos."""
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
        self.setFillColor(colors.HexColor("#64748B"))

        # Cabeçalho a partir da página 2
        if self._pageNumber > 1:
            self.drawString(MARGIN, PAGE_HEIGHT - 32, "NOVA • MANUAL DE ENGENHARIA & ARQUITETURA DE SOFTWARE")
            self.drawRightString(PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 32, "Java 21 • Clean Architecture • v3.6")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(MARGIN, PAGE_HEIGHT - 38, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 38)

        # Rodapé em todas as páginas
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(MARGIN, 38, PAGE_WIDTH - MARGIN, 38)
        self.drawString(MARGIN, 28, "Ecossistema NOVA • Fábio Rodrigues | Java 21 • Spring Boot 3.3 • Spring AI MCP")
        self.drawRightString(PAGE_WIDTH - MARGIN, 28, f"Página {self._pageNumber} de {page_count}")
        self.restoreState()


def clean_inline(text: str) -> str:
    """Higieniza marcações markdown inline, tags HTML e fórmulas para o ReportLab."""
    if not text:
        return ""

    # Remove emojis customizados
    custom_symbols = [
        "■", "▪", "▫", "🔹", "🔸", "📍", "📧", "📱", "💼", "💻", "🚀", "🌌",
        "🎙️", "🎙", "🎓", "🎯", "🛠️", "🛠", "🔍", "⚡", "📅", "📝", "📊",
        "💡", "⚪", "🟢", "🟡", "❌", "🌟", "✨", "🔗", "⭐", "🏷️", "🏷", "🍩", "💰", "✉️", "📚", "☕", "🍃", "🏛️", "🏛", "🧪", "💾", "🤖", "🐍", "📑", "🔴", "🔵", "💳", "☁️", "🧭"
    ]
    for sym in custom_symbols:
        text = text.replace(sym, "")

    emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
    text = emoji_pattern.sub('', text)

    # Remove tags HTML residuais (<img...>, <div>, etc.)
    text = re.sub(r'<img\s+[^>]*>', '', text)
    text = re.sub(r'</?(?:div|span|p|a|details|summary)[^>]*>', '', text)

    # Conversão de fórmulas matemáticas LaTeX em notação legível
    text = re.sub(r'\$\$\\text\{([^}]+)\}\s*=\s*\\frac\{([^}]+)\}\{([^}]+)\}\$\$', r'<b>\1</b> = (\2) / (\3)', text)
    text = re.sub(r'\$\$([^\$]+)\$\$', r'<b>\1</b>', text)
    text = re.sub(r'\\text\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1) / (\2)', text)
    text = text.replace(r'\times', '×').replace(r'\sum', 'Soma de')

    # Links markdown [Texto](url) -> Texto
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)

    # Negrito e Itálico
    text = re.sub(r'\*\*\*([^\*]+)\*\*\*', r'<b><i>\1</i></b>', text)
    text = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*([^\*]+)\*', r'<i>\1</i>', text)

    # Código inline `code`
    text = re.sub(r'`([^`]+)`', r'<font face="Courier" color="#0F172A"><b>\1</b></font>', text)

    # Limpeza de múltiplos espaços
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def calculate_col_widths(num_cols: int, sample_rows: list) -> list:
    """Calcula larguras proporcionais para colunas garantindo total exato de 510 pt."""
    if num_cols == 1:
        return [USABLE_WIDTH]
    elif num_cols == 2:
        return [160.0, 350.0]
    elif num_cols == 3:
        return [130.0, 200.0, 180.0]
    elif num_cols == 4:
        return [110.0, 130.0, 140.0, 130.0]
    elif num_cols == 5:
        return [90.0, 110.0, 80.0, 110.0, 120.0]
    else:
        width = USABLE_WIDTH / num_cols
        return [width] * num_cols


def compilar_manual_pdf(markdown_path: str, output_pdf_path: str):
    if not os.path.exists(markdown_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {markdown_path}")

    with open(markdown_path, "r", encoding="utf-8") as f:
        content = f.read()

    os.makedirs(os.path.dirname(os.path.abspath(output_pdf_path)), exist_ok=True)

    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN
    )

    styles = getSampleStyleSheet()

    PRIMARY = colors.HexColor('#0F172A')       # Slate 900
    SECONDARY = colors.HexColor('#1E293B')     # Slate 800
    ACCENT = colors.HexColor('#2563EB')        # Blue 600
    BORDER_COLOR = colors.HexColor('#CBD5E1')  # Slate 300
    BG_CARD = colors.HexColor('#F8FAFC')       # Slate 50
    CODE_BG = colors.HexColor('#F1F5F9')       # Slate 100

    doc_title_style = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=PRIMARY,
        alignment=1,
        spaceAfter=4
    )
    doc_sub_style = ParagraphStyle(
        'DocSub',
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=ACCENT,
        alignment=1,
        spaceAfter=3
    )
    doc_meta_style = ParagraphStyle(
        'DocMeta',
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor('#64748B'),
        alignment=1,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'H1',
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=PRIMARY,
        spaceBefore=12,
        spaceAfter=4,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'H2',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=ACCENT,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )
    h3_style = ParagraphStyle(
        'H3',
        fontName='Helvetica-Bold',
        fontSize=9.2,
        leading=12.5,
        textColor=SECONDARY,
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=8.2,
        leading=12,
        textColor=SECONDARY,
        spaceAfter=4
    )
    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    bullet_style = ParagraphStyle(
        'Bullet',
        fontName='Helvetica',
        fontSize=8.2,
        leading=12,
        textColor=SECONDARY,
        leftIndent=12,
        spaceAfter=3
    )
    code_style = ParagraphStyle(
        'CodeStyle',
        fontName='Courier',
        fontSize=7,
        leading=9.2,
        textColor=PRIMARY
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
            if i < len(lines) and (lines[i].strip().startswith("**") or lines[i].strip().startswith("Dossiê")):
                sub_text = clean_inline(lines[i].strip())
                story.append(Paragraph(sub_text, doc_sub_style))
                i += 1

            if i < len(lines) and (lines[i].strip().startswith("*") or lines[i].strip().startswith("Autor")):
                meta_text = clean_inline(lines[i].strip())
                story.append(Paragraph(meta_text, doc_meta_style))
                i += 1

            story.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT, spaceAfter=8))
            header_done = True
            continue

        # Título de Capítulo H1 (# ...)
        if raw_line.startswith("# ") and header_done:
            chap_text = clean_inline(raw_line[2:])
            heading_elem = KeepTogether([
                Paragraph(chap_text, h1_style),
                HRFlowable(width="100%", thickness=0.8, color=PRIMARY, spaceAfter=5)
            ])
            story.append(heading_elem)
            i += 1
            continue

        # Subtítulo H2 (## ...)
        if raw_line.startswith("## "):
            sec_text = clean_inline(raw_line[3:])
            heading_elem = KeepTogether([
                Paragraph(sec_text, h2_style),
                HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR, spaceAfter=4)
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

        # Bloco de Imagem HTML (<img ...>) ou Tabela de Imagem
        if "<img" in raw_line:
            caption_para = Paragraph("<b>Visualização de Interface:</b> NOVA Control Center — Layouts Executivos em Tema Claro (Light) e Escuro (Dark) com Living Shader WebGL e Design System Material 3 Expressive.", body_style)
            t_box = Table([[caption_para]], colWidths=[USABLE_WIDTH])
            t_box.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), BG_CARD),
                ('BOX', (0, 0), (-1, -1), 0.8, BORDER_COLOR),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ]))
            story.append(Spacer(1, 3))
            story.append(t_box)
            story.append(Spacer(1, 4))
            i += 1
            continue

        # Bloco de Código (```...)
        if raw_line.startswith("```"):
            lang = raw_line[3:].strip().lower()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # pula fechamento de ```

            # Tratamento Especial: Diagrama Mermaid -> Matriz Estruturada em Tabela
            if "mermaid" in lang or any("flowchart" in cl for cl in code_lines):
                diag_data = [
                    [
                        Paragraph("<b>Camada</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
                        Paragraph("<b>Componentes & Tecnologias</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
                        Paragraph("<b>Responsabilidade no Ecossistema</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white))
                    ],
                    [
                        Paragraph("<b>UI Layer</b>", body_bold),
                        Paragraph("NOVA Control Center (Render / localhost:3000)<br/>Voice Studio (:5050)<br/>Chat CLI (/ e !)<br/>Túnel HTTPS (/compartilhar)", body_style),
                        Paragraph("Interfaces visuais, dashboard SPA em 7 abas, living shader WebGL e interação por voz neural.", body_style)
                    ],
                    [
                        Paragraph("<b>Orquestrador</b>", body_bold),
                        Paragraph("MAIN Agent (NOVA Orchestrator)<br/>Roteador Semântico com Fallback 3 Níveis", body_style),
                        Paragraph("Triagem inteligente de comandos, regras de ouro, checkpoints e delegação para especialistas.", body_style)
                    ],
                    [
                        Paragraph("<b>Agentes</b>", body_bold),
                        Paragraph("💰 Agente Financeiro<br/>💼 Agente Carreira 360°<br/>💻 Agente Código (Java 21)<br/>📚 Agente Estudos (DIO)", body_style),
                        Paragraph("CFO algorítmico preditivo, esteira de vagas em 3 trilhas, Clean Architecture e mentoria técnica.", body_style)
                    ],
                    [
                        Paragraph("<b>Backend & Dados</b>", body_bold),
                        Paragraph("Spring Boot 3.3.3 API (:8081)<br/>Spring AI MCP Tools (@Tool)<br/>Banco H2 ACID (financiadb.mv.db)<br/>Motor Gráfico (chart_engine.py)", body_style),
                        Paragraph("Persistência transacional ACID, ProblemDetail RFC 7807, ferramentas corporativas e relatórios visuais.", body_style)
                    ]
                ]
                t_diag = Table(diag_data, colWidths=[80, 215, 215])
                t_diag.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
                    ('BOX', (0, 0), (-1, -1), 0.8, BORDER_COLOR),
                    ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_CARD])
                ]))
                story.append(Spacer(1, 4))
                story.append(t_diag)
                story.append(Spacer(1, 6))
                continue

            # Código Comum: Envoltório seguro que quebra linhas longas
            wrapped_code_lines = []
            for c_line in code_lines:
                while len(c_line) > 68:
                    wrapped_code_lines.append(c_line[:68])
                    c_line = "    " + c_line[68:]
                wrapped_code_lines.append(c_line)

            code_text = "\n".join(wrapped_code_lines)
            code_para = Preformatted(code_text, code_style)
            
            code_table = Table([[code_para]], colWidths=[USABLE_WIDTH])
            code_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), CODE_BG),
                ('BOX', (0, 0), (-1, -1), 0.6, BORDER_COLOR),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))
            story.append(Spacer(1, 2))
            story.append(code_table)
            story.append(Spacer(1, 4))
            continue

        # Linha Horizontal (---)
        if raw_line == "---":
            story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR, spaceBefore=4, spaceAfter=6))
            i += 1
            continue

        # Tabela Markdown (| col1 | col2 | ...)
        if raw_line.startswith("|") and "|" in raw_line[1:]:
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            
            rows_data = []
            for t_line in table_lines:
                # Ignora tags de imagem dentro de linhas de tabela
                if "<img" in t_line:
                    continue
                cells = [c.strip() for c in t_line.split("|")[1:-1]]
                # Ignora linhas separadoras markdown (|---|---|)
                if all(re.match(r'^:?-+:?$', c) for c in cells if c):
                    continue
                if any(cells):
                    rows_data.append(cells)
            
            if rows_data:
                num_cols = max(len(r) for r in rows_data)
                col_widths = calculate_col_widths(num_cols, rows_data)
                
                table_flowables = []
                for row_idx, row in enumerate(rows_data):
                    flowable_row = []
                    is_header = (row_idx == 0)
                    for c_idx, cell in enumerate(row):
                        cell_cleaned = clean_inline(cell)
                        if is_header:
                            p = Paragraph(f"<b>{cell_cleaned}</b>", ParagraphStyle('TH_Dynamic', fontName='Helvetica-Bold', fontSize=8, leading=10.5, textColor=colors.white))
                        else:
                            p = Paragraph(cell_cleaned, ParagraphStyle('TD_Dynamic', fontName='Helvetica', fontSize=7.6, leading=10.5, textColor=SECONDARY))
                        flowable_row.append(p)
                    while len(flowable_row) < num_cols:
                        flowable_row.append(Paragraph("", body_style))
                    table_flowables.append(flowable_row)
                
                t = Table(table_flowables, colWidths=col_widths)
                t_style = [
                    ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
                    ('BOX', (0, 0), (-1, -1), 0.8, BORDER_COLOR),
                    ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
                    ('TOPPADDING', (0, 0), (-1, -1), 3.5),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ]
                for r_idx in range(1, len(table_flowables)):
                    if r_idx % 2 == 1:
                        t_style.append(('BACKGROUND', (0, r_idx), (-1, r_idx), BG_CARD))
                t.setStyle(TableStyle(t_style))
                story.append(Spacer(1, 3))
                story.append(t)
                story.append(Spacer(1, 5))
            continue

        # Bullets (- ... ou • ... ou * ...)
        if raw_line.startswith("- ") or raw_line.startswith("• ") or (raw_line.startswith("* ") and not raw_line.endswith("*")):
            bullet_text = clean_inline(raw_line[2:])
            formatted = f'<font color="#2563EB">&bull;</font> {bullet_text}'
            story.append(Paragraph(formatted, bullet_style))
            i += 1
            continue

        # Parágrafo comum
        p_text = clean_inline(raw_line)
        if p_text:
            story.append(Paragraph(p_text, body_style))
        i += 1

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✅ Manual Técnico em PDF gerado com sucesso em: {output_pdf_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compilador do Manual Técnico e Arquitetural NOVA em PDF")
    parser.add_argument("--input", default="estudos/guia_estudos_nova/Manual_Engenharia_e_Arquitetura_NOVA.md", help="Arquivo Markdown de entrada")
    parser.add_argument("--output", default="docs/Manual_Engenharia_e_Arquitetura_NOVA.pdf", help="Arquivo PDF de saída")

    args = parser.parse_args()
    compilar_manual_pdf(args.input, args.output)
    
    # Sincroniza também com estudos/guia_estudos_nova se a saída padrão docs/ foi usada
    if args.output == "docs/Manual_Engenharia_e_Arquitetura_NOVA.pdf":
        alt_path = "estudos/guia_estudos_nova/Manual_Engenharia_e_Arquitetura_NOVA.pdf"
        os.makedirs(os.path.dirname(alt_path), exist_ok=True)
        shutil.copyfile(args.output, alt_path)
        print(f"✅ Cópia sincronizada em: {alt_path}")
