/* Atelier Mémo : service worker (mode hors connexion).
   La liste des fichiers et la version sont régénérées par
   outils/maj_hors_connexion.py : ne pas les modifier à la main. */

// <genere>
const VERSION = '42a5f142a0';
const FICHIERS = [
  "favicon.svg",
  "hors-connexion.js",
  "icones/apple-touch-icon.png",
  "icones/icone-192.png",
  "icones/icone-512.png",
  "icones/icone-maskable-512.png",
  "./",
  "jeux/intrus/",
  "jeux/memory/",
  "jeux/quiz/",
  "jeux/simon/",
  "manifest.webmanifest",
  "polices/4463a6e3.css",
  "polices/482e5863.css",
  "polices/f55b3729.css",
  "polices/fichiers/dmmono_v16_aFTR7PB1QTsUX8KYvumzEY2tbZX9.woff2",
  "polices/fichiers/dmmono_v16_aFTR7PB1QTsUX8KYvumzEYOtbQ.woff2",
  "polices/fichiers/dmmono_v16_aFTU7PB1QTsUX8KYthSQBLyM.woff2",
  "polices/fichiers/dmmono_v16_aFTU7PB1QTsUX8KYthqQBA.woff2",
  "polices/fichiers/dmsans_v17_rP2Yp2ywxg089UriI5-g4vlH9VoD8Cmcqbu0-K4.woff2",
  "polices/fichiers/dmsans_v17_rP2Yp2ywxg089UriI5-g4vlH9VoD8Cmcqbu6-K6h9Q.woff2",
  "polices/fichiers/inter_v20_UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7.woff2",
  "polices/fichiers/inter_v20_UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa25L7SUc.woff2",
  "polices/fichiers/lora_v37_0QIvMX1D_JOuMwT7I-NP.woff2",
  "polices/fichiers/lora_v37_0QIvMX1D_JOuMwr7Iw.woff2",
  "polices/fichiers/playfairdisplay_v40_nuFiD-vYSZviVYUb_rj3ij__anPXDTLYgFE_.woff2",
  "polices/fichiers/playfairdisplay_v40_nuFiD-vYSZviVYUb_rj3ij__anPXDTzYgA.woff2"
];
// </genere>

const PREFIXE = 'atelier-memo-';
const CACHE = PREFIXE + VERSION;
const BASE = new URL('./', self.location).href;          // .../Atelier/
const A_RAFRAICHIR = /\/$|\.(html|json|js|css|webmanifest)$/i; // petits fichiers mis à jour en arrière-plan

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE)
      .then((cache) => cache.addAll(FICHIERS.map((f) => new Request(f, { cache: 'reload' }))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((cles) => Promise.all(cles
        .filter((c) => c.startsWith(PREFIXE) && c !== CACHE)
        .map((c) => caches.delete(c))))
      .then(() => self.clients.claim())
  );
});

function cleDuCache(url) {
  const u = new URL(url);
  u.search = '';
  u.hash = '';
  if (u.pathname.endsWith('/index.html')) u.pathname = u.pathname.slice(0, -'index.html'.length);
  return u.href;
}

// Safari exige des réponses partielles (206) pour les sons lus depuis le cache.
async function reponsePartielle(requete, reponse) {
  const plage = requete.headers.get('range');
  if (!plage) return reponse;
  const m = /bytes=(\d*)-(\d*)/.exec(plage);
  if (!m) return reponse;
  const blob = await reponse.blob();
  const debut = m[1] ? parseInt(m[1], 10) : Math.max(0, blob.size - parseInt(m[2], 10));
  const fin = m[1] && m[2] ? parseInt(m[2], 10) : blob.size - 1;
  return new Response(blob.slice(debut, fin + 1), {
    status: 206,
    statusText: 'Partial Content',
    headers: {
      'Content-Type': reponse.headers.get('Content-Type') || 'application/octet-stream',
      'Content-Range': `bytes ${debut}-${fin}/${blob.size}`,
      'Content-Length': String(fin - debut + 1),
    },
  });
}

async function rafraichir(cle) {
  try {
    const rep = await fetch(cle, { cache: 'no-cache' });
    if (rep.ok) await (await caches.open(CACHE)).put(cle, rep);
  } catch (e) { /* pas de réseau : on garde la version en cache */ }
}

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET' || !req.url.startsWith(BASE)) return; // le reste passe par Internet
  const cle = cleDuCache(req.url);

  event.respondWith((async () => {
    const cache = await caches.open(CACHE);
    const enCache = await cache.match(cle);
    if (enCache) {
      // Cache d'abord ; les pages et scripts se mettent à jour en arrière-plan quand Internet est là.
      if (A_RAFRAICHIR.test(new URL(cle).pathname)) event.waitUntil(rafraichir(cle));
      return reponsePartielle(req, enCache.clone());
    }
    try {
      const rep = await fetch(req);
      if (rep.ok && rep.status === 200 && !req.headers.get('range')) cache.put(cle, rep.clone());
      return rep;
    } catch (e) {
      if (req.mode === 'navigate') {
        const accueil = await cache.match(BASE);
        if (accueil) return accueil;
      }
      return new Response('Hors connexion', { status: 503, headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
    }
  })());
});
