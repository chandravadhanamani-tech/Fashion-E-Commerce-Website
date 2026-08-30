// Fashion Store Master JavaScript App
const API_BASE = '/api/v1';

// Auth State Helpers
function getAuthToken() {
    return localStorage.getItem('fashion_token');
}

function setAuthToken(token) {
    localStorage.setItem('fashion_token', token);
}

function removeAuthToken() {
    localStorage.removeItem('fashion_token');
    localStorage.removeItem('fashion_user');
}

function getStoredUser() {
    const u = localStorage.getItem('fashion_user');
    return u ? JSON.parse(u) : null;
}

function setStoredUser(userObj) {
    localStorage.setItem('fashion_user', JSON.stringify(userObj));
}

function authHeaders() {
    const token = getAuthToken();
    return token ? { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' } : { 'Content-Type': 'application/json' };
}

// UI Initialization
document.addEventListener('DOMContentLoaded', () => {
    updateNavAuth();
    updateCartCount();
});

function updateNavAuth() {
    const user = getStoredUser();
    const navAuthContainer = document.getElementById('navAuthContainer');
    if (!navAuthContainer) return;

    if (user && getAuthToken()) {
        navAuthContainer.innerHTML = `
            <div class="dropdown">
                <button class="btn btn-outline-custom dropdown-toggle d-flex align-items-center gap-2" type="button" data-bs-toggle="dropdown">
                    <i class="bi bi-person-circle fs-5 text-pink"></i>
                    <span>${user.full_name || 'My Account'}</span>
                </button>
                <ul class="dropdown-menu dropdown-menu-dark dropdown-menu-end shadow">
                    <li><a class="dropdown-item" href="/profile"><i class="bi bi-sliders me-2"></i>Profile & Size Fit</a></li>
                    <li><a class="dropdown-item" href="/profile#orders"><i class="bi bi-bag-check me-2"></i>My Orders</a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item text-danger" href="#" onclick="handleLogout(event)"><i class="bi bi-box-arrow-right me-2"></i>Logout</a></li>
                </ul>
            </div>
        `;
    } else {
        navAuthContainer.innerHTML = `
            <a href="/auth" class="btn btn-gradient btn-sm">
                <i class="bi bi-box-arrow-in-right me-1"></i> Sign In / Register
            </a>
        `;
    }
}

function handleLogout(e) {
    if (e) e.preventDefault();
    removeAuthToken();
    window.location.href = '/';
}

async function updateCartCount() {
    const badge = document.getElementById('cartBadgeCount');
    if (!badge) return;

    if (!getAuthToken()) {
        badge.innerText = '0';
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/cart/`, { headers: authHeaders() });
        if (res.ok) {
            const cart = await res.json();
            badge.innerText = cart.total_items || '0';
        } else {
            badge.innerText = '0';
        }
    } catch (err) {
        console.error('Failed to fetch cart count:', err);
    }
}

// Global Size Recommendation Modal Calculator
async function runModalSizeRecommendation(event) {
    if (event) event.preventDefault();

    const gender = document.getElementById('recGender').value;
    const height = parseFloat(document.getElementById('recHeight').value);
    const weight = parseFloat(document.getElementById('recWeight').value);
    const chest = parseFloat(document.getElementById('recChest').value) || null;
    const waist = parseFloat(document.getElementById('recWaist').value) || null;
    const fit = document.getElementById('recFit').value;

    if (!height || !weight) {
        alert('Please provide height and weight.');
        return;
    }

    const payload = {
        gender: gender,
        height_cm: height,
        weight_kg: weight,
        chest_cm: chest,
        waist_cm: waist,
        fit_preference: fit
    };

    try {
        const res = await fetch(`${API_BASE}/recommendations/size`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!res.ok) throw new Error('Size calculation failed');
        const data = await res.json();

        const resultBox = document.getElementById('modalSizeResult');
        resultBox.classList.remove('d-none');
        resultBox.innerHTML = `
            <div class="alert alert-success bg-dark border-success text-white">
                <div class="d-flex align-items-center justify-content-between mb-2">
                    <h5 class="mb-0 text-pink font-weight-bold"><i class="bi bi-magic me-2"></i>Recommended Size: <strong>${data.recommended_size}</strong></h5>
                    <span class="badge bg-pink px-3 py-2 fs-6">${data.confidence_percentage}% Match Confidence</span>
                </div>
                <p class="mb-2 text-secondary small">${data.fit_summary}</p>
                <div class="d-flex gap-3 text-muted border-top border-secondary pt-2 mt-2 fs-7">
                    <span>Est. Chest: ${data.size_breakdown.estimated_chest_cm}cm</span>
                    <span>Est. Waist: ${data.size_breakdown.estimated_waist_cm}cm</span>
                    ${data.suggested_alternative ? `<span>Alt. Size: ${data.suggested_alternative}</span>` : ''}
                </div>
            </div>
        `;
    } catch (err) {
        alert('Error computing size recommendation: ' + err.message);
    }
}
