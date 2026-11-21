#!/usr/bin/env python3
"""Régénère la liste des fichiers mis en cache et la version du service worker.
À relancer après chaque ajout ou modification de jeu, d'image ou de son :
    python3 outils/maj_hors_connexion.py
Changer la version force les tablettes à tout retélécharger à la prochaine
connexion."""
import hashlib, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXCLUS_DOSSIERS = {".git", "outils", ".github"}
EXCLUS_FICHIERS = {"sw.js", "LICENSE", ".gitattributes", ".gitignore"}
EXCLUS_EXT = {".md", ".py"}

def fichiers():
    for p in sorted(ROOT.rglob("*")):
        rel = p.relative_to(ROOT)
        if not p.is_file() or rel.parts[0] in EXCLUS_DOSSIERS:
            continue
        if p.name in EXCLUS_FICHIERS or p.suffix.lower() in EXCLUS_EXT or p.stat().st_size <= 1:
            continue
        yield rel

def main():
    h = hashlib.sha256()
    liste = []
    for rel in fichiers():
        h.update(str(rel).encode()); h.update((ROOT / rel).read_bytes())
        s = rel.as_posix()
        if s == "index.html":
            s = "./"
        elif s.endswith("/index.html"):
            s = s[: -len("index.html")]
        liste.append(s)
    version = h.hexdigest()[:10]
    sw = ROOT / "sw.js"
    bloc = ("// <genere>\nconst VERSION = '%s';\nconst FICHIERS = %s;\n// </genere>"
            % (version, json.dumps(liste, ensure_ascii=False, indent=2)))
    sw.write_text(re.sub(r"// <genere>.*?// </genere>", lambda _: bloc, sw.read_text(), flags=re.S))
    taille = sum((ROOT / f).stat().st_size for f in fichiers())
    print(f"{len(liste)} fichiers, {taille/1e6:.1f} Mo, version {version}")

if __name__ == "__main__":
    main()
