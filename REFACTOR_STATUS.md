# Lamia French Pedagogy Refactoring — Status & Roadmap

This document summarizes the completed modernization, modular competence architecture, and commands for Madame Lamia's French pedagogy workspace.

---

## 1. What Has Been Completed

1. **Audit & Inventory**:
   - Identified and preserved original LibreOffice sources: `Remediation 1AMTG.pdf` and `verbe etre et avoir au present.pdf`.
   - Identified 4 incoming scanned preparation documents in `new/` (`CamScanner 22-10-2026 ...`).
   - Cleaned build cruft (`*.aux`, `*.log`, `*.synctex.gz`, etc.).

2. **Standardized Directory Structure**:
   - `sty/`: Shared LaTeX packages and pedagogical design system (`lamia-pedagogy.sty`).
   - `assets/images/`: Centralized vector and photographic image assets.
   - `src/1AM/`: Modular, standalone 2-page documents for each 1AM competence:
     - `competence_01_oral.tex` : Compréhension & Expression Orales (2 pages)
     - `competence_02_lecture.tex` : Lecture & Phonétique + Planche Vignettes Gazelle (2 pages)
     - `competence_03_comprehension_ecrit.tex` : Compréhension de l'Écrit (2 pages)
     - `competence_04_production_ecrite.tex` : Production Écrite + Planche Billets Lion (2 pages)
   - `src/grammaire/`: Grammar and conjugation sheets (`verbe_etre_avoir.tex` — Lesson + Full-Page 8-card student memo sheet).
   - `src/templates/`: Reusable boilerplate templates for new courses (`course_template.tex` with `\modaliteSupportBar`).
   - `archive/original_pdfs/`: Safe storage for pre-refactor original files.
   - `archive/legacy_tex/`: Safe storage for early basic LaTeX drafts.
   - `dist/`: Dedicated folder for clean compiled PDFs and static web portal with zero duplicate files.
   - `portal/`: Web gallery generator and static frontend.
   - `.github/workflows/`: CI/CD pipeline for GitHub Pages deployment.

3. **Design System Extracted (`sty/lamia-pedagogy.sty`)**:
   - Packaged pedagogical colors (`primary`, `secondary`, `accent`, `emerald`, `amber`, `softred`, `primarylight`, `cardborder`).
   - Standardized typography (`helvet`, sans-serif, tight margins).
   - Core pedagogical macros created:
     - `\ficheHeader{Durée}{Date}{Niveau}{Année}`
     - `\competenceBanner{\faIcon\ Title}`
     - `\modaliteSupportBar{Modalité}{Support}` (work modality and support material pill)
     - `\badge[color]{Text}`
     - `\qcmCircle` (TikZ circle for student ticking)
     - `\cardOptTwo{a}{b}` & `\cardOptThree{a}{b}{c}` (aligned QCM option grids)
     - `\cutLineH` (dashed scissor cut marker with icon)
     - `\drule{width}` (custom dotted student answer line)
     - Automatic multi-path graphicspath resolution for images.

4. **Task Checklist**:
   - [x] **Modularize 1AM Competencies**:
     - Split into 4 focused 2-page documents with zero duplication.
     - Verified clean compilation into `dist/1AM/`.
   - [x] **Template & AI Agent Playbook**:
     - Updated `src/templates/course_template.tex` showcasing `\modaliteSupportBar`.
     - Documented macros in `AGENTS.md`.
   - [x] **Automated Build System & Cleanliness**:
     - `Makefile` compiles all documents into `dist/` and routes auxiliary files to `.build_cache/`.
     - Created comprehensive `.gitignore`.
   - [x] **Full-Page Student Cards (*Être & Avoir*)**:
     - Modernized Page 2 of `src/grammaire/verbe_etre_avoir.tex` into 8 large, highly readable student memo cards spanning the full A4 page.
   - [x] **Teacher Web Portal & CI/CD**:
     - Created `portal/generate_index.py` generating a clean, categorized web portal:
       - 1ère Année Moyenne (1AM) with the 4 competencies
       - Conjugaison & Grammaire
       - Modèles Enseignant
     - Configured `.github/workflows/deploy.yml` for automated GitHub Pages deployment.
   - [x] **Final Cleanup & Clean Git Commits**:
     - Removed obsolete 14-page duplicates.
     - Kept working tree clean and synchronized.

---

## 2. Directory Layout

```text
├── .github/
│   └── workflows/
│       └── deploy.yml                        # Automated GitHub Pages CI/CD
├── .gitignore                                # Ignore compiler cache & auxiliary files
├── AGENTS.md                                 # AI Agent instructions & macro reference
├── Makefile                                  # Multi-document build system
├── REFACTOR_STATUS.md                        # Project status and reference
├── archive/
│   ├── extracted_text.txt
│   ├── legacy_tex/                           # Remediation_1AMTG_basic.tex & pdf
│   └── original_pdfs/                        # Remediation_1AMTG.pdf, verbe_etre_et_avoir_au_present.pdf
├── assets/
│   └── images/                               # Centralized images (environement, lion, girafe, lavage, etc.)
├── dist/                                     # Pure compiled PDFs & portal (Zero duplicates)
│   ├── 1AM/
│   │   ├── competence_01_oral.pdf            # 2 pages
│   │   ├── competence_02_lecture.pdf         # 2 pages
│   │   ├── competence_03_comprehension_ecrit.pdf # 2 pages
│   │   └── competence_04_production_ecrite.pdf   # 2 pages
│   ├── grammaire/
│   │   └── verbe_etre_avoir.pdf              # 2 pages (Lesson + 8 Large Student Cards)
│   ├── templates/
│   │   └── course_template.pdf               # 2 pages
│   └── index.html                            # Teacher web portal
├── new/                                      # Raw inbound teacher scans (CamScanner)
├── portal/
│   ├── generate_index.py                     # Portal generator script
│   └── index.html
├── src/
│   ├── 1AM/
│   │   ├── competence_01_oral.tex
│   │   ├── competence_02_lecture.tex
│   │   ├── competence_03_comprehension_ecrit.tex
│   │   └── competence_04_production_ecrite.tex
│   ├── grammaire/
│   │   └── verbe_etre_avoir.tex
│   └── templates/
│       └── course_template.tex
└── sty/
    └── lamia-pedagogy.sty                    # Unified pedagogical LaTeX package
```

---

## 3. Quick Reference Commands

- `make` : Compiles all sources into `dist/` and refreshes the web portal.
- `make 1am` : Compiles all 1AM competence documents.
- `make portal` : Refreshes the HTML web portal.
- `make clean` : Clears `.build_cache/` without touching `dist/`.
- `make distclean` : Removes both `.build_cache/` and generated `dist/` outputs.
