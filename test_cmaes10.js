const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    page.on('console', msg => console.log('BROWSER LOG:', msg.text()));

    await page.goto(`http://localhost:8080/index.html`);

    await page.waitForTimeout(1000);

    const optimizePromise = page.evaluate(async () => {
        // Unlock some
        document.getElementById('in-v-bottle').nextElementSibling.click();
        document.getElementById('in-m-empty').nextElementSibling.click();

        // Use a flag to avoid alert freezing testing
        window.alert = console.log;

        await optimizeRange();
    });

    console.log("Optimization started...");

    await optimizePromise;

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
    process.exit(0);
})();
