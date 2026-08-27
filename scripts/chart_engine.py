#!/usr/bin/env python3
"""
Motor Central de Gráficos (Chart Engine) — Ecossistema NOVA
Suporte a Gráficos Executivos para Carreira e Finanças via Matplotlib
"""

import os
import matplotlib
matplotlib.use('Agg')  # Modo sem interface gráfica
import matplotlib.pyplot as plt
import numpy as np

# Estilo e Paleta de Cores NOVA Executiva
COLOR_PRIMARY = "#1A2530"       # Navy Charcoal
COLOR_ACCENT_BLUE = "#2980B9"   # Azul Corporativo
COLOR_ACCENT_GREEN = "#27AE60"  # Verde Sucesso / Receitas
COLOR_ACCENT_RED = "#C0392B"    # Vermelho Alerta / Despesas
COLOR_ACCENT_ORANGE = "#E67E22" # Laranja Atenção / Parcial
COLOR_MUTED_GRAY = "#BDC3C7"    # Cinza Claro
COLOR_BG_CARD = "#F8F9F9"       # Fundo Leve
COLOR_TEXT = "#2C3E50"          # Texto Principal

def apply_global_styles():
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Helvetica', 'Arial', 'DejaVu Sans'],
        'text.color': COLOR_TEXT,
        'axes.labelcolor': COLOR_TEXT,
        'xtick.color': COLOR_TEXT,
        'ytick.color': COLOR_TEXT,
        'figure.facecolor': 'white',
        'axes.facecolor': 'white',
        'axes.edgecolor': COLOR_MUTED_GRAY,
        'axes.linewidth': 0.8
    })

def gerar_grafico_match(competencias_dict: dict, output_path: str):
    """
    Gera gráfico de barras horizontais comparando exigências da vaga vs competência no NOVA.
    competencias_dict formato: {'Java 21 / Spring Boot': (100, 100), 'Clean Architecture': (90, 100), ...}
    tupla: (nivel_candidato_pct, exigencia_vaga_pct)
    """
    apply_global_styles()
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    skills = list(competencias_dict.keys())
    candidato_scores = [competencias_dict[s][0] for s in skills]
    vaga_reqs = [competencias_dict[s][1] for s in skills]

    y_pos = np.arange(len(skills))
    bar_height = 0.35

    fig, ax = plt.subplots(figsize=(8, max(4.5, len(skills) * 0.6)), dpi=300)

    # Barras de Exigência da Vaga (fundo / base)
    rects1 = ax.barh(y_pos - bar_height/2, vaga_reqs, bar_height, label='Exigência da Vaga', color=COLOR_MUTED_GRAY, alpha=0.6)
    # Barras de Nível Candidato / NOVA
    colors_bars = [COLOR_ACCENT_GREEN if score >= req else COLOR_ACCENT_ORANGE for score, req in zip(candidato_scores, vaga_reqs)]
    rects2 = ax.barh(y_pos + bar_height/2, candidato_scores, bar_height, label='Competência NOVA', color=colors_bars)

    ax.set_xlabel('Aderência & Nível Técnico (%)', fontsize=10, fontweight='bold', labelpad=8)
    ax.set_title('Aderência Técnica: Exigências da Vaga vs Portfólio NOVA', fontsize=12, fontweight='bold', pad=14, color=COLOR_PRIMARY)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(skills, fontsize=9.5, fontweight='medium')
    ax.set_xlim(0, 115)
    ax.invert_yaxis()  # Exibe de cima para baixo
    ax.legend(loc='lower right', frameon=True, facecolor=COLOR_BG_CARD, edgecolor=COLOR_MUTED_GRAY, fontsize=9)
    ax.grid(axis='x', linestyle='--', alpha=0.5)

    # Rótulos de porcentagem nas barras
    for rect, score in zip(rects2, candidato_scores):
        width = rect.get_width()
        ax.text(width + 2, rect.get_y() + rect.get_height()/2, f'{score}%', ha='left', va='center', fontsize=8.5, fontweight='bold', color=COLOR_PRIMARY)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"📊 Gráfico de Match gerado em: {output_path}")

def gerar_grafico_salario(faixa_min: float, media: float, pretensao: float, teto: float, output_path: str, cargo: str = "Backend Java Pleno"):
    """
    Gera régua de posicionamento salarial em relação ao mercado.
    """
    apply_global_styles()
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 2.4), dpi=300)

    # Barra contínua de mercado
    ax.barh(0, teto - faixa_min, left=faixa_min, height=0.25, color=COLOR_MUTED_GRAY, alpha=0.35, label='Faixa de Mercado')
    ax.barh(0, media - faixa_min, left=faixa_min, height=0.25, color="#AED6F1", alpha=0.6, label='Faixa Média')

    # Marcadores verticais
    ax.axvline(faixa_min, color="#7F8C8D", linestyle=":", linewidth=1.2)
    ax.text(faixa_min, 0.18, f'Mínimo\nR$ {faixa_min:,.0f}', ha='center', va='bottom', fontsize=7.5, color="#7F8C8D")

    ax.axvline(media, color=COLOR_ACCENT_BLUE, linestyle="--", linewidth=1.8)
    ax.text(media, 0.18, f'Média Mercado\nR$ {media:,.0f}', ha='center', va='bottom', fontsize=8, fontweight='bold', color=COLOR_ACCENT_BLUE)

    ax.axvline(teto, color="#7F8C8D", linestyle=":", linewidth=1.2)
    ax.text(teto, 0.18, f'Teto\nR$ {teto:,.0f}', ha='center', va='bottom', fontsize=7.5, color="#7F8C8D")

    # Ponto da Pretensão
    ax.scatter([pretensao], [0], color=COLOR_ACCENT_GREEN, s=160, zorder=5, edgecolors=COLOR_PRIMARY, linewidth=1.5)
    ax.text(pretensao, -0.22, f'Pretensão Alvo: R$ {pretensao:,.0f}', ha='center', va='top', fontsize=8.5, fontweight='bold', color=COLOR_ACCENT_GREEN)

    ax.set_title(f'Posicionamento Salarial: {cargo}', fontsize=10.5, fontweight='bold', pad=22, color=COLOR_PRIMARY)
    ax.set_yticks([])
    ax.set_ylim(-0.55, 0.55)
    ax.set_xlim(faixa_min * 0.85, teto * 1.15)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(COLOR_MUTED_GRAY)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"💰 Gráfico Salarial gerado em: {output_path}")

def gerar_grafico_despesas_categoria(categoria_map: dict, output_path: str, mes_ano: str = "Agosto/2026"):
    """
    Gera gráfico de rosca (Donut chart) da distribuição percentual de despesas.
    categoria_map: {'MORADIA': 550.0, 'ALIMENTACAO': 345.5, ...}
    """
    apply_global_styles()
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    labels = list(categoria_map.keys())
    values = list(categoria_map.values())
    total = sum(values)

    palette = ['#2980B9', '#27AE60', '#E67E22', '#8E44AD', '#D35400', '#16A085', '#34495E', '#F39C12']
    colors_pie = palette[:len(labels)]

    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)

    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors_pie,
        pctdistance=0.75,
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2)
    )

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(8.5)
        autotext.set_fontweight('bold')

    for text in texts:
        text.set_fontsize(9)
        text.set_color(COLOR_TEXT)

    # Texto no centro da rosca
    ax.text(0, 0, f'Total Gastos\nR$ {total:,.2f}', ha='center', va='center', fontsize=10, fontweight='bold', color=COLOR_PRIMARY)
    ax.set_title(f'Distribuição de Despesas por Categoria — {mes_ano}', fontsize=12, fontweight='bold', pad=12, color=COLOR_PRIMARY)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"🍩 Gráfico de Despesas gerado em: {output_path}")

def gerar_grafico_balanco(receitas: float, despesas: float, saldo: float, output_path: str, mes_ano: str = "Agosto/2026"):
    """
    Gera gráfico de barras executivo comparando Receitas, Despesas e Saldo Líquido.
    """
    apply_global_styles()
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    categorias = ['Receitas', 'Despesas', 'Saldo Líquido']
    valores = [receitas, despesas, saldo]
    cores = [COLOR_ACCENT_GREEN, COLOR_ACCENT_RED, COLOR_ACCENT_BLUE]

    fig, ax = plt.subplots(figsize=(6.5, 4), dpi=300)

    bars = ax.bar(categorias, valores, color=cores, width=0.48, edgecolor=COLOR_PRIMARY, linewidth=0.8)

    ax.set_ylabel('Valor (R$)', fontsize=10, fontweight='bold')
    ax.set_title(f'Balanço Financeiro Consolidado — {mes_ano}', fontsize=12, fontweight='bold', pad=14, color=COLOR_PRIMARY)
    ax.set_ylim(0, max(valores) * 1.25)
    ax.grid(axis='y', linestyle='--', alpha=0.4)

    # Rótulos sobre as barras
    for bar, val in zip(bars, valores):
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + (max(valores) * 0.03), f'R$ {val:,.2f}', ha='center', va='bottom', fontsize=9.5, fontweight='bold', color=COLOR_PRIMARY)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"📊 Gráfico de Balanço gerado em: {output_path}")

def gerar_grafico_portfolio_match(dados_portfolio: dict, output_path: str):
    """
    Gera gráfico visual de adequação criativa e alinhamento dos cases de portfólio audiovisual.
    dados_portfolio: {'Institucional / Governo (DER-PE)': 95, 'Viral / Engajamento (Gildo Lanches)': 96, ...}
    """
    apply_global_styles()
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    cases = list(dados_portfolio.keys())
    scores = list(dados_portfolio.values())

    y_pos = np.arange(len(cases))
    bar_height = 0.45

    fig, ax = plt.subplots(figsize=(8, max(3.8, len(cases) * 0.52)), dpi=300)

    # Cores personalizadas elegantes
    colors_bars = [COLOR_ACCENT_GREEN if s >= 92 else COLOR_ACCENT_BLUE for s in scores]

    rects = ax.barh(y_pos, scores, bar_height, color=colors_bars, edgecolor=COLOR_PRIMARY, linewidth=0.6, alpha=0.9)

    ax.set_xlabel('Aderência Criativa & Relevância Prática (%)', fontsize=9.5, fontweight='bold', labelpad=8)
    ax.set_title('Auditoria de Portfólio: Adequação dos Cases vs Demandas da Vaga', fontsize=11.5, fontweight='bold', pad=12, color=COLOR_PRIMARY)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(cases, fontsize=9, fontweight='medium')
    ax.set_xlim(0, 115)
    ax.invert_yaxis()
    ax.grid(axis='x', linestyle='--', alpha=0.5)

    for rect, score in zip(rects, scores):
        width = rect.get_width()
        ax.text(width + 2, rect.get_y() + rect.get_height()/2, f'{score}%', ha='left', va='center', fontsize=8.5, fontweight='bold', color=COLOR_PRIMARY)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"🎬 Gráfico de Portfólio Match gerado em: {output_path}")

if __name__ == "__main__":
    print("Testing Chart Engine...")
    test_dir = "carreira/scripts/test_charts"
    os.makedirs(test_dir, exist_ok=True)

    test_skills = {
        'Java 21 / Spring Boot 3': (100, 100),
        'Clean Architecture / SOLID': (100, 90),
        'TDD (JUnit 5 / Mockito)': (100, 95),
        'Spring AI (MCP Server)': (100, 80),
        'PostgreSQL / Relacional': (95, 90),
        'TypeScript / Prototipagem': (90, 85),
        'Inglês Avançado': (95, 90)
    }
    gerar_grafico_match(test_skills, f"{test_dir}/match_test.png")
    gerar_grafico_salario(6000, 8500, 9000, 12000, f"{test_dir}/salario_test.png")
    gerar_grafico_despesas_categoria({'ALIMENTACAO': 450.0, 'MORADIA': 600.0, 'TRANSPORTE': 200.0, 'LAZER': 150.0}, f"{test_dir}/despesas_test.png")
    gerar_grafico_balanco(2299.00, 1709.77, 589.23, f"{test_dir}/balanco_test.png")
    print("All test charts generated successfully!")
