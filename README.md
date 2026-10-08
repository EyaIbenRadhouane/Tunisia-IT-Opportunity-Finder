# Tunisia IT Opportunity Finder

> Find your next IT opportunity in Tunisia.

Plateforme de recherche de stages PFE et d'emplois dans le domaine informatique en Tunisie : collecte d'offres issues de sources autorisées, nettoyage et normalisation, recherche par région / domaine / technologie / type, dashboard d'analyse, puis NLP, clustering et matching profil ↔ offres.

**Statut : en cours de développement (Version 1, étape 1 : cadrage).**

## Problème

Les offres IT sont dispersées sur plusieurs sites, les intitulés varient pour un même métier, les localisations et compétences ne sont pas normalisées. Le candidat perd du temps à multiplier les recherches.

## Architecture

```
Sources autorisées → Collector → Raw data → Cleaning → Normalization → SQLite
                                                                         │
                                                      ┌──────────────────┴─────────────┐
                                                      ▼                                ▼
                                              NLP / ML (TF-IDF, K-Means)      Application Streamlit
                                                                              (recherche, dashboard,
                                                                               clusters, matching)
```

## Stack

Python 3.11+, requests, BeautifulSoup, pandas, SQLite, scikit-learn, Streamlit, Plotly.

## Structure

```
data/raw/          offres brutes (jamais modifiées)
data/reference/    governorates.json, domains.json, skills.json
collectors/        un script par source
pipeline/          nettoyage, normalisation, chargement en base
ml/                NLP, clustering, matching
app/               application Streamlit
notebooks/         exploration et analyses
docs/              schémas et captures
```

## Feuille de route

- [ ] **V1** : collecte, nettoyage, normalisation, base SQLite, recherche, dashboard
- [ ] **V2** : NLP, TF-IDF, K-Means, visualisation des clusters, clusters par région
- [ ] **V3** : matching profil ↔ offres, finitions, déploiement

## Installation

```bash
git clone <url-du-depot>
cd tunisia-it-opportunity-finder
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

## Éthique de la collecte

- Seules des sources autorisées sont utilisées (vérification du `robots.txt` et des conditions d'utilisation).
- Pause de 2 à 3 secondes entre deux requêtes.
- Seules les informations publiques de l'offre et le lien vers l'annonce originale sont conservés.
- LinkedIn et Indeed ne sont pas collectés.

## Ce que j'apprends (journal)

- *À compléter à chaque étape.*
