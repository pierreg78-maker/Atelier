#!/usr/bin/env python3
"""Recopie les jeux depuis leurs dépôts GitHub d'origine dans jeux/, adapte
les liens pour le mode hors connexion, puis met à jour le service worker.
Usage (depuis la racine du dépôt, avec git installé) :
    python3 outils/importer_jeux.py
Les dépôts d'origine restent la référence : modifier un jeu là-bas, puis
relancer ce script ici."""
import pathlib, re, shutil, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
COMPTE = "pierreg78-maker"
SITE = f"https://{COMPTE}.github.io/"
# dépôt d'origine -> (dossier dans jeux/, fichiers/dossiers à copier)
JEUX = {
    "les-sosies": ("memory", ["index.html"]),
    "la-sequence": ("simon", ["index.html"]),
    "quizz": ("quiz", ["index.html"]),
    "intrus": ("intrus", ["index.html"]),
}
LIENS = {f"{SITE}{depot}/": f"jeux/{dossier}/" for depot, (dossier, _) in JEUX.items()}

def adapter(page: pathlib.Path):
    h = page.read_text()
    prof = len(page.relative_to(ROOT).parts) - 1
    rel = "../" * prof
    h = h.replace(f"{SITE}Atelier/", rel)
    h = re.sub(r"https://raw\.githubusercontent\.com/%s/[^/]+/main/" % COMPTE, "", h)
    for src, dst in LIENS.items():
        h = h.replace(src, rel + dst)
    if "hors-connexion.js" not in h:
        i = h.lower().index("</head>")
        h = h[:i] + f'<script src="{rel}hors-connexion.js"></script>\n' + h[i:]
    page.write_text(h)

def main():
    with tempfile.TemporaryDirectory() as tmp:
        for depot, (dossier, elements) in JEUX.items():
            print("import", depot)
            subprocess.run(["git", "clone", "-q", "--depth", "1",
                            f"https://github.com/{COMPTE}/{depot}.git", f"{tmp}/{depot}"], check=True)
            dest = ROOT / "jeux" / dossier
            for e in elements:
                s, d = pathlib.Path(tmp, depot, e), dest / e
                if d.is_dir(): shutil.rmtree(d)
                d.parent.mkdir(parents=True, exist_ok=True)
                if s.is_dir(): shutil.copytree(s, d, ignore=shutil.ignore_patterns("test.*"))
                else: shutil.copy2(s, d)
            adapter(dest / "index.html")
    here = pathlib.Path(__file__).parent
    subprocess.run([sys.executable, str(here / "polices_locales.py")], check=True)
    subprocess.run([sys.executable, str(here / "maj_hors_connexion.py")], check=True)

if __name__ == "__main__":
    main()
