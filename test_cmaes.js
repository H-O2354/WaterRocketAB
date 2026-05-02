const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    await page.goto(`file://${__dirname}/index.html`);

    // Let WASM load
    await page.waitForTimeout(1000);

    // Open all locks to optimize everything
    const locks = await page.$$('.opt-lock');
    for (const lock of locks) {
        if ((await lock.innerText()).trim() === 'KHÓA') {
            await lock.click();
        }
    }

    // Run CMA-ES
    await page.click('button[onclick="optimizeRange()"]');

    console.log("Optimization started...");

    // Wait until button says "CHẠY TỐI ƯU HÓA CMA-ES" again
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
