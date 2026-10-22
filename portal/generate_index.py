#!/usr/bin/env python3
"""
Generates an elegant, teacher-friendly web portal (index.html)
categorizing documents clearly by grade level and domain.
"""
import os
import subprocess
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
        size_str = f"{size_bytes / 1024:.0f} Ko"
    else:
        size_str = f"{size_bytes / (1024 * 1024):.2f} Mo"
    return pages, size_str

def get_doc_metadata(rel_path):
    stem = rel_path.stem
    p_str = str(rel_path)

    if "competence_01" in stem:
        return {
            "group": "1AM",
            "badge": "1AM · Oral",
            "badge_color": "bg-blue-50 text-blue-700 border-blue-200",
            "title": "Compétence 01 : Compréhension & Expression Orales",
            "desc": "Fiche enseignant (thème de l'hygiène et dialogue) + Fiche élève découpable en 2 colonnes A5 avec QCM illustrés.",
            "icon": "fa-headphones"
        }
    elif "competence_02" in stem:
        return {
            "group": "1AM",
            "badge": "1AM · Lecture",
            "badge_color": "bg-emerald-50 text-emerald-700 border-emerald-200",
            "title": "Compétence 02 : Lecture & Phonétique",
            "desc": "Fiche de lecture expressive (texte de la gazelle) + Planche de 15 vignettes du schéma de la gazelle à découper.",
            "icon": "fa-book-open"
        }
    elif "competence_03" in stem:
        return {
            "group": "1AM",
            "badge": "1AM · Écrit",
            "badge_color": "bg-teal-50 text-teal-700 border-teal-200",
            "title": "Compétence 03 : Compréhension de l'Écrit",
            "desc": "Fiche d'analyse textuelle structurée (Phase 1 : Repérage et axes de lecture + Phase 2 : Activités de consolidation).",
            "icon": "fa-book-reader"
        }
    elif "competence_04" in stem:
        return {
            "group": "1AM",
            "badge": "1AM · Production",
            "badge_color": "bg-amber-50 text-amber-700 border-amber-200",
            "title": "Compétence 04 : Production Écrite",
            "desc": "Fiche enseignant et critères d'évaluation + Planche de 6 billets de rédaction (Le lion) prêts à découper.",
            "icon": "fa-pen-fancy"
        }
    elif "verbe_etre_avoir" in stem:
        return {
            "group": "Grammaire",
            "badge": "Conjugaison · Grammaire",
            "badge_color": "bg-purple-50 text-purple-700 border-purple-200",
            "title": "Les Verbes ÊTRE et AVOIR au Présent",
            "desc": "Fiche de cours avec 4 activités d'application + Planche plein format A4 de 8 grandes étiquettes mémo découpables pour les élèves.",
            "icon": "fa-spell-check"
        }
    elif "template" in stem:
        return {
            "group": "Templates",
            "badge": "Gabarit Enseignant",
            "badge_color": "bg-slate-100 text-slate-700 border-slate-300",
            "title": "Gabarit Type de Fiche Pédagogique",
            "desc": "Modèle standard 2 pages avec en-tête métadonnées, barre modalité/support, mémo, QCM et grille d'auto-évaluation.",
            "icon": "fa-file-lines"
        }
    else:
        return {
            "group": "Autres",
            "badge": "Document",
            "badge_color": "bg-slate-50 text-slate-700 border-slate-200",
            "title": stem.replace("_", " ").title(),
            "desc": "Document pédagogique prêt pour l'impression.",
            "icon": "fa-file-pdf"
        }

def render_cards(docs):
    html = ""
    for d in docs:
        html += f"""
        <div class="bg-white rounded-xl p-5 shadow-sm hover:shadow-md transition-all duration-200 border border-slate-200 flex flex-col justify-between group">
          <div>
            <div class="flex items-center justify-between gap-2 mb-2.5">
              <span class="inline-flex items-center text-xs font-semibold px-2.5 py-0.5 rounded-full border {d['badge_color']}">
                {d['badge']}
              </span>
              <span class="text-xs text-slate-400 font-medium">
                <i class="fa-regular fa-file-pdf mr-1"></i>{d['pages']} p. · {d['size']}
              </span>
            </div>
            <h4 class="text-base font-bold text-slate-900 group-hover:text-sky-800 transition-colors mb-2 leading-snug">
              {d['title']}
            </h4>
            <p class="text-xs text-slate-600 leading-relaxed mb-4">
              {d['desc']}
            </p>
          </div>
          <div class="pt-3 border-t border-slate-100 flex items-center gap-2">
            <a href="{d['path']}" target="_blank" class="flex-1 inline-flex items-center justify-center gap-1.5 px-3 py-2 rounded-lg bg-sky-800 text-white text-xs font-semibold hover:bg-sky-900 transition-colors shadow-sm">
              <i class="fa-solid fa-eye text-[11px]"></i> Consulter
            </a>
            <a href="{d['path']}" download class="inline-flex items-center justify-center p-2 rounded-lg border border-slate-200 text-slate-600 hover:bg-slate-50 hover:text-slate-900 transition-colors" title="Télécharger">
              <i class="fa-solid fa-download text-xs"></i>
            </a>
          </div>
        </div>
        """
    return html

def build_portal():
    if not DIST.exists():
        return

    # Find all PDFs under dist (excluding duplicates)
    groups = {"1AM": [], "Grammaire": [], "Templates": [], "Autres": []}
    
    for p in sorted(DIST.rglob("*.pdf")):
        rel = p.relative_to(DIST)
        # Skip root aliases if any
        if p.parent == DIST:
            continue
        pages, size_str = get_pdf_info(p)
        meta = get_doc_metadata(rel)
        meta["path"] = str(rel)
        meta["pages"] = pages
        meta["size"] = size_str
        groups[meta["group"]].append(meta)

    total_docs = sum(len(v) for v in groups.values())

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
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-7 sm:py-9">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-500/10 border border-sky-400/20 text-sky-300 text-xs font-semibold mb-2.5">
            <i class="fa-solid fa-feather-pointed"></i> Enseignement du Français · Année Scolaire 2026-2027
          </div>
          <h1 class="text-2xl sm:text-3xl font-extrabold tracking-tight text-white">
            Espace Pédagogique — Madame Lamia
          </h1>
          <p class="text-sm text-slate-300 mt-1">
            Fiches de remédiation par compétence, leçons de grammaire et supports prêts pour impression.
          </p>
        </div>
        <div class="flex items-center gap-3">
          <div class="bg-white/10 backdrop-blur-md px-4 py-2 rounded-xl border border-white/10 text-center">
            <div class="text-xl font-extrabold text-white">{total_docs}</div>
            <div class="text-[10px] font-medium text-sky-200 uppercase tracking-wider">Fiches Prêtes</div>
          </div>
        </div>
      </div>
    </div>
  </header>

  <!-- Main Content -->
  <main class="flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-10">

    <!-- Section 1 : 1ère Année Moyenne (1AM) -->
    <section>
      <div class="flex items-center gap-3 pb-3 mb-5 border-b border-slate-200">
        <span class="inline-flex items-center justify-center w-8 h-8 rounded-lg bg-sky-800 text-white font-bold text-sm">
          1AM
        </span>
        <div>
          <h2 class="text-lg font-bold text-slate-900">1ère Année Moyenne — Fiches de Remédiation par Compétence</h2>
          <p class="text-xs text-slate-500">Chaque compétence est un document autonome de 2 pages (Fiche enseignant + Fiche élève découpable).</p>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        {render_cards(groups["1AM"])}
      </div>
    </section>

    <!-- Section 2 : Conjugaison & Grammaire -->
    <section>
      <div class="flex items-center gap-3 pb-3 mb-5 border-b border-slate-200">
        <span class="inline-flex items-center justify-center w-8 h-8 rounded-lg bg-purple-800 text-white font-bold text-sm">
          <i class="fa-solid fa-spell-check text-xs"></i>
        </span>
        <div>
          <h2 class="text-lg font-bold text-slate-900">Grammaire & Conjugaison</h2>
          <p class="text-xs text-slate-500">Leçons synthétiques, exercices d'application et étiquettes mémo découpables pour les élèves.</p>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {render_cards(groups["Grammaire"])}
      </div>
    </section>

    <!-- Section 3 : Modèles Pédagogiques -->
    <section>
      <div class="flex items-center gap-3 pb-3 mb-5 border-b border-slate-200">
        <span class="inline-flex items-center justify-center w-8 h-8 rounded-lg bg-slate-700 text-white font-bold text-sm">
          <i class="fa-solid fa-shapes text-xs"></i>
        </span>
        <div>
          <h2 class="text-lg font-bold text-slate-900">Gabarits & Modèles (Templates)</h2>
          <p class="text-xs text-slate-500">Boîte à outils et modèle standardisé pour composer de nouvelles fiches d'activités.</p>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {render_cards(groups["Templates"])}
      </div>
    </section>

  </main>

  <!-- Footer -->
  <footer class="bg-white border-t border-slate-200 py-5 text-center text-xs text-slate-500">
    <div class="max-w-6xl mx-auto px-4">
      <p>Système de Publication Pédagogique Lamia · LaTeX & Lamia-Pedagogy Design System · Mis à jour automatiquement</p>
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
    print(f"Generated {portal_index} and {dist_index} with {total_docs} documents.")

if __name__ == "__main__":
    build_portal()
