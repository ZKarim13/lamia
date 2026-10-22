#!/usr/bin/env python3
"""
Generates an elegant, teacher-friendly web portal (index.html)
categorizing documents clearly by grade level, sequence, and domain.
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

    # SEQUENCE 01 DOCUMENTS
    if "P01_S01_01" in stem:
        return {
            "group": "1AM_SEQ1",
            "badge": "Séance 01 · Oral",
            "badge_color": "bg-sky-50 text-sky-700 border-sky-200",
            "title": "Compréhension de l'Oral : Le lavage des mains",
            "desc": "Support d'écoute transcrit « Selon M. Pompe », découverte du thème des microbes et questionnaire des 3 écoutes méthodiques.",
            "icon": "fa-headphones"
        }
    elif "P01_S01_02" in stem:
        return {
            "group": "1AM_SEQ1",
            "badge": "Séance 02 · Oral",
            "badge_color": "bg-indigo-50 text-indigo-700 border-indigo-200",
            "title": "Production de l'Oral : Les 5 étapes du lavage",
            "desc": "Manuel p. 10. Support iconique illustré des 5 étapes chronologiques, boîte à outils lexicale et jeu de rôle en binôme.",
            "icon": "fa-comments"
        }
    elif "P01_S01_03" in stem:
        return {
            "group": "1AM_SEQ1",
            "badge": "Séance 03 · Lecture",
            "badge_color": "bg-emerald-50 text-emerald-700 border-emerald-200",
            "title": "Compréhension de l'Écrit (01) : Gestes d'hygiène",
            "desc": "Texte explicatif sur l'hygiène corporelle, identification des microbes, questions à choix multiples et définition du lavage.",
            "icon": "fa-book-open"
        }
    elif "P01_S01_04" in stem:
        return {
            "group": "1AM_SEQ1",
            "badge": "Séance 04 · Vocabulaire",
            "badge_color": "bg-amber-50 text-amber-700 border-amber-200",
            "title": "Vocabulaire : La Définition et la Synonymie",
            "desc": "Procédés explicatifs essentiels en 1AM. Verbes introducteurs (être, consister à), règle des synonymes et exercices d'application.",
            "icon": "fa-spell-check"
        }
    elif "P01_S01_05" in stem:
        return {
            "group": "1AM_SEQ1",
            "badge": "Séance 05 · Grammaire",
            "badge_color": "bg-blue-50 text-blue-700 border-blue-200",
            "title": "Grammaire : La Subordonnée Relative par « qui »",
            "desc": "Construction de la phrase complexe explicative. Identification de l'antécédent, rôle du pronom « qui » et suppression des répétitions.",
            "icon": "fa-project-diagram"
        }
    elif "P01_S01_06" in stem:
        return {
            "group": "1AM_SEQ1",
            "badge": "Séance 06 · Conjugaison",
            "badge_color": "bg-rose-50 text-rose-700 border-rose-200",
            "title": "Conjugaison : Le Présent des Verbes en -ER",
            "desc": "Présent de l'indicatif des verbes du 1er groupe liés à l'hygiène (laver, brosser, nettoyer, rincer) et règles d'accord sujet-verbe.",
            "icon": "fa-pencil-ruler"
        }
    elif "P01_S01_07" in stem:
        return {
            "group": "1AM_SEQ1",
            "badge": "Séance 07 · Lecture",
            "badge_color": "bg-teal-50 text-teal-700 border-teal-200",
            "title": "Compréhension de l'Écrit (02) : Les caries dentaires",
            "desc": "Manuel p. 26. Analyse scientifique des causes de la carie, tableau des 3 phases du texte explicatif et schémas dentaires.",
            "icon": "fa-tooth"
        }
    elif "P01_S01_08" in stem:
        return {
            "group": "1AM_SEQ1",
            "badge": "Séance 08 · Écrit",
            "badge_color": "bg-purple-50 text-purple-700 border-purple-200",
            "title": "Production Écrite (1er Jet) : Texte sur l'hygiène",
            "desc": "Situation d'intégration (journal du collège). Reconstitution de phrases, grille des critères de réussite et espace d'écriture guidé.",
            "icon": "fa-pen-fancy"
        }

    # REMEDIATION COMPETENCIES
    elif "competence_01" in stem:
        return {
            "group": "1AM_REMED",
            "badge": "Remédiation · Oral",
            "badge_color": "bg-blue-50 text-blue-700 border-blue-200",
            "title": "Compétence 01 : Compréhension & Expression Orales",
            "desc": "Fiche enseignant (thème de l'hygiène et dialogue) + Fiche élève découpable en 2 colonnes A5 avec QCM illustrés.",
            "icon": "fa-headphones"
        }
    elif "competence_02" in stem:
        return {
            "group": "1AM_REMED",
            "badge": "Remédiation · Lecture",
            "badge_color": "bg-emerald-50 text-emerald-700 border-emerald-200",
            "title": "Compétence 02 : Lecture & Phonétique",
            "desc": "Fiche de lecture expressive (La gazelle) + Planche de 15 vignettes découpables du schéma anatomique.",
            "icon": "fa-book-open"
        }
    elif "competence_03" in stem:
        return {
            "group": "1AM_REMED",
            "badge": "Remédiation · Écrit",
            "badge_color": "bg-teal-50 text-teal-700 border-teal-200",
            "title": "Compétence 03 : Compréhension de l'Écrit",
            "desc": "Fiche d'analyse textuelle structurée (Phase 1 : Repérage et axes de lecture + Phase 2 : Activités de consolidation).",
            "icon": "fa-book-reader"
        }
    elif "competence_04" in stem:
        return {
            "group": "1AM_REMED",
            "badge": "Remédiation · Production",
            "badge_color": "bg-amber-50 text-amber-700 border-amber-200",
            "title": "Compétence 04 : Production Écrite",
            "desc": "Fiche enseignant et critères d'évaluation + Planche de 6 billets de rédaction (Le lion) prêts à découper.",
            "icon": "fa-pen-fancy"
        }

    # OTHER MODULES
    elif "verbe_etre_avoir" in stem:
        return {
            "group": "Grammaire",
            "badge": "Conjugaison · Grammaire",
            "badge_color": "bg-purple-50 text-purple-700 border-purple-200",
            "title": "Les Verbes ÊTRE et AVOIR au Présent",
            "desc": "Fiche de cours avec 4 activités + Planche plein format A4 de 8 grandes étiquettes mémo découpables pour les élèves.",
            "icon": "fa-spell-check"
        }
    elif "template" in stem:
        return {
            "group": "Templates",
            "badge": "Gabarit Enseignant",
            "badge_color": "bg-slate-100 text-slate-700 border-slate-300",
            "title": "Gabarit Type de Fiche Pédagogique",
            "desc": "Modèle standard 2 pages avec métadonnées, barre modalité/support, mémo, QCM et grille d'auto-évaluation.",
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

    groups = {"1AM_SEQ1": [], "1AM_REMED": [], "Grammaire": [], "Templates": [], "Autres": []}
    
    for p in sorted(DIST.rglob("*.pdf")):
        rel = p.relative_to(DIST)
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
            Fiches de cours officielles, livrets de remédiation et supports pédagogiques prêts à l'impression.
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
  <main class="flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-12">

    <!-- Section 1 : Séquence 01 (Projet 1) -->
    <section>
      <div class="flex items-center gap-3 pb-3 mb-5 border-b border-slate-200">
        <span class="inline-flex items-center justify-center w-8 h-8 rounded-lg bg-sky-800 text-white font-bold text-sm">
          P1
        </span>
        <div>
          <h2 class="text-lg font-bold text-slate-900">1ère Année Moyenne — Projet 01 / Séquence 01 : L'Hygiène Corporelle</h2>
          <p class="text-xs text-slate-500">Les 8 séances officielles de la séquence : de la compréhension orale à la production écrite finale.</p>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        {render_cards(groups["1AM_SEQ1"])}
      </div>
    </section>

    <!-- Section 2 : Remédiation 1AM -->
    <section>
      <div class="flex items-center gap-3 pb-3 mb-5 border-b border-slate-200">
        <span class="inline-flex items-center justify-center w-8 h-8 rounded-lg bg-teal-800 text-white font-bold text-sm">
          REM
        </span>
        <div>
          <h2 class="text-lg font-bold text-slate-900">1ère Année Moyenne — Livret de Remédiation par Compétence</h2>
          <p class="text-xs text-slate-500">Documents modulaires de 2 pages pour les séances de soutien et de remédiation pédagogique.</p>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        {render_cards(groups["1AM_REMED"])}
      </div>
    </section>

    <!-- Section 3 : Conjugaison & Grammaire -->
    <section>
      <div class="flex items-center gap-3 pb-3 mb-5 border-b border-slate-200">
        <span class="inline-flex items-center justify-center w-8 h-8 rounded-lg bg-purple-800 text-white font-bold text-sm">
          <i class="fa-solid fa-spell-check text-xs"></i>
        </span>
        <div>
          <h2 class="text-lg font-bold text-slate-900">Grammaire & Conjugaison (Fiches Spécifiques)</h2>
          <p class="text-xs text-slate-500">Leçons synthétiques et étiquettes mémo découpables pour les cahiers des élèves.</p>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        {render_cards(groups["Grammaire"])}
      </div>
    </section>

    <!-- Section 4 : Modèles Pédagogiques -->
    <section>
      <div class="flex items-center gap-3 pb-3 mb-5 border-b border-slate-200">
        <span class="inline-flex items-center justify-center w-8 h-8 rounded-lg bg-slate-700 text-white font-bold text-sm">
          <i class="fa-solid fa-shapes text-xs"></i>
        </span>
        <div>
          <h2 class="text-lg font-bold text-slate-900">Gabarits & Modèles (Templates)</h2>
          <p class="text-xs text-slate-500">Modèle standardisé pour composer de nouvelles fiches d'activités.</p>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
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
