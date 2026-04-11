const CACHE_NAME = 'fdx-reader-v26';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icons/icon-192.png',
  './icons/icon-512.png'
];

// Install: cache app shell
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(ASSETS))
      .then(() => self.skipWaiting())
  );
});

// Activate: clean old caches
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

// Fetch strategy:
// - scripts/ folder (library content): network-first so new files/index.json
//   updates show up without waiting for a cache bust
// - Other same-origin (app shell): cache-first for fast offline loads
// - External (fonts, CDNs): network-first with cache fallback
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  const isSameOrigin = url.origin === self.location.origin;
  const isLibraryContent = isSameOrigin && url.pathname.includes('/scripts/');

  // Never touch non-GET requests (PUT/POST/DELETE to GitHub API etc.)
  if (e.request.method !== 'GET') return;

  // Never cache or intercept GitHub API calls — they must always go
  // straight to the network so SHA lookups and writes see fresh data.
  if (url.hostname === 'api.github.com') return;

  if (isLibraryContent) {
    // Network-first for library content
    e.respondWith(
      fetch(e.request).then(response => {
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(e.request, clone));
        }
        return response;
      }).catch(() => caches.match(e.request))
    );
    return;
  }

  if (isSameOrigin) {
    // Cache-first for app shell
    e.respondWith(
      caches.match(e.request).then(cached => {
        if (cached) return cached;
        return fetch(e.request).then(response => {
          if (response.ok) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(e.request, clone));
          }
          return response;
        });
      }).catch(() => {
        if (e.request.mode === 'navigate') {
          return caches.match('./index.html');
        }
      })
    );
    return;
  }

  // External resources: network-first with cache fallback
  e.respondWith(
    fetch(e.request).then(response => {
      if (response.ok) {
        const clone = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(e.request, clone));
      }
      return response;
    }).catch(() => caches.match(e.request))
  );
});
