const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    await page.goto(`file://${__dirname}/index.html`);

    await page.waitForTimeout(2000); // Give enough time for WASM

    await page.evaluate(() => {
        document.querySelectorAll('.opt-lock').forEach(btn => {
            if (btn.innerText.trim() === 'KHÓA') {
                btn.click();
            }
        });
        document.querySelector('button[onclick="optimizeRange()"]').click();
    });

    console.log("Optimization started...");

    await page.waitForFunction(() => {
        const btn = document.querySelector('button[onclick="optimizeRange()"]');
        return btn && !btn.classList.contains('running');
    }, { timeout: 120000 }); // Increase timeout to 120 seconds for CMA-ES

    console.log("Optimization finished. Getting values:");
    const inputs = await page.$$('input[type="number"]');
    for (const input of inputs) {
        const id = await input.getAttribute('id');
        const val = await input.inputValue();
        console.log(`${id}: ${val}`);
    }

    await browser.close();
})();
