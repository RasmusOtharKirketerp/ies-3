document.addEventListener('DOMContentLoaded', function () {
    const apiKey = '1f3879c87fa9c0c5e894a16510d496c8';
    const city = 'Stenløse,DK';
    const weatherTicker = document.getElementById('weather-ticker');
    const weatherTickerInner = document.getElementById('weather-ticker-inner');

    function getDayName(dt) {
        return new Date(dt * 1000).toLocaleDateString(undefined, { weekday: 'short' });
    }

    function getIconHtml(icon, desc) {
        return `<img src="https://openweathermap.org/img/wn/${icon}@2x.png" alt="${desc}" title="${desc}">`;
    }

    fetch(`https://api.openweathermap.org/data/2.5/forecast?q=${encodeURIComponent(city)}&appid=${apiKey}&units=metric&lang=da`)
        .then(response => response.json())
        .then(data => {
            if (!data.list) {
                weatherTickerInner.textContent = "Weather data unavailable";
                return;
            }
            const now = new Date();
            const today = now.getDate();
            const tomorrow = new Date(now.getTime() + 86400000).getDate();

            let todayTemps = [];
            let tomorrowTemps = [];
            let weekendTemps = [];

            data.list.forEach(item => {
                const date = new Date(item.dt * 1000);
                const day = date.getDate();
                const weekday = date.getDay();
                if (day === today) {
                    todayTemps.push(item);
                } else if (day === tomorrow) {
                    tomorrowTemps.push(item);
                } else if (weekday === 6 || weekday === 0) {
                    weekendTemps.push(item);
                }
            });

            function summarizePeriod(period) {
                if (period.length === 0) return '';
                // Find max temp and most frequent icon
                const max = Math.round(Math.max(...period.map(i => i.main.temp_max)));
                const iconCounts = {};
                period.forEach(i => {
                    const icon = i.weather[0].icon;
                    iconCounts[icon] = (iconCounts[icon] || 0) + 1;
                });
                const mainIcon = Object.entries(iconCounts).sort((a, b) => b[1] - a[1])[0][0];
                return `${getIconHtml(mainIcon, '')} ${max}°C`;
            }

            const todayStr = todayTemps.length ? `I dag: ${summarizePeriod(todayTemps)}` : '';
            const tomorrowStr = tomorrowTemps.length ? `I morgen: ${summarizePeriod(tomorrowTemps)}` : '';
            let weekendStr = '';
            if (weekendTemps.length) {
                const days = {};
                weekendTemps.forEach(item => {
                    const d = getDayName(item.dt);
                    if (!days[d]) days[d] = [];
                    days[d].push(item);
                });
                weekendStr = Object.entries(days).map(([d, arr]) =>
                    `${d}: ${summarizePeriod(arr)}`
                ).join('  ');
                if (weekendStr) weekendStr = `Weekend: ${weekendStr}`;
            }

            weatherTickerInner.innerHTML = [todayStr, tomorrowStr, weekendStr].filter(Boolean).join('  ');
        })
        .catch(() => {
            weatherTickerInner.textContent = "Weather data unavailable";
        });
});
