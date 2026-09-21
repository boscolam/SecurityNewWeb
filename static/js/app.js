/**
 * Cybersecurity News Dashboard - Main JavaScript
 * ================================================
 * Handles interactive features:
 * 1. Mobile navigation toggle (hamburger menu)
 * 2. Auto-refresh of dashboard statistics
 * 3. Notification toasts for user feedback
 * 4. Keyboard shortcuts for quick navigation
 */

/* ============================================================
   MOBILE NAVIGATION TOGGLE
   When the hamburger menu icon is clicked on mobile devices,
   this toggles the visibility of the navigation links dropdown.
   ============================================================ */
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', function() {
            /* Toggle the 'show' CSS class which controls
               display:flex vs display:none on mobile */
            navLinks.classList.toggle('show');
        });

        /* Close the mobile nav menu when clicking outside of it */
        document.addEventListener('click', function(e) {
            if (!navToggle.contains(e.target) && !navLinks.contains(e.target)) {
                navLinks.classList.remove('show');
            }
        });
    }
});

/* ============================================================
   AUTO-REFRESH DASHBOARD
   Periodically fetches updated statistics from the API
   and refreshes the page if on the dashboard.
   Refresh interval matches the configured feed refresh setting.
   ============================================================ */
(function() {
    /* Only auto-refresh on the dashboard page */
    if (window.location.pathname === '/') {
        /* Refresh the page every 5 minutes to show updated stats.
           The actual feed fetching happens in the backend scheduler. */
        const DASHBOARD_REFRESH_MS = 5 * 60 * 1000; // 5 minutes

        setInterval(function() {
            /* Fetch updated stats via API without full page reload */
            fetch('/api/stats')
                .then(function(response) { return response.json(); })
                .then(function(data) {
                    /* Update stat card numbers if elements exist */
                    updateStatIfExists('total-articles', data.total_news);
                    updateStatIfExists('today-news', data.today_news);
                    updateStatIfExists('hacking-count', data.hacking_incidents);
                    updateStatIfExists('cve-count', data.cve_count);
                })
                .catch(function(err) {
                    console.warn('Auto-refresh failed:', err);
                });
        }, DASHBOARD_REFRESH_MS);
    }

    /* Helper: update a stat card's number if the element exists */
    function updateStatIfExists(id, value) {
        var el = document.getElementById(id);
        if (el) {
            el.textContent = value;
        }
    }
})();

/* ============================================================
   NOTIFICATION TOAST
   Shows a brief notification message at the bottom of the screen.
   Used to confirm actions like feed refresh, analysis run, etc.
   ============================================================ */
function showToast(message, type) {
    /* type can be: 'success', 'error', 'info', 'warning' */
    type = type || 'info';

    /* Create the toast element */
    var toast = document.createElement('div');
    toast.className = 'toast toast-' + type;
    toast.textContent = message;

    /* Style the toast notification */
    toast.style.cssText = [
        'position: fixed',
        'bottom: 20px',
        'right: 20px',
        'padding: 12px 24px',
        'border-radius: 8px',
        'color: white',
        'font-size: 0.9rem',
        'font-weight: 500',
        'z-index: 9999',
        'animation: slideIn 0.3s ease',
        'max-width: 400px',
        'box-shadow: 0 4px 12px rgba(0,0,0,0.4)'
    ].join(';');

    /* Set background color based on toast type */
    var colors = {
        success: '#28a745',
        error: '#dc3545',
        warning: '#ffc107',
        info: '#17a2b8'
    };
    toast.style.background = colors[type] || colors.info;
    if (type === 'warning') {
        toast.style.color = '#000';
    }

    document.body.appendChild(toast);

    /* Auto-remove the toast after 4 seconds */
    setTimeout(function() {
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.3s';
        setTimeout(function() {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }, 4000);
}

/* ============================================================
   KEYBOARD SHORTCUTS
   Quick navigation shortcuts for power users:
   - Alt+D: Go to Dashboard
   - Alt+N: Go to News
   - Alt+C: Go to CVE Monitor
   - Alt+S: Go to Sources
   - Alt+P: Go to Priorities
   - Alt+G: Go to Settings
   ============================================================ */
document.addEventListener('keydown', function(e) {
    /* Only trigger shortcuts when Alt key is held and not typing in an input */
    if (e.altKey && !e.target.matches('input, textarea, select')) {
        var shortcuts = {
            'd': '/',          /* Dashboard */
            'n': '/news',      /* News */
            'c': '/cve',       /* CVE Monitor */
            's': '/sources',   /* Sources */
            'p': '/priorities', /* Priorities */
            'g': '/settings'   /* Settings (G for gear) */
        };

        var path = shortcuts[e.key.toLowerCase()];
        if (path) {
            e.preventDefault();
            window.location.href = path;
        }
    }
});

/* ============================================================
   CONFIRM DELETE HELPER
   Generic confirmation dialog for delete actions.
   ============================================================ */
function confirmDelete(itemName) {
    return confirm('Are you sure you want to delete "' + itemName + '"? This cannot be undone.');
}

/* ============================================================
   TIMESTAMP FORMATTER
   Updates all time-ago elements periodically to keep them fresh
   without requiring a full page reload.
   ============================================================ */
(function() {
    /* Re-format time-ago values every minute */
    setInterval(function() {
        document.querySelectorAll('[data-timestamp]').forEach(function(el) {
            var timestamp = el.getAttribute('data-timestamp');
            if (timestamp) {
                el.textContent = formatTimeAgo(new Date(timestamp));
            }
        });
    }, 60000); /* Update every 60 seconds */

    /* Convert a Date object to a human-readable time-ago string */
    function formatTimeAgo(date) {
        var now = new Date();
        var seconds = Math.floor((now - date) / 1000);

        if (seconds < 60) return 'Just now';
        if (seconds < 3600) return Math.floor(seconds / 60) + 'm ago';
        if (seconds < 86400) return Math.floor(seconds / 3600) + 'h ago';
        if (seconds < 2592000) return Math.floor(seconds / 86400) + 'd ago';
        return date.toISOString().split('T')[0];
    }
})();
