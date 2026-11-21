/* Atelier Mémo : active le mode hors connexion (service worker).
   Ce fichier est inclus dans toutes les pages (accueil et jeux). */
(function () {
  if (!('serviceWorker' in navigator)) return;
  var script = document.currentScript;
  var swUrl = new URL('sw.js', script ? script.src : location.href);
  window.addEventListener('load', function () {
    navigator.serviceWorker.register(swUrl.href).catch(function (e) {
      console.warn('Mode hors connexion indisponible :', e);
    });
  });

  // Sur l'accueil : petit indicateur + liens qui demandent Internet grisés hors ligne.
  function majEtat() {
    document.documentElement.classList.toggle('hors-ligne', !navigator.onLine);
  }
  window.addEventListener('online', majEtat);
  window.addEventListener('offline', majEtat);
  majEtat();

  document.addEventListener('DOMContentLoaded', function () {
    var ind = document.getElementById('etat-hors-connexion');
    if (!ind) return;
    navigator.serviceWorker.ready.then(function () {
      return caches.keys();
    }).then(function (cles) {
      if (cles.some(function (c) { return c.indexOf('atelier-memo-') === 0; })) {
        ind.hidden = false;
      }
    }).catch(function () {});
  });
})();
