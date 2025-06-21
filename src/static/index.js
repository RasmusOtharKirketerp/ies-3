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
