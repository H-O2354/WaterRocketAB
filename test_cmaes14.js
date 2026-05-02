const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    page.on('console', msg => console.log('BROWSER LOG:', msg.text()));

    await page.goto(`http://localhost:8080/index.html`);

    await page.waitForTimeout(1000);

    // ensure it's defined
    let defined = await page.evaluate(() => {
        return typeof window.WasmCmaes !== 'undefined';
    });
    console.log("Is WasmCmaes defined?", defined);

    await page.evaluate(() => {
        // Unlock some
        document.getElementById('in-v-bottle').nextElementSibling.click();
        document.getElementById('in-m-empty').nextElementSibling.click();

        let btn = document.querySelector('button[onclick="optimizeRange()"]');
        if(btn) btn.click();
    });

    console.log("Optimization started...");

    await page.waitForFunction(() => {
        const btn = document.querySelector('button[onclick="optimizeRange()"]');
        return btn && btn.innerText.includes('CHẠY');
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
    process.exit(0);
})();
