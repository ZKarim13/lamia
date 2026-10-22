# Lamia French Pedagogy Refactoring — Status & Roadmap

This document summarizes the completed modernization, modular competence architecture, and commands for Madame Lamia's French pedagogy workspace.

---

## 1. What Has Been Completed

1. **Audit & Inventory**:
   - Identified and preserved original LibreOffice sources (`Remediation 1AMTG.pdf`, `verbe etre et avoir au present.pdf`).
   - Integrated full 29-page pedagogical binder from `new/CamScanner 22-10-2026 20.50.pdf`.
   - Cleaned build cruft (`*.aux`, `*.log`, `*.synctex.gz`, etc.).

2. **Standardized Directory Structure**:
   - `sty/`: Shared LaTeX packages and pedagogical design system (`lamia-pedagogy.sty`).
   - `assets/images/`: Centralized vector and photographic image assets (including `etapes_lavage_mains.png`, `caries_dents.png`, `savon_bulles.png`, `lavage_gestes.png`).
   - `src/1AM/sequence_01/`: The 8 official pedagogical sheets for **Projet 01 / Séquence 01 (L'Hygiène)**:
     - `P01_S01_01_oral_comprehension.tex` (2 pages)
     - `P01_S01_02_oral_production.tex` (2 pages)
     - `P01_S01_03_lecture_hygiene.tex` (2 pages)
     - `P01_S01_04_vocabulaire_definition.tex` (2 pages)
     - `P01_S01_05_grammaire_relative_qui.tex` (2 pages)
     - `P01_S01_06_conjugaison_present.tex` (2 pages)
     - `P01_S01_07_lecture_caries_dentaires.tex` (2 pages)
     - `P01_S01_08_production_ecrite.tex` (2 pages)
   - `src/1AM/`: Standalone 2-page documents for each 1AM remedial competence:
     - `competence_01_oral.tex` (2 pages)
     - `competence_02_lecture.tex` (2 pages)
     - `competence_03_comprehension_ecrit.tex` (2 pages)
     - `competence_04_production_ecrite.tex` (2 pages)
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
│   └── images/                               # Centralized images (etapes_lavage_mains, caries, lion, etc.)
├── dist/                                     # Pure compiled PDFs & portal (Zero duplicates)
│   ├── 1AM/
│   │   ├── sequence_01/                      # 8 official course sheets (2 pages each)
│   │   │   ├── P01_S01_01_oral_comprehension.pdf
│   │   │   ├── P01_S01_02_oral_production.pdf
│   │   │   ├── P01_S01_03_lecture_hygiene.pdf
│   │   │   ├── P01_S01_04_vocabulaire_definition.pdf
│   │   │   ├── P01_S01_05_grammaire_relative_qui.pdf
│   │   │   ├── P01_S01_06_conjugaison_present.pdf
│   │   │   ├── P01_S01_07_lecture_caries_dentaires.pdf
│   │   │   └── P01_S01_08_production_ecrite.pdf
│   │   ├── competence_01_oral.pdf            # 2 pages
│   │   ├── competence_02_lecture.pdf         # 2 pages
│   │   ├── competence_03_comprehension_ecrit.pdf # 2 pages
│   │   └── competence_04_production_ecrite.pdf   # 2 pages
│   ├── grammaire/
│   │   └── verbe_etre_avoir.pdf              # 2 pages (Lesson + 8 Large Student Cards)
│   ├── templates/
│   │   └── course_template.pdf               # 2 pages
│   └── index.html                            # Teacher web portal (14 documents)
├── new/
│   └── CamScanner 22-10-2026 20.50.pdf       # Raw consolidated scan
├── portal/
│   ├── generate_index.py                     # Portal generator script
│   └── index.html
├── src/
│   ├── 1AM/
│   │   ├── sequence_01/
│   │   │   ├── P01_S01_01_oral_comprehension.tex
│   │   │   ├── P01_S01_02_oral_production.tex
│   │   │   ├── P01_S01_03_lecture_hygiene.tex
│   │   │   ├── P01_S01_04_vocabulaire_definition.tex
│   │   │   ├── P01_S01_05_grammaire_relative_qui.tex
│   │   │   ├── P01_S01_06_conjugaison_present.tex
│   │   │   ├── P01_S01_07_lecture_caries_dentaires.tex
│   │   │   └── P01_S01_08_production_ecrite.tex
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
- `make 1am` : Compiles all 1AM documents.
- `make portal` : Refreshes the HTML web portal.
- `make clean` : Clears `.build_cache/` without touching `dist/`.
- `make distclean` : Removes both `.build_cache/` and generated `dist/` outputs.
