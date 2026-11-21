#!/usr/bin/env python3
"""Télécharge les polices Google Fonts utilisées par les pages et les range
dans polices/ pour qu'elles marchent hors connexion. À lancer depuis la racine
du dépôt :  python3 outils/polices_locales.py"""
import hashlib, pathlib, re, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTS = ROOT / "polices"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
KEEP = {"latin", "latin-ext"}
LINK = re.compile(r'<link[^>]*href="(https://fonts\.googleapis\.com/css2\?[^"]+)"[^>]*>')
PRECONNECT = re.compile(r'\s*<link rel="preconnect" href="https://fonts\.(googleapis|gstatic)\.com"[^>]*>')

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30).read()

def vendor(url):
    css = get(url.replace("&amp;", "&")).decode()
    name = hashlib.sha1(url.encode()).hexdigest()[:8]
    out = []
    for comment, block in re.findall(r'/\* ([\w-]+) \*/\s*(@font-face \{.*?\})', css, re.S):
        if comment not in KEEP:
            continue
        def dl(m):
            u = m.group(1)
            fn = re.sub(r'[^A-Za-z0-9._-]', '_', u.split('/s/')[-1])
            p = FONTS / "fichiers" / fn
            if not p.exists():
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(get(u))
            return f"url(fichiers/{fn})"
        out.append(f"/* {comment} */\n" + re.sub(r'url\((https://[^)]+)\)', dl, block))
    (FONTS / f"{name}.css").write_text("\n".join(out) + "\n")
    return f"{name}.css"

def main():
    FONTS.mkdir(exist_ok=True)
    for page in [ROOT / "index.html", *sorted((ROOT / "jeux").glob("*/index.html"))]:
        html = page.read_text()
        if "fonts.googleapis.com" not in html:
            continue
        rel = "../" * (len(page.relative_to(ROOT).parts) - 1) + "polices/"
        html = PRECONNECT.sub("", html)
        html = LINK.sub(lambda m: f'<link href="{rel}{vendor(m.group(1))}" rel="stylesheet">', html)
        page.write_text(html)
        print("polices locales :", page.relative_to(ROOT))

if __name__ == "__main__":
    main()
