#!/usr/bin/env python3
"""
Script de Padronização e Renomeação Retroativa de PDFs e Cover Letters
Ecossistema NOVA - Módulo de Carreira
"""

import os
import shutil
import glob

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VAGAS_DIR = os.path.join(BASE_DIR, "carreira/vagas_analisadas")

def padronizar():
    print("🔍 Iniciando varredura em:", VAGAS_DIR)
    
    # 1. Tech & Dev
    tech_dir = os.path.join(VAGAS_DIR, "tech_dev")
    if os.path.exists(tech_dir):
        for company in os.listdir(tech_dir):
            comp_path = os.path.join(tech_dir, company)
            if not os.path.isdir(comp_path):
                continue
            
            target_cv = "Curriculo_Fabio_Rodrigues_FullStack.pdf" if company == "fullstack" else "Curriculo_Fabio_Rodrigues_Java_Backend.pdf"
            
            # Renomeia ou consolida CVs
            cv_files = glob.glob(os.path.join(comp_path, "*curriculo*.pdf")) + glob.glob(os.path.join(comp_path, "*Curriculo*.pdf"))
            cv_files = list(set(cv_files))
            for f in cv_files:
                dest = os.path.join(comp_path, target_cv)
                if os.path.abspath(f) != os.path.abspath(dest):
                    print(f"Renomeando CV: {f} -> {dest}")
                    shutil.move(f, dest)
            
            # Renomeia Cover Letter docx
            docx_files = glob.glob(os.path.join(comp_path, "*cover_letter*.docx")) + glob.glob(os.path.join(comp_path, "*Cover_Letter*.docx"))
            docx_files = list(set(docx_files))
            for f in docx_files:
                dest = os.path.join(comp_path, "Cover_Letter_Fabio_Rodrigues.docx")
                if os.path.abspath(f) != os.path.abspath(dest):
                    print(f"Renomeando Cover Letter DOCX: {f} -> {dest}")
                    shutil.move(f, dest)

            # Renomeia Cover Letter pdf
            cov_pdf_files = glob.glob(os.path.join(comp_path, "*cover_letter*.pdf")) + glob.glob(os.path.join(comp_path, "*Cover_Letter*.pdf"))
            cov_pdf_files = list(set(cov_pdf_files))
            for f in cov_pdf_files:
                dest = os.path.join(comp_path, "Cover_Letter_Fabio_Rodrigues.pdf")
                if os.path.abspath(f) != os.path.abspath(dest):
                    print(f"Renomeando Cover Letter PDF: {f} -> {dest}")
                    shutil.move(f, dest)

    # 2. Marketing & Audiovisual
    mkt_dir = os.path.join(VAGAS_DIR, "marketing_audiovisual")
    if os.path.exists(mkt_dir):
        for company in os.listdir(mkt_dir):
            comp_path = os.path.join(mkt_dir, company)
            if not os.path.isdir(comp_path):
                continue
            
            target_cv = "Curriculo_Fabio_Rodrigues_Marketing_Design.pdf"
            
            # Renomeia ou consolida CVs
            cv_files = glob.glob(os.path.join(comp_path, "*curriculo*.pdf")) + glob.glob(os.path.join(comp_path, "*Curriculo*.pdf"))
            cv_files = list(set(cv_files))
            for f in cv_files:
                dest = os.path.join(comp_path, target_cv)
                if os.path.abspath(f) != os.path.abspath(dest):
                    print(f"Renomeando CV: {f} -> {dest}")
                    shutil.move(f, dest)

            # Renomeia Cover Letter docx
            docx_files = glob.glob(os.path.join(comp_path, "*cover_letter*.docx")) + glob.glob(os.path.join(comp_path, "*Cover_Letter*.docx"))
            docx_files = list(set(docx_files))
            for f in docx_files:
                dest = os.path.join(comp_path, "Cover_Letter_Fabio_Rodrigues.docx")
                if os.path.abspath(f) != os.path.abspath(dest):
                    print(f"Renomeando Cover Letter DOCX: {f} -> {dest}")
                    shutil.move(f, dest)

            # Renomeia Cover Letter pdf
            cov_pdf_files = glob.glob(os.path.join(comp_path, "*cover_letter*.pdf")) + glob.glob(os.path.join(comp_path, "*Cover_Letter*.pdf"))
            cov_pdf_files = list(set(cov_pdf_files))
            for f in cov_pdf_files:
                dest = os.path.join(comp_path, "Cover_Letter_Fabio_Rodrigues.pdf")
                if os.path.abspath(f) != os.path.abspath(dest):
                    print(f"Renomeando Cover Letter PDF: {f} -> {dest}")
                    shutil.move(f, dest)

    # 3. Suporte & Operações
    sup_dir = os.path.join(VAGAS_DIR, "suporte_operacoes")
    if os.path.exists(sup_dir):
        for company in os.listdir(sup_dir):
            comp_path = os.path.join(sup_dir, company)
            if not os.path.isdir(comp_path):
                continue
            
            target_cv = "Curriculo_Fabio_Rodrigues_Suporte_TI.pdf"
            
            cv_files = glob.glob(os.path.join(comp_path, "*curriculo*.pdf")) + glob.glob(os.path.join(comp_path, "*Curriculo*.pdf"))
            cv_files = list(set(cv_files))
            for f in cv_files:
                dest = os.path.join(comp_path, target_cv)
                if os.path.abspath(f) != os.path.abspath(dest):
                    print(f"Renomeando CV: {f} -> {dest}")
                    shutil.move(f, dest)

            docx_files = glob.glob(os.path.join(comp_path, "*cover_letter*.docx")) + glob.glob(os.path.join(comp_path, "*Cover_Letter*.docx"))
            docx_files = list(set(docx_files))
            for f in docx_files:
                dest = os.path.join(comp_path, "Cover_Letter_Fabio_Rodrigues.docx")
                if os.path.abspath(f) != os.path.abspath(dest):
                    print(f"Renomeando Cover Letter DOCX: {f} -> {dest}")
                    shutil.move(f, dest)

            cov_pdf_files = glob.glob(os.path.join(comp_path, "*cover_letter*.pdf")) + glob.glob(os.path.join(comp_path, "*Cover_Letter*.pdf"))
            cov_pdf_files = list(set(cov_pdf_files))
            for f in cov_pdf_files:
                dest = os.path.join(comp_path, "Cover_Letter_Fabio_Rodrigues.pdf")
                if os.path.abspath(f) != os.path.abspath(dest):
                    print(f"Renomeando Cover Letter PDF: {f} -> {dest}")
                    shutil.move(f, dest)

    print("✅ Padronização de nomes concluída em todas as pastas de vagas.")

if __name__ == "__main__":
    padronizar()
