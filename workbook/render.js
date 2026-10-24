// usage: node render.js <html> <pdf> [pngDir] [pngPrefix]
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [html, pdf, pngDir, prefix = 'page'] = process.argv.slice(2);
  const browser = await chromium.launch();
  const scale = 1545 / 816; // match workbook page PNGs (1545 x 1999)
  const page = await browser.newPage({ viewport: { width: 816, height: 1056 }, deviceScaleFactor: scale });
  await page.goto('file://' + html);
  await page.waitForSelector('body[data-ready="1"]');
  await page.pdf({ path: pdf, width: '8.5in', height: '11in', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  if (pngDir) {
    fs.mkdirSync(pngDir, { recursive: true });
    const pages = await page.$$('.page');
    for (let i = 0; i < pages.length; i++) {
      await pages[i].screenshot({ path: `${pngDir}/${prefix}-${String(i + 1).padStart(2, '0')}.png` });
    }
  }
  await browser.close();
})();
