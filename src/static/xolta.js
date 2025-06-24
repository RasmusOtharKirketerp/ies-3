document.addEventListener('DOMContentLoaded', function () {
    const xoltaTicker = document.getElementById('xolta-ticker');
    const xoltaTickerInner = document.getElementById('xolta-ticker-inner');

    function safe(val, unit = '') {
        // Accept 0, negative, and positive numbers, but not undefined/null/empty/"undefined"/"null"
        if (
            val === undefined ||
            val === null ||
            val === '' ||
            val === 'undefined' ||
            val === 'null' ||
            (typeof val !== 'number' && isNaN(Number(val)))
        ) return '--' + unit;
        // Special: treat values between -0.05 and +0.05 as 0 (no decimals)
        if (unit === '%' && (val > -0.1 && val < 0.1)) {
            return '0' + unit;
        }
        if (unit === '%') {
            // If exactly 100, show as 100 % (no decimals)
            if (Math.abs(Number(val) - 100) < 0.005) return '100' + unit;
            return Number(val).toFixed(0) + ' ' + unit;
        }
        if (unit === 'A') {
            if (val == -0)
                val = 0; // Handle -0 case
                unit = ' '; // Current in Amperes
            
            if (val < -0.09)
                unit = ' Sælger'; // Negative current
            else if (val > 0.09)
                unit = ' Køber'; // Positive current
            val = Math.abs(Number(val)) 
            return Number(val).toFixed(1) + unit;
        }
        if (unit === 'kW') {
            unit = '';
            let num = Number(val);
            if (num > -0.05 && num < 0.05) return '0' + unit;
            return num.toFixed(2) + unit;
        }
        return val + unit;
    }

    function fetchAndShowXolta() {
        const XOLTA_API = "http://80.197.112.200:9123/xolta/data";
        const XOLTA_KEY = "sk-5nC3TqA7rLgJ9wXzM0vKbF2eYtPqDU1L";
        fetch(XOLTA_API, {
            headers: {
                "Authorization": `Bearer ${XOLTA_KEY}`,
                "X-API-Key": XOLTA_KEY
            }
        })
            .then(r => r.json())
            .then(xolta => {
                const xoltaStr = `
                <i class="bi bi-house"></i> ${safe(xolta["Husforbrug"], '')}
                <i class="bi bi-sun"></i> ${safe(xolta["Solceller"], '')}
                <i class="bi bi-battery-charging"></i> ${safe(xolta["Batteri"], 'kW')}
                <i class="bi bi-lightning-charge"></i> ${safe(xolta["Nettet"], 'A')}<br>
                <i class="bi bi-sun"></i> ${safe(xolta["Egenproduktion_pct"], '%')}
                <i class="bi bi-battery-full"></i> ${safe(xolta["Batteri status"], '%')}
                `;
                xoltaTickerInner.innerHTML = xoltaStr;
            })
            .catch(() => {
                xoltaTickerInner.textContent = "Xolta data unavailable";
            });
    }

    fetchAndShowXolta();
    // Optionally, refresh Xolta box every 60 seconds if needed:
    // setInterval(fetchAndShowXolta, 60000);
});
