#!/usr/bin/env python3
"""
Generates a modern, elegant web portal index.html listing all compiled PDFs in dist/
"""
import os
import subprocess
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
PORTAL = ROOT / "portal"

def get_pdf_info(pdf_path):
    pages = 1
    try:
        res = subprocess.run(["pdfinfo", str(pdf_path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        for line in res.stdout.splitlines():
            if line.startswith("Pages:"):
                pages = int(line.split()[1])
                break
    except Exception:
        pass
    size_bytes = pdf_path.stat().st_size
    if size_bytes < 1024 * 1024:
        size_str = f"{size_bytes / 1024:.1f} Ko"
    else:
        size_str = f"{size_bytes / (1024 * 1024):.2f} Mo"
    return pages, size_str

def get_meta(rel_path):
    stem = rel_path.stem
    if "1AM" in str(rel_path) or "remediation" in stem:
        category = "1AM — Remédiation"
        title = "Livret de Remédiation Pédagogique (1AM)"
        desc = "Cahier complet de remédiation : 4 compétences disciplinaires, 14 fiches modernes prêtes à l'impression."
        icon = "fa-book"
        badge_color = "bg-blue-100 text-blue-800 border-blue-200"
    elif "verbe_etre_avoir" in stem:
        category = "Grammaire & Conjugaison"
        title = "Les Verbes ÊTRE et AVOIR au Présent"
        desc = "Fiche pédagogique complète avec activités d'entraînement + planche de 12 étiquettes mémo découpables pour les élèves."
        icon = "fa-spell-check"
        badge_color = "bg-teal-100 text-teal-800 border-teal-200"
    elif "template" in stem:
        category = "Modèle Reutilisable"
        title = "Gabarit Pédagogique Type (Template)"
        desc = "Modèle vierge structuré de 2 pages avec tous les composants (objectifs, activités, QCM, auto-évaluation)."
        icon = "fa-file-signature"
        badge_color = "bg-amber-100 text-amber-800 border-amber-200"
    else:
        category = "Ressource Pédagogique"
        title = stem.replace("_", " ").title()
        desc = "Document pédagogique officiel au format PDF haute fidélité."
        icon = "fa-file-pdf"
        badge_color = "bg-slate-100 text-slate-800 border-slate-200"
    return category, title, desc, icon, badge_color

def build_portal():
    if not DIST.exists():
        print("dist/ directory does not exist.")
        return

    # Find all PDFs under dist
    pdfs = []
    seen_names = set()
    for p in sorted(DIST.rglob("*.pdf")):
        # Skip duplicates like 1AM/remediation_1am.pdf if 1AM_remediation.pdf is primary
        rel = p.relative_to(DIST)
        if p.name in seen_names and ("remediation_1am.pdf" in p.name and "1AM_remediation.pdf" in seen_names):
            continue
        pages, size_str = get_pdf_info(p)
        cat, title, desc, icon, badge_color = get_meta(rel)
        seen_names.add(p.name)
        pdfs.append({
            "path": str(rel),
            "filename": p.name,
            "title": title,
            "category": cat,
            "desc": desc,
            "pages": pages,
            "size": size_str,
            "icon": icon,
            "badge_color": badge_color
        })

    cards_html = ""
    for item in pdfs:
        cards_html += f"""
        <div class="bg-white rounded-2xl p-6 shadow-sm hover:shadow-md transition-all duration-200 border border-slate-200/80 flex flex-col justify-between group">
          <div>
            <div class="flex items-center justify-between gap-2 mb-3">
              <span class="inline-flex items-center text-xs font-semibold px-2.5 py-1 rounded-full border {item['badge_color']}">
                {item['category']}
              </span>
              <span class="text-xs font-medium text-slate-400">
                <i class="fa-regular fa-file-lines mr-1"></i>{item['pages']} page{'s' if item['pages'] > 1 else ''} · {item['size']}
              </span>
            </div>
            <h3 class="text-lg font-bold text-slate-900 group-hover:text-sky-700 transition-colors mb-2">
              {item['title']}
            </h3>
            <p class="text-sm text-slate-600 line-clamp-3 mb-4">
              {item['desc']}
            </p>
          </div>
          <div class="pt-4 border-t border-slate-100 flex items-center gap-3">
            <a href="{item['path']}" target="_blank" class="flex-1 inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-sky-800 text-white text-sm font-semibold hover:bg-sky-900 transition-colors shadow-sm">
              <i class="fa-solid fa-eye text-xs"></i> Consulter
            </a>
            <a href="{item['path']}" download class="inline-flex items-center justify-center p-2.5 rounded-xl border border-slate-300 text-slate-700 hover:bg-slate-50 hover:text-slate-900 transition-colors" title="Télécharger">
              <i class="fa-solid fa-download"></i>
            </a>
          </div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="fr" class="h-full bg-slate-50">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Espace Pédagogique — Madame Lamia (Français)</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
  </style>
</head>
<body class="min-h-full flex flex-col text-slate-800 antialiased selection:bg-sky-500 selection:text-white">

  <!-- Header Banner -->
  <header class="bg-gradient-to-r from-sky-950 via-slate-900 to-indigo-950 text-white border-b border-sky-900/50">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-10">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-500/10 border border-sky-400/20 text-sky-300 text-xs font-semibold mb-3">
            <i class="fa-solid fa-feather-pointed"></i> Enseignement du Français · Année Scolaire 2026-2027
          </div>
          <h1 class="text-2xl sm:text-3xl font-extrabold tracking-tight text-white">
            Espace Pédagogique — Madame Lamia
          </h1>
          <p class="text-sm sm:text-base text-slate-300 mt-1 max-w-2xl">
            Référentiel des livrets de remédiation, fiches de langue et supports pédagogiques modernisés au format haute fidélité.
          </p>
        </div>
        <div class="flex items-center gap-3">
          <div class="bg-white/10 backdrop-blur-md px-4 py-2.5 rounded-2xl border border-white/10 text-center">
            <div class="text-xl font-extrabold text-white">{len(pdfs)}</div>
            <div class="text-[11px] font-medium text-sky-200 uppercase tracking-wider">Documents</div>
          </div>
        </div>
      </div>
    </div>
  </header>

  <!-- Main Content Grid -->
  <main class="flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-10">
    <!-- Action Bar -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
      <div>
        <h2 class="text-xl font-bold text-slate-900">Catalogue des Documents</h2>
        <p class="text-sm text-slate-500">Tous les fichiers sont compilés en PDF vectoriel prêt pour l'impression ou la projection.</p>
      </div>
      <div class="flex items-center gap-2">
        <span class="inline-flex items-center gap-1.5 text-xs font-medium text-emerald-700 bg-emerald-50 border border-emerald-200 px-3 py-1.5 rounded-full">
          <i class="fa-solid fa-circle-check text-[10px]"></i> Version TeX Live 2026 Validée
        </span>
      </div>
    </div>

    <!-- Cards Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {cards_html}
    </div>
  </main>

  <!-- Footer -->
  <footer class="bg-white border-t border-slate-200 py-6 text-center text-xs text-slate-500">
    <div class="max-w-6xl mx-auto px-4">
      <p>Système de Publication Pédagogique Lamia · LaTeX & Lamia-Pedagogy Design System · Généré automatiquement</p>
    </div>
  </footer>

</body>
</html>
"""
    portal_index = PORTAL / "index.html"
    dist_index = DIST / "index.html"
    with open(portal_index, "w", encoding="utf-8") as f:
        f.write(html)
    with open(dist_index, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated {portal_index} and {dist_index} with {len(pdfs)} documents.")

if __name__ == "__main__":
    build_portal()
