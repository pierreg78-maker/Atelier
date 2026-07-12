# Claude.md – Atelier Mémoire

## 🎯 État du projet
**Portail** : `pierreg78-maker.github.io/Atelier/`  
**Hub/Index** : `index.html` (collection de cartes de jeux)  
**Portail créatif** : `Atelier (ré)Créatif` (atelier_crea/)

✅ **Fonctionnalités stables**
- Grille de cartes responsive (2 colonnes max)
- Chaque jeu = une carte cliquable (nom, icône SVG, couleur)
- Footer stylisé (Lora italic, underline pointillé, low opacity)
- Navigation fluide (lien relatif vers chaque jeu HTML)
- Compatibilité mobile 65+ (touches généreuses)

🔧 **En cours**
- Documentation README pour chaque jeu
- Statistiques d'utilisation (localStorage minimal)
- Plus de jeux (domino, loto, etc.)

---

## 📐 Architecture générale

### Répertoire
```
pierreg78-maker.github.io/
├── Atelier/
│   ├── index.html              # 🔴 Hub principal
│   ├── memoire.html            # Jeu Memory
│   ├── simon.html              # Jeu Simon
│   ├── Mini-Rummikub-Access/
│   │   └── index.html
│   ├── jardin.html (ou /atelier_crea/jardin.html)
│   ├── anagrammes.html
│   ├── flashcards.html
│   ├── puzzle-3x3.html
│   └── README.md
└── atelier_crea/
    ├── index.html              # Hub créatif
    ├── jardin.html
    └── autres...
```

---

## 🎨 Convention : Cartes de jeux

### Structure HTML
```html
<div class="game-card" style="background-color: #[color];" onclick="window.location='./[game].html'">
  <div class="card-icon">
    <svg width="60" height="60" viewBox="0 0 60 60">
      <!-- Icône SVG custom -->
    </svg>
  </div>
  <h3>[Nom du jeu]</h3>
  <p class="card-desc">[Description courte]</p>
</div>
```

### CSS de base
```css
.game-card {
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.game-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.2);
}

.card-icon {
  margin-bottom: 12px;
}

h3 {
  font-size: 1.3rem;
  margin: 0;
  color: #333;
}

.card-desc {
  font-size: 0.9rem;
  color: #666;
  margin-top: 8px;
}
```

### Palettes couleurs existantes
| Jeu | Couleur | Hex | Notes |
|-----|---------|-----|-------|
| Mémoire | Bleu ciel | #87CEEB | Original |
| Simon | Orange | #FF8C42 | Vif |
| Mini-Rummikub | Brun-or | #A0826D | Chaud, sophistiqué |
| Anagrammes | Terracotta | #CD7F32 | Terracotta naturel |
| Jardin | Vert | #2d8a4a | Végétal |
| Flashcards | Rose | #E8A0BF | Doux |
| Puzzle 3×3 | Gris-bleu | #5a7c91 | Neutre |

**Règle** : Choisir couleurs qui contrastent bien, éviter deux proches (ex. bleu + bleu ciel)

---

## 🏗️ Patterns JavaScript partagés

### Template pour un nouveau jeu
```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Nom du jeu] - Atelier Mémoire</title>
  <style>
    body {
      font-family: 'Opensans', sans-serif;
      background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
      margin: 0;
      padding: 20px;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
    }
    .container {
      background: white;
      padding: 30px;
      border-radius: 12px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      max-width: 600px;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>[Nom du jeu]</h1>
    <!-- Contenu du jeu -->
    <button id="backBtn" onclick="window.history.back()">← Retour</button>
  </div>
  <script>
    // Initialisation
    console.log('Jeu chargé');
  </script>
</body>
</html>
```

### Bouton retour universel
```html
<button id="backBtn" onclick="window.history.back()" 
  style="padding: 12px 20px; font-size: 1rem; margin-top: 20px;">
  ← Retour au portail
</button>
```

### LocalStorage (score, progression)
```javascript
// Sauvegarder
localStorage.setItem('memoire_scores', JSON.stringify([5, 7, 6, 8]));

// Charger
const scores = JSON.parse(localStorage.getItem('memoire_scores')) || [];
```

### Feedback utilisateur (65+ ans)
```javascript
// ✅ Faire du bruit/vibration quand correct
function playWinSound() {
  const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.frequency.value = 800;
  gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
  osc.start(audioCtx.currentTime);
  osc.stop(audioCtx.currentTime + 0.3);
}

// ✅ Afficher message clair et rassurant
function showMessage(text) {
  const msg = document.createElement('div');
  msg.textContent = text;
  msg.style.cssText = `
    position: fixed; top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    background: #4CAF50; color: white;
    padding: 20px 40px;
    border-radius: 8px;
    font-size: 1.3rem;
    z-index: 1000;
  `;
  document.body.appendChild(msg);
  setTimeout(() => msg.remove(), 2000);
}
```

---

## 🎯 Ajouter un nouveau jeu au hub

### Étapes
1. **Créer le fichier HTML** : `nouveau-jeu.html` dans `/Atelier/`
2. **Ajouter la carte au index.html** :
   ```html
   <div class="game-card" style="background-color: #[COLOR];" 
        onclick="window.location='./nouveau-jeu.html'">
     <div class="card-icon">
       <svg><!-- icône --></svg>
     </div>
     <h3>Nom du Jeu</h3>
     <p class="card-desc">Description rapide</p>
   </div>
   ```
3. **Respecter l'ordre dans la grille** (généralement : Mémoire, Simon, Mini-Rummikub, puis autres)
4. **Tester sur mobile** (iPhone + Android)
5. **Commiter** : `git add . && git commit -m "Add: Nouveau Jeu"`

### Checklist pour tout jeu
- [ ] Pas de dépendances externes (vanilla JS)
- [ ] Responsive mobile (tester sur écran 360×640)
- [ ] Bouton "Retour au portail"
- [ ] Message de victoire/encouragement
- [ ] Contraste élevé (WCAG AA minimum)
- [ ] Pas de sons agressifs ou frustrants
- [ ] Tester sur connexion lente (throttle 3G)

---

## 🎨 Footer standard

### HTML
```html
<footer style="text-align: center; margin-top: 60px; opacity: 0.6;">
  <p style="font-family: Lora; font-style: italic; 
    border-bottom: 1px dotted #999; padding-bottom: 10px;">
    Atelier Mémoire • Créé avec ❤️ pour stimuler et sourire
  </p>
</footer>
```

---

## 🌐 Déploiement & Git

### Workflow quotidien
```bash
# 1. Développement local
git checkout -b feature/nouveau-jeu
# ... éditer fichiers ...

# 2. Test local (live server)
# Naviguer vers http://localhost:8000

# 3. Commit
git add .
git commit -m "Add: Nom du Jeu - [description courte]"

# 4. Push
git push origin feature/nouveau-jeu

# 5. Merge (ou auto-deploy depuis main)
# Vérifier : pierreg78-maker.github.io/Atelier/
```

### Messages de commit
```
Add: [Feature Name] - [Description]
Fix: [Bug] - [Solution]
Update: [Component] - [What changed]
Refactor: [Function] - [Why]
```

---

## 📱 Contexte utilisateurs & Accessibilité

### Profil cible
- Âge : 65–90 ans
- Lieu : Périgord (connexion parfois instable)
- Objectif : stimulation cognitive, plaisir, pas frustration
- Dextérité : variée (gestes amples, double-tap difficile)

### Règles d'or
1. **Grosses touches** (min 44×44px)
2. **Contraste élevé** (#333 sur blanc, pas gris clair)
3. **Feedback immédiat** (son + visuel + texte encourageant)
4. **Pas de timer stressant** (ou optionnel)
5. **Toujours gagner** (jamais "Game Over" brutal)
6. **Fichier léger** (< 500 KB par jeu)

---

## 🔗 Ressources & Stack

| Outil | Usage | Lien |
|-------|-------|------|
| GitHub Pages | Hébergement | `pierreg78-maker.github.io` |
| Vanilla JS | Langage | Pas de framework |
| Canvas | Graphiques | Pour jeux complexes (Jardin, Mini-Rummikub) |
| Web Audio API | Sons | Synth, feedback |
| SVG | Icônes | Scalable, léger |
| LocalStorage | Persistance | Scores, préférences |

---

## 📞 Quand relancer Claude ?

### Pour le hub/index
```
"J'ajoute un nouveau jeu [nom] à la grille.
Voici la structure existante [...].
Peux-tu vérifier que [couleur/position/responsive] est OK?"
```

### Pour un jeu nouveau
```
"Je crée [jeu] pour Atelier Mémoire.
Objectif : [description].
Cible : 65+.
Respecter : no dependencies, accessible, fun.
Pourrais-tu [créer/refiner] le code HTML/JS?"
```

### Pour amélioration globale
```
"Améliore [aspect] du hub/jeu pour mieux servir 65+.
Contexte : [problème observé].
Contraintes : [limites tech/design]."
```
