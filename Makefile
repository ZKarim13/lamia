# Lamia French Pedagogy Makefile
SHELL := /bin/bash
export TEXINPUTS := .:$(CURDIR)/sty:$(CURDIR)/../sty:sty::

CACHE_DIR := .build_cache
DIST_DIR := dist
SRC_DIR := src

SRCS := $(shell find $(SRC_DIR) -name "*.tex")
PDFS := $(patsubst $(SRC_DIR)/%.tex,$(DIST_DIR)/%.pdf,$(SRCS))
1AM_SRCS := $(shell find $(SRC_DIR)/1AM -name "*.tex")
1AM_PDFS := $(patsubst $(SRC_DIR)/%.tex,$(DIST_DIR)/%.pdf,$(1AM_SRCS))

.PHONY: all build 1am clean distclean help portal

all: build

build: $(CACHE_DIR) $(DIST_DIR) $(PDFS) portal
	@echo "All documents compiled successfully into $(DIST_DIR)/"

$(CACHE_DIR):
	@mkdir -p $(CACHE_DIR)

$(DIST_DIR):
	@mkdir -p $(DIST_DIR)

# Pattern rule for compiling any src/**/*.tex into dist/**/*.pdf
# Auxiliary files are isolated strictly inside .build_cache/
$(DIST_DIR)/%.pdf: $(SRC_DIR)/%.tex $(CACHE_DIR) $(DIST_DIR) sty/lamia-pedagogy.sty
	@mkdir -p $(dir $@)
	@mkdir -p $(CACHE_DIR)/$(dir $*)
	@echo "--> Compiling $<..."
	@pdflatex -interaction=nonstopmode -output-directory=$(CACHE_DIR) -jobname=$(notdir $*) $< > /dev/null || (pdflatex -interaction=nonstopmode -output-directory=$(CACHE_DIR) -jobname=$(notdir $*) $< && exit 1)
	@cp $(CACHE_DIR)/$(notdir $*).pdf $@
	@echo "    [OK] Generated $@"

# Target specifically for 1AM competence documents
1am: $(CACHE_DIR) $(DIST_DIR) $(1AM_PDFS)
	@echo "1AM Competence documents up to date."

PASSWORD ?= karim2001

portal:
	@if [ -f portal/generate_index.py ]; then python3 portal/generate_index.py; fi
	@$(MAKE) encrypt

encrypt:
	@echo "--> Encrypting dist/index.html with StatiCrypt (Password: $(PASSWORD))..."
	@npx --yes staticrypt portal/index.html \
		-p "$(PASSWORD)" \
		-d ./$(DIST_DIR) \
		--short \
		--remember 30 \
		--template-title "Espace Pédagogique — Madame Lamia" \
		--template-instructions "Ressources pédagogiques réservées aux élèves et enseignants autorisés." \
		--template-placeholder "Mot de passe d'accès" \
		--template-button "Accéder aux cours" \
		--template-remember "Se souvenir de moi sur cet appareil (30 jours)" \
		--template-error "Mot de passe incorrect !" \
		--template-color-primary "#182b49" \
		--template-color-secondary "#0d9488"
	@echo "    [OK] Encrypted portal written to $(DIST_DIR)/index.html"

serve:
	@echo "Serving $(DIST_DIR) at http://localhost:8080 (Press Ctrl+C to stop)..."
	@python3 -m http.server 8080 -d $(DIST_DIR)

clean:
	@echo "Cleaning temporary build cache..."
	@rm -rf $(CACHE_DIR)
	@rm -f *.aux *.log *.fls *.fdb_latexmk *.synctex.gz *.out *.toc
	@find $(SRC_DIR) -name "*.aux" -o -name "*.log" | xargs rm -f 2>/dev/null || true
	@find $(DIST_DIR) -name "*.aux" -o -name "*.log" | xargs rm -f 2>/dev/null || true
	@echo "Build cache cleaned."

distclean: clean
	@echo "Cleaning dist directory..."
	@rm -rf $(DIST_DIR)/*
	@echo "Dist directory cleaned."

help:
	@echo "Lamia French Pedagogy Build Commands:"
	@echo "  make          - Compile all LaTeX documents into $(DIST_DIR)/"
	@echo "  make 1am      - Compile only the 1AM Competence sheets"
	@echo "  make portal   - Regenerate the HTML web portal"
	@echo "  make clean    - Remove compiler cache and auxiliary files"
	@echo "  make distclean- Remove compiler cache and all compiled PDFs"
