// All JavaScript logic from index.html except weather/xolta

const viewSwitch = document.getElementById('viewSwitch');
viewSwitch.addEventListener('change', function () {
    document.body.classList.toggle('compact', this.checked);
    localStorage.setItem('compactView', this.checked ? '1' : '0');
});

// Picture switch logic
const pictureSwitch = document.getElementById('pictureSwitch');
pictureSwitch.addEventListener('change', function () {
    document.body.classList.toggle('hide-pictures', !this.checked);
    localStorage.setItem('showPictures', this.checked ? '1' : '0');
});

// Dark mode switch logic
const darkModeSwitch = document.getElementById('darkModeSwitch');
function setDarkMode(enabled) {
    if (enabled) {
        document.body.classList.add('dark-mode');
        localStorage.setItem('darkMode', '1');
    } else {
        document.body.classList.remove('dark-mode');
        localStorage.setItem('darkMode', '0');
    }
}
darkModeSwitch.addEventListener('change', function () {
    setDarkMode(this.checked);
});

document.addEventListener('DOMContentLoaded', function () {
    const compact = localStorage.getItem('compactView') === '1';
    viewSwitch.checked = compact;
    if (compact) {
        document.body.classList.add('compact');
    }

    // Picture switch state
    const showPictures = localStorage.getItem('showPictures');
    if (showPictures === null || showPictures === '1') {
        pictureSwitch.checked = true;
        document.body.classList.remove('hide-pictures');
    } else {
        pictureSwitch.checked = false;
        document.body.classList.add('hide-pictures');
    }

    // Dark mode state
    const darkMode = localStorage.getItem('darkMode') === '1';
    darkModeSwitch.checked = darkMode;
    setDarkMode(darkMode);

    // Hide articles that were hidden previously
    const hiddenArticles = JSON.parse(localStorage.getItem('hiddenArticles') || '[]');
    hiddenArticles.forEach(url => {
        const card = document.querySelector(`.article-card[data-article-url="${url}"]`);
        if (card) card.style.display = 'none';
    });

    // Show time since published for each article
    document.querySelectorAll('[data-publish-date]').forEach(function (el) {
        const dateStr = el.getAttribute('data-publish-date');
        if (!dateStr) return;
        // Try to parse as local or UTC
        let dt = new Date(dateStr.replace(' ', 'T'));
        if (isNaN(dt)) dt = new Date(dateStr);
        if (isNaN(dt)) return;
        const now = new Date();
        let diff = Math.floor((now - dt) / 1000); // seconds
        if (diff < 0) return;
        const days = Math.floor(diff / 86400);
        diff %= 86400;
        const hours = Math.floor(diff / 3600);
        diff %= 3600;
        const minutes = Math.floor(diff / 60);
        let parts = [];
        if (days > 0) parts.push(days + 'd');
        if (hours > 0 || days > 0) parts.push(hours + 'h');
        parts.push(minutes + 'm');
        el.textContent = '(' + parts.join(' ') + ' siden)';
    });

    // Highlight user words in all articles on page load
    loadAndHiliteUserWords();
});

function removeArticle(btn) {
    const card = btn.closest('.article-card');
    if (card) {
        card.style.display = 'none';
        // Save hidden article URL to localStorage
        const url = card.getAttribute('data-article-url');
        let hiddenArticles = JSON.parse(localStorage.getItem('hiddenArticles') || '[]');
        if (!hiddenArticles.includes(url)) {
            hiddenArticles.push(url);
            localStorage.setItem('hiddenArticles', JSON.stringify(hiddenArticles));
        }
    }
}

function resetHiddenArticles() {
    // Show all articles
    document.querySelectorAll('.article-card').forEach(card => {
        card.style.display = '';
    });
    // Clear hidden articles from localStorage
    localStorage.removeItem('hiddenArticles');
}

function markAllRead() {
    // Hide all articles and store their URLs in localStorage
    let hiddenArticles = [];
    document.querySelectorAll('.article-card').forEach(card => {
        card.style.display = 'none';
        const url = card.getAttribute('data-article-url');
        if (url) hiddenArticles.push(url);
    });
    localStorage.setItem('hiddenArticles', JSON.stringify(hiddenArticles));
}

// Progress bar timer for reload
let reloadSeconds = 60;
const progressBar = document.getElementById('reload-progress');
let progress = 100;
function updateProgressBar() {
    progress -= 100 / reloadSeconds;
    if (progress < 0) progress = 0;
    progressBar.style.width = progress + "%";
    progressBar.setAttribute('aria-valuenow', Math.round(progress));
}
setInterval(updateProgressBar, 1000);

// Page reload every 60 seconds
setTimeout(function () {
    window.location.reload();
}, reloadSeconds * 1000);

// Loads user words from /words and highlights them in all articles
function loadAndHiliteUserWords() {
    fetch('/words')
        .then(r => r.text())
        .then(html => {
            // Parse the HTML and extract words from the table/list
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            // Try to find all words in the table (assuming .word-da or .word-en class or <td>)
            let wordNodes = Array.from(doc.querySelectorAll('.word-da, .word-en'));
            if (wordNodes.length === 0) {
                // fallback: all <td> in table with id or class 'words'
                const table = doc.querySelector('table');
                if (table) {
                    wordNodes = Array.from(table.querySelectorAll('td'));
                }
            }
            // Extract unique words, lowercased
            let userWords = wordNodes.map(n => n.textContent.trim().toLowerCase()).filter(Boolean);
            userWords = Array.from(new Set(userWords));
            userWords.sort((a, b) => b.length - a.length);

            // For each article, highlight user words (including all endings)
            document.querySelectorAll('.card-text').forEach(function (el) {
                let orig = el.textContent || '';
                let html = orig;
                userWords.forEach(word => {
                    if (!word) return;
                    // Regex: match word as a substring of any token (allow all endings)
                    // This will match the word inside any word, case-insensitive, but not as part of another word's prefix
                    const re = new RegExp(`\\b(\\w*${escapeRegExp(word)}\\w*)\\b`, 'gi');
                    html = html.replace(re, '<span class="user-word-hilite" style="text-decoration:underline;">$1</span>');
                });
                el.innerHTML = html;
            });
        });
}

// Utility: escape regex special characters
function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
