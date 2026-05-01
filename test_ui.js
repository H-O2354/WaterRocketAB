const { chromium } = require('playwright');
(async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage();

    page.on('console', msg => console.log('BROWSER CONSOLE:', msg.text()));
    page.on('pageerror', err => console.log('BROWSER ERROR:', err.message));

    await page.goto('http://127.0.0.1:8080');
    await page.waitForTimeout(1000);

    // Unlock multiple inputs to test optimizer
    await page.evaluate(() => {
        let locks = document.querySelectorAll('.opt-lock');
        if(locks.length > 0) locks[0].click();
        if(locks.length > 1) locks[1].click();
    });

    // Start optimizer
    await page.evaluate(() => {
        window.optimizeRange();
    });

    await page.waitForTimeout(5000);

    await browser.close();
})();
