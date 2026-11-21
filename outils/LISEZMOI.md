# Mode hors connexion de l'Atelier Mémo

Seuls quelques jeux sont disponibles sans Internet. Ils sont copiés dans
`jeux/` et mis en cache sur les tablettes (service worker `sw.js`, déclaré par
`hors-connexion.js` dans chaque page) :

| Carte du menu              | Dépôt d'origine | Copie locale    |
|----------------------------|-----------------|-----------------|
| Les Sosies (Memory)        | `les-sosies`    | `jeux/memory/`  |
| La Séquence (Simon)        | `la-sequence`   | `jeux/simon/`   |
| Quiz                       | `quizz`         | `jeux/quiz/`    |
| L'Intrus                   | `intrus`        | `jeux/intrus/`  |

Leur carte porte le badge vert « ✈ Hors ligne » (coin en haut à droite).
Toutes les autres cartes pointent vers le jeu en ligne : sans Internet, elles
sont grisées avec la mention « Nécessite internet ».

## Modifier un de ces jeux
1. Modifier le jeu dans son dépôt d'origine, comme d'habitude.
2. Ici, lancer `python3 outils/importer_jeux.py` (recopie les jeux, met les
   polices en local, met à jour la liste du cache et sa version).
3. Vérifier, puis publier.

## Rendre un autre jeu disponible hors connexion
1. Ajouter une ligne dans `JEUX` en haut de `outils/importer_jeux.py`
   (dépôt d'origine -> dossier dans `jeux/`, fichiers à copier : images, sons…).
2. Lancer `python3 outils/importer_jeux.py`.
3. Dans `index.html`, sur la carte du jeu : remplacer le lien en ligne par
   `jeux/<dossier>/`, retirer `data-internet` et copier le bloc
   `<span class="badge-offline">…</span>` d'une carte déjà badgée.
4. Vérifier, puis publier.

## Modification faite directement ici (image, son, nouveau fichier)
Lancer `python3 outils/maj_hors_connexion.py`, puis publier.

Les pages (HTML, JSON, JS, CSS) se mettent aussi à jour toutes seules en
arrière-plan dès que la tablette a Internet ; la nouvelle version s'affiche à
l'ouverture suivante.
