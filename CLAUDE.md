# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

Personal/lab academic website for **Jemin Lee (Efficient Computing Lab)**, built on the [al-folio](https://github.com/alshedivat/al-folio) Jekyll theme. Deployed at https://leejaymin.github.io via GitHub Pages (`gh-pages` branch). Source lives on `master`.

## Common Commands

### Local Development (Standard)

```bash
bundle install                    # install Ruby dependencies (first time only)
bundle exec jekyll serve          # serve at http://localhost:4000 with live reload
bundle exec jekyll build --lsi    # production-style build (matches CI; --lsi enables related posts)
```

### Local Development (Docker)

```bash
# Pre-built image from Docker Hub:
docker compose pull
docker compose up

# Or build/run locally with the included scripts:
./bin/docker_build_image.sh
./bin/docker_run.sh               # serves on :8080 with watch + livereload
```

Use `docker-compose.yml` for the prebuilt `amirpourmand/al-folio` image, or `docker-local.yml` to build from the local `Dockerfile`.

### CI / Deploy

- `bin/cibuild` — single command run by CI: `bundle exec jekyll build --lsi`.
- `.github/workflows/deploy.yml` — on push to `master`/`main`, builds with Ruby 3.2.2 and pushes `_site/` to `gh-pages` via `JamesIves/github-pages-deploy-action`.
- `bin/deploy` — manual deploy script (interactive; commits `_site/` onto a fresh `gh-pages` branch and force-pushes). Prefer the GitHub Action; only use this for emergency manual deploys.

## High-Level Architecture

This is a **Jekyll 4 site with `jekyll-scholar`** (BibTeX-driven publications). Content is data-first: authoring usually means editing YAML/BibTeX/Markdown, not code.

### Content Sources (where to edit what)

| What | Where | Notes |
|---|---|---|
| Publications | `_bibliography/papers.bib` | Rendered via `jekyll-scholar` on `_pages/publications.md`. `selected: true` highlights on the about page. Filtered keywords in `_config.yml:filtered_bibtex_keywords`. |
| News / announcements | `_news/*.md` | Each file is one news item; shown on the about page (limit set in `_config.yml:announcements`). |
| Projects | `_projects/*.md` | Rendered as cards on the projects page; categories controlled by front-matter. |
| Research entries | `_research/*.md` | Custom collection (see `_config.yml:collections`). |
| Blog posts | `_posts/YYYY-MM-DD-title.md` | Permalink `/blog/:year/:title/`. |
| Static pages | `_pages/*.md` | About, CV, publications, members, etc. — included via `include: ['_pages']`. |
| CV data | `_data/cv*.yml` (one per member: `cv_jemin.yml`, `cv_gihwan.yml`, ...) | Each maps to a matching layout `_layouts/cv_*.html` and is rendered into a per-member CV page. |
| Co-authors / venues / repos | `_data/coauthors.yml`, `_data/venues.yml`, `_data/repositories.yml` | Referenced from publications and the repositories page. |
| Site config | `_config.yml` | Title, social links, scholar settings, plugins, theme toggles. |

### Lab-Member CV System

CVs are member-scoped: every member has both a data file (`_data/cv_<name>.yml`) **and** a layout (`_layouts/cv_<name>.html`). When adding a new member, both must be created and the corresponding `_pages/<name>.md` (or members entry) wired up. The generic `_data/cv.yml` and `_layouts/cv.html` are the legacy single-CV path.

### Build Pipeline (key plugins)

- `jekyll-scholar` — BibTeX → publications page; `bibtex_filters` and `filtered_bibtex_keywords` strip internal-only fields (`abbr`, `award`, `selected`, `bibtex_show`, ...).
- `jekyll-imagemagick` — generates responsive WebP variants from `assets/img/*.{jpg,jpeg,png,tiff}`. Requires ImageMagick on the host (the Dockerfile installs it).
- `jekyll-jupyter-notebook` — renders `.ipynb` posts. CI also runs `pip3 install --upgrade jupyter`.
- `jekyll-diagrams` — supports mermaid/plantuml/etc.; CI installs `mermaid.cli` via npm.
- `jekyll-minifier` — HTML/CSS/JS minification on production builds (`JEKYLL_ENV=production`).
- `jekyll-archives` — generates `/blog/:year/`, `/blog/tag/:name/`, `/blog/category/:name/` archives.
- `jekyll-paginate-v2` — blog pagination.

### Output

- `_site/` is the build output. **Don't edit it** — it's regenerated on every build and deployed to `gh-pages` by CI.
- `.jekyll-cache/`, `.tweet-cache/` are caches; safe to delete.

## Conventions and Gotchas

- **Site language is English** (`lang: en`), but commit messages, news items, and other authoring content are often in Korean. Keep this mixed-language style when editing existing content.
- **Don't commit `Gemfile.lock` changes from inside Docker** — the docker scripts delete it before serving (`rm -f Gemfile.lock`) to avoid platform mismatches between host and container.
- **`_pages/dropdown.md`** defines a navbar dropdown; its `children` front-matter controls submenu links — adding a new top-level page may require editing this.
- **`max_author_limit: 10`** in `_config.yml` truncates publication author lists; click-to-expand is animated via JS (delay configured by `more_authors_animation_delay`).
- **Image preview field** in BibTeX entries (`preview: foo.jpg`) resolves against `assets/img/publication_preview/`.
- **Pre-commit hooks** (`.pre-commit-config.yaml`): trailing whitespace, EOF newline, YAML check, large-file check. Run `pre-commit install` once if working locally.
- **Custom plugins** live in `_plugins/` and are loaded automatically by Jekyll — check there before assuming a feature comes from the theme.

## Working on Publications

To add a paper:

1. Add a BibTeX entry to `_bibliography/papers.bib`. Required custom fields commonly used here:
   - `selected={true}` — feature on the about page.
   - `preview={image.jpg}` — thumbnail (place in `assets/img/publication_preview/`).
   - `abbr={ICML}`, `award={Best Paper}`, `bibtex_show={true}` — display options.
   - `pdf=`, `arxiv=`, `code=`, `slides=`, `poster=`, `html=` — link buttons.
2. Authors: if a co-author should link to a profile, ensure they exist in `_data/coauthors.yml`.
3. Venues: if it's a new venue, add to `_data/venues.yml` for consistent rendering.

Sorting is automatic by year (`group_by: year`, `group_order: descending` in `_config.yml`).
