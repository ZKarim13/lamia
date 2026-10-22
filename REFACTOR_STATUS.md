# Lamia French Pedagogy Refactoring — Status & Roadmap

This document summarizes the completed modernization, repository architecture, and commands for Madame Lamia's French pedagogy workspace.

---

## 1. What Has Been Completed

1. **Audit & Inventory**:
   - Identified and preserved original LibreOffice sources: `Remediation 1AMTG.pdf` and `verbe etre et avoir au present.pdf`.
   - Identified 4 incoming scanned preparation documents in `new/` (`CamScanner 22-10-2026 ...`).
   - Cleaned build cruft (`*.aux`, `*.log`, `*.synctex.gz`, etc.).

2. **Standardized Directory Structure**:
   - `sty/`: Shared LaTeX packages and pedagogical design system (`lamia-pedagogy.sty`).
   - `assets/images/`: Centralized vector and photographic image assets.
   - `src/1AM/`: Production LaTeX source documents for 1AM (`remediation_1am.tex`).
   - `src/grammaire/`: Grammar and conjugation lesson sheets (`verbe_etre_avoir.tex`).
   - `src/templates/`: Reusable boilerplate templates for new courses (`course_template.tex`).
   - `archive/original_pdfs/`: Safe storage for pre-refactor original files.
   - `archive/legacy_tex/`: Safe storage for early basic LaTeX drafts.
   - `dist/`: Dedicated folder for final, clean compiled PDFs and static web portal.
   - `portal/`: Web gallery generator and static frontend.
   - `.github/workflows/`: CI/CD pipeline for GitHub Pages deployment.

3. **Design System Extracted (`sty/lamia-pedagogy.sty`)**:
   - Packaged pedagogical colors (`primary`, `secondary`, `accent`, `emerald`, `amber`, `softred`, `primarylight`, `cardborder`).
   - Standardized typography (`helvet`, sans-serif, tight margins).
   - Core pedagogical macros created:
     - `\ficheHeader{Durée}{Date}{Niveau}{Année}`
     - `\competenceBanner{\faIcon\ Title}`
     - `\badge[color]{Text}`
     - `\qcmCircle` (TikZ circle for student ticking)
     - `\cardOptTwo{a}{b}` & `\cardOptThree{a}{b}{c}` (aligned QCM option grids)
     - `\cutLineH` (dashed scissor cut marker with icon)
     - `\drule{width}` (custom dotted student answer line)
     - Automatic multi-path graphicspath resolution for images.

4. **Task Checklist**:
   - [x] **Task 1: Complete Course Source Migration**:
     - Created `src/1AM/remediation_1am.tex` powered by `\usepackage{lamia-pedagogy}`.
     - Verified clean compilation into `dist/1AM_remediation.pdf` (14 pages).
   - [x] **Task 2: Template & AI Agent Playbook**:
     - Created `src/templates/course_template.tex` (2-page reusable template).
     - Created `AGENTS.md` at root with clear build and contribution rules for AI agents.
   - [x] **Task 3: Root Makefile & `.gitignore`**:
     - Created automated `Makefile` with targets (`all`, `build`, `1am`, `portal`, `clean`, `distclean`).
     - Kept build artifacts strictly inside `.build_cache/` so `dist/` contains only pure PDFs.
     - Created comprehensive `.gitignore`.
   - [x] **Task 4: Modernize Remaining Courses**:
     - Created `src/grammaire/verbe_etre_avoir.tex` modernizing `verbe_etre_et_avoir_au_present.pdf` into a 2-page document (lesson + 12 printable pocket cutout slips).
     - Inspected and cataloged all 4 scanned binder documents in `new/`.
   - [x] **Task 5: Sharing Hub & CI/CD Pipeline**:
     - Created `.github/workflows/deploy.yml` for automated GitHub Pages compilation and deployment.
     - Created `portal/index.html` & `portal/generate_index.py` (responsive, elegant teacher portal with direct preview and download buttons).
   - [x] **Task 6: Final Cleanup & Clean Git Init**:
     - Removed obsolete root files and temporary compiler artifacts.
     - Verified all PDFs in `dist/`.
     - Initialized fresh Git repository with clean root commit.

---

## 2. Directory Layout

```text
├── .github/
│   └── workflows/
│       └── deploy.yml              # Automated GitHub Pages CI/CD
├── .gitignore                      # Ignore compiler cache & auxiliary files
├── AGENTS.md                       # AI Agent instructions & standard rules
├── Makefile                        # Multi-document build system
├── REFACTOR_STATUS.md              # Project status and reference
├── archive/
│   ├── extracted_text.txt
│   ├── legacy_tex/                 # Remediation_1AMTG_basic.tex & pdf
│   └── original_pdfs/              # Remediation_1AMTG.pdf, verbe_etre_et_avoir_au_present.pdf
├── assets/
│   └── images/                     # Centralized images (environement, lion, girafe, lavage, etc.)
├── dist/                           # Pure compiled PDFs & portal
│   ├── 1AM/
│   │   └── remediation_1am.pdf     # 14-page Remediation booklet
│   ├── 1AM_remediation.pdf
│   ├── grammaire/
│   │   └── verbe_etre_avoir.pdf    # 2-page Lesson + 12 Cutout Slips
│   ├── templates/
│   │   └── course_template.pdf     # 2-page Starting Template
│   └── index.html                  # Teacher web portal
├── new/                            # Raw inbound teacher scans (CamScanner)
├── portal/
│   ├── generate_index.py           # Portal generator script
│   └── index.html
├── src/
│   ├── 1AM/
│   │   └── remediation_1am.tex
│   ├── grammaire/
│   │   └── verbe_etre_avoir.tex
│   └── templates/
│       └── course_template.tex
└── sty/
    └── lamia-pedagogy.sty          # Unified pedagogical LaTeX package
```

---

## 3. Quick Reference Commands

- `make` : Compiles all sources into `dist/` and refreshes the web portal.
- `make 1am` : Compiles only the 14-page 1AM Remediation booklet.
- `make portal` : Refreshes the HTML web portal.
- `make clean` : Clears `.build_cache/` without touching `dist/`.
- `make distclean` : Removes both `.build_cache/` and generated `dist/` outputs.
