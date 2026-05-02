const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    page.on('console', msg => console.log('BROWSER LOG:', msg.text()));

    await page.goto(`file://${__dirname}/index.html`);

    await page.waitForTimeout(1000);

    await page.evaluate(() => {
        // Unlock some
        document.getElementById('in-v-bottle').nextElementSibling.click();
        document.getElementById('in-m-empty').nextElementSibling.click();
        document.querySelector('button[onclick="optimizeRange()"]').click();
    });

    console.log("Optimization started...");

    await page.waitForFunction(() => {
        const btn = document.querySelector('button[onclick="optimizeRange()"]');
        return btn && !btn.classList.contains('running');
    }, { timeout: 120000 });

    console.log("Optimization finished. Getting values:");
    const inputs = await page.$$('input[type="number"]');
    for (const input of inputs) {
        const id = await input.getAttribute('id');
        const val = await input.inputValue();
        if (id === 'in-v-bottle' || id === 'in-m-empty') {
            console.log(`${id}: ${val}`);
        }
    }

    await browser.close();
})();
