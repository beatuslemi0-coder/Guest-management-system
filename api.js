const API_BASE_URL = window.API_BASE_URL || 'http://127.0.0.1:8000/api/v1';

async function apiRequest(path, options = {}) {
    const headers = new Headers(options.headers || {});
    const token = localStorage.getItem('token');

    if (token) {
        headers.set('Authorization', `Bearer ${token}`);
    }
    if (options.body && !headers.has('Content-Type') && !(options.body instanceof FormData)) {
        headers.set('Content-Type', 'application/json');
    }

    const response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers });
    const contentType = response.headers.get('content-type') || '';
    const data = contentType.includes('application/json') ? await response.json() : null;

    if (!response.ok) {
        if (response.status === 401 && token && path !== '/auth/login') {
            localStorage.removeItem('token');
            window.location.href = 'index.html';
        }

        const detail = data && data.detail;
        const message = Array.isArray(detail)
            ? detail.map((item) => item.msg).join(', ')
            : detail || `Ombi limeshindikana (${response.status}).`;
        throw new Error(message);
    }

    return data;
}

async function apiDownload(path, filename) {
    const headers = new Headers();
    const token = localStorage.getItem('token');
    if (token) headers.set('Authorization', `Bearer ${token}`);

    const response = await fetch(`${API_BASE_URL}${path}`, { headers });
    if (!response.ok) {
        const contentType = response.headers.get('content-type') || '';
        const data = contentType.includes('application/json') ? await response.json() : null;
        if (response.status === 401 && token) {
            localStorage.removeItem('token');
            window.location.href = 'index.html';
        }
        const detail = data && data.detail;
        const message = Array.isArray(detail)
            ? detail.map((item) => item.msg).join(', ')
            : detail || `Imeshindikana kupakua faili (${response.status}).`;
        throw new Error(message);
    }

    const blob = await response.blob();
    const objectUrl = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = objectUrl;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.setTimeout(() => URL.revokeObjectURL(objectUrl), 1000);
}
