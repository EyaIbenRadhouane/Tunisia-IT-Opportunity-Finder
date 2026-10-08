import json
import re
import unicodedata
from pathlib import Path


REFERENCE_DIR = Path(__file__).resolve().parent.parent / "data" / "reference"

# Les 24 gouvernorats et les 8 domaines attendus par le cahier des charges
EXPECTED_GOVERNORATES = [
    "Tunis", "Ariana", "Ben Arous", "Manouba", "Nabeul", "Zaghouan", "Bizerte",
    "Béja", "Jendouba", "Le Kef", "Siliana", "Sousse", "Monastir", "Mahdia",
    "Sfax", "Kairouan", "Kasserine", "Sidi Bouzid", "Gabès", "Medenine",
    "Tataouine", "Gafsa", "Tozeur", "Kébili",
]
EXPECTED_DOMAINS = [
    "Development", "AI & Data", "Cybersecurity", "Cloud & DevOps",
    "Mobile", "QA", "Database", "UI/UX",
]

# Lit data/reference/<name>.json et renvoie un dictionnaire.
def load_json(name):
    with open(REFERENCE_DIR / f"{name}.json", encoding="utf-8") as f:
        return json.load(f)

#	Met en minuscules, enlève les accents et la ponctuation, pour comparer des textes de façon équitable
def normalize_text(text):
    text = unicodedata.normalize("NFD", str(text))
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = re.sub(r"[,;:()\[\]\-–/|]", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip()


#Cherche un mot entier (« java » n’est pas trouvé dans « javascript »)
def contains_term(text, term):
    """Vrai si 'term' apparaît comme un mot entier dans 'text' (déjà normalisé).
    Évite les faux positifs : 'java' n'est pas trouvé dans 'javascript'."""
    pattern = r"(?<!\w)" + re.escape(term) + r"(?!\w)"
    return re.search(pattern, text) is not None



def find_governorate(location):
    """'Sahloul - Sousse' -> 'Sousse'. Renvoie None si rien n'est reconnu.
    Si plusieurs lieux sont trouvés, on garde le plus long (le plus précis)."""
    text = normalize_text(location)
    best, best_len = None, 0
    for governorate, places in load_json("governorates").items():
        for place in places:
            p = normalize_text(place)
            if len(p) > best_len and contains_term(text, p):
                best, best_len = governorate, len(p)
    return best


def find_domain(title):
    """'Machine Learning Intern' -> 'AI & Data'.
    L'ordre du fichier domains.json compte : les domaines précis sont testés
    avant 'Development', qui est volontairement le dernier (le plus général)."""
    text = normalize_text(title)
    for domain, keywords in load_json("domains").items():
        if any(contains_term(text, normalize_text(k)) for k in keywords):
            return domain
    return None


def find_skills(text):
    """'Python, SQL et ML' -> ['Python', 'SQL', 'Machine Learning']."""
    text = normalize_text(text)
    found = []
    for skill, synonyms in load_json("skills").items():
        if any(contains_term(text, normalize_text(s)) for s in synonyms):
            found.append(skill)
    return found


def check_reference_files():
    """Contrôle de qualité des 3 fichiers. Renvoie la liste des problèmes."""
    problems = []

    gov = load_json("governorates")
    for g in EXPECTED_GOVERNORATES:
        if g not in gov:
            problems.append(f"Gouvernorat manquant : {g}")
    for g in gov:
        if g not in EXPECTED_GOVERNORATES:
            problems.append(f"Gouvernorat inattendu : {g}")
    seen = {}
    for g, places in gov.items():
        if not places:
            problems.append(f"Aucune localité pour {g}")
        for p in places:
            key = normalize_text(p)
            if key in seen and seen[key] != g:
                problems.append(f"Localité ambiguë '{p}' : {seen[key]} et {g}")
            seen[key] = g

    dom = load_json("domains")
    for d in EXPECTED_DOMAINS:
        if d not in dom:
            problems.append(f"Domaine manquant : {d}")
    if list(dom)[-1] != "Development":
        problems.append("'Development' doit rester le dernier domaine du fichier")

    skills = load_json("skills")
    seen = {}
    for s, syns in skills.items():
        for syn in syns:
            key = normalize_text(syn)
            if key in seen and seen[key] != s:
                problems.append(f"Synonyme '{syn}' présent dans {seen[key]} et {s}")
            seen[key] = s

    return problems


if __name__ == "__main__":
    gov = load_json("governorates")
    print(f"Gouvernorats : {len(gov)}")
    print(f"Localités    : {sum(len(v) for v in gov.values())}")
    print(f"Domaines     : {len(load_json('domains'))}")
    print(f"Technologies : {len(load_json('skills'))}")

    problems = check_reference_files()
    print("\nContrôle :", "OK, aucun problème" if not problems else f"{len(problems)} problème(s)")
    for p in problems:
        print("  -", p)

    print("\n--- Démo : localisation -> gouvernorat ---")
    for loc in ["Sousse", "Sousse, Tunisia", "Sahloul - Sousse", "Sousse Ville",
                "Centre Urbain Nord, Tunis", "Route de Tunis, Sfax", "Gabès", "Paris"]:
        print(f"{loc!r:32} -> {find_governorate(loc)}")

    print("\n--- Démo : titre -> domaine ---")
    for title in ["AI Engineer Intern", "Artificial Intelligence Engineer", "ML Engineer",
                  "Machine Learning Engineer", "Full Stack Developer", "Flutter Developer",
                  "Pentester", "Stage PFE UX Designer", "Comptable"]:
        print(f"{title!r:36} -> {find_domain(title)}")

    print("\n--- Démo : texte -> technologies ---")
    for txt in ["Python, SQL et ML", "Java Spring Boot, Docker", "JavaScript React / Node.js",
                "C# .NET", "Aucune techno ici"]:
        print(f"{txt!r:32} -> {find_skills(txt)}")