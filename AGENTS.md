# AI Agent Playbook — Lamia Pedagogy Workspace

This workspace is dedicated to modernizing, compiling, and managing pedagogical French teaching documents for Madame Lamia.

---

## ⚡ Core Rules for AI Agents

1. **TeX Live is Fully Installed**:
   - The complete TeX Live system with all necessary packages (`tcolorbox`, `fontawesome5`, `tikz`, `babel-french`, etc.) is installed and configured on the machine.
   - **Do NOT waste time testing whether packages exist or running exploratory package checks.**

2. **Standard Build System**:
   - Always compile documents using `make` (e.g. `make` to build everything, or `make <target>`).
   - All auxiliary files (`.aux`, `.log`, `.fls`, `.fdb_latexmk`) are kept strictly inside `.build_cache/`.
   - All output PDFs are placed inside `dist/`.

3. **Input Documents**:
   - New raw source material, scans, photos, or LibreOffice documents are placed in `new/`.
   - Never overwrite raw documents in `new/` or `archive/`.

4. **Document Output Paths**:
   - All new LaTeX source documents must be placed in `src/<category>/<doc>.tex`:
     - `src/1AM/` for 1ère Année Moyenne remediation or sequence documents.
     - `src/grammaire/` for grammar-specific lessons and exercise sheets.
     - `src/orthographe/` for spelling/phonetics lessons.
     - `src/conjugaison/` for conjugation sheets.
     - `src/templates/` for reusable templates.

5. **Mandatory Pedagogical Design System**:
   - Every `.tex` document must start with:
     ```latex
     \documentclass[a4paper,10pt]{article}
     \usepackage{lamia-pedagogy}

     \begin{document}
     ...
     \end{document}
     ```
   - **Do NOT re-declare** font setups, babel, colors, geometry, or custom macros in document headers. They are all standardized inside `sty/lamia-pedagogy.sty`.

6. **Image Assets**:
   - Central image assets live in `assets/images/`.
   - `lamia-pedagogy.sty` automatically configures `\graphicspath` to locate images in `assets/images/`, so you can include images using simply:
     `\includegraphics[options]{image_name.png}` or `\includegraphics[options]{images/image_name.png}`.

---

## 🛠 Available Pedagogical Macros

The `lamia-pedagogy` package provides:

| Macro | Description & Usage |
| :--- | :--- |
| `\ficheHeader{Durée}{Date}{Niveau}{Année}` | Standard metadata header bar with duration, date, level, and school year. |
| `\competenceBanner{<Icon> <Title>}` | Full-width navy title banner for the current competence/domain. |
| `\modaliteSupportBar{Modalité}{Support}` | Compact dual banner indicating student work modality and pedagogical support material. |
| `\badge[color]{Text}` | Rounded badge pill (colors: `primary`, `secondary`, `accent`, `emerald`, `amber`, `softred`). |
| `\qcmCircle` | TikZ circle checkbox for student tick answers in multiple-choice questions. |
| `\cardOptTwo{a}{b}` | Standardized 2-choice horizontal QCM grid. |
| `\cardOptThree{a}{b}{c}` | Standardized 3-choice horizontal QCM grid. |
| `\cutLineH` | Dashed horizontal scissor cut line for printable student exercise slips. |
| `\drule{width}` | Dotted fill line for student written responses. |

---

## 📋 Quick Commands

- `make` : Compiles all source documents and updates `dist/`.
- `make 1am` : Compiles only the 1AM remediation booklet.
- `make clean` : Cleans `.build_cache/` and temporary artifacts without deleting `dist/`.
- `make distclean` : Removes both `.build_cache/` and generated `dist/` PDFs.
