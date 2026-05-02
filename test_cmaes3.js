const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    await page.goto(`file://${__dirname}/index.html`);

    // Let WASM load
    await page.waitForTimeout(1000);

    // Instead of clicking all locks which might be hidden, just execute JS in browser
    await page.evaluate(() => {
        document.querySelectorAll('.opt-lock').forEach(btn => {
            if (btn.innerText.trim() === 'KHÓA') {
                btn.click();
            }
        });
        optimizeRange();
    });

    console.log("Optimization started...");

    await page.waitForFunction(() => {
        const btn = document.querySelector('button[onclick="optimizeRange()"]');
        return !btn.classList.contains('running');
    }, { timeout: 60000 });

    console.log("Optimization finished. Getting values:");
    const inputs = await page.$$('input[type="number"]');
    for (const input of inputs) {
        const id = await input.getAttribute('id');
        const val = await input.inputValue();
        console.log(`${id}: ${val}`);
    }

    await browser.close();
})();
