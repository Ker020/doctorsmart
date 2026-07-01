const CACHE_NAME = 'smart-healthcare-v19';
const ASSETS_TO_CACHE = [
    '/static/css/bootstrap.min.css',
    '/static/css/bootstrap-icons.css',
    '/static/css/custom.css',
    '/static/js/bootstrap.bundle.min.js?v=3.2',
    '/static/js/marked.min.js?v=3.2',
    '/static/js/sweetalert2.all.min.js?v=3.2'
];

self.addEventListener('install', (event) => {
    console.log('[SW] Installing v17...');
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('[SW] Pre-caching critical assets');
            return Promise.all(
                ASSETS_TO_CACHE.map(url => {
                    return fetch(url).then(response => {
                        if (!response.ok) {
                            throw new Error(`Request for ${url} failed with status ${response.status}`);
                        }
                        return cache.put(url, response);
                    }).catch(error => {
                        console.error(`[SW] Failed to cache ${url}:`, error);
                        // Still allow installation but log the failure
                    });
                })
            );
        })
    );
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    console.log('[SW] Activating v17...');
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('[SW] Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

self.addEventListener('fetch', (event) => {
    // 1. Immediately skip non-GET requests (like AI analysis POST)
    if (event.request.method !== 'GET') {
        console.log(`[SW v19] Skipping non-GET request: ${event.request.method} ${event.request.url}`);
        return;
    }

    const url = new URL(event.request.url);

    // 2. STRATEGY: Network First for dynamic routes and navigation
    if (!url.pathname.startsWith('/static/')) {
        console.log(`[SW v19] Network First for: ${url.pathname}`);
        event.respondWith(
            fetch(event.request).catch((err) => {
                console.error(`[SW v19] Fetch failed for ${url.pathname}:`, err);
                return caches.match(event.request);
            })
        );
        return;
    }

    // 3. STRATEGY: Cache First for static assets (/static/*)
    event.respondWith(
        caches.match(event.request).then((response) => {
            if (response) {
                console.log(`[SW v19] Cache Hit: ${url.pathname}`);
                return response;
            }

            console.log(`[SW v19] Cache Miss, fetching: ${url.pathname}`);
            return fetch(event.request).then((networkResponse) => {
                if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') {
                    return networkResponse;
                }
                const responseToCache = networkResponse.clone();
                caches.open(CACHE_NAME).then((cache) => {
                    cache.put(event.request, responseToCache);
                });
                return networkResponse;
            });
        })
    );
});
