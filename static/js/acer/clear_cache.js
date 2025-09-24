async function clearCache() {
    if ('caches' in window) {
        try {
            const names = await caches.keys();
            await Promise.all(names.map(name => caches.delete(name)));
            console.log('Caches cleared successfully');
        } catch (err) {
            console.error('Failed to clear caches:', err);
        }
    }
}
setInterval(clearCache, 3600000);