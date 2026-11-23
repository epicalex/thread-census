// Run after build.py. Only needed when rebuilding the committed image assets.
import { chromium } from 'playwright';
import sharp from 'sharp';
import { readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';
const root = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch({ headless: true, ...(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {}) });
try {
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(path.join(root, 'social-card.svg')).href);
  await page.screenshot({ path: path.join(root, 'social-card.png') });
  const icon = await readFile(path.join(root, 'favicon.svg'));
  await sharp(icon).resize(180, 180).png().toFile(path.join(root, 'apple-touch-icon.png'));
  // ICO supports PNG entries, preserving crisp icons at each browser size.
  const sizes = [16, 32, 48];
  const images = await Promise.all(sizes.map(size => sharp(icon).resize(size, size).png().toBuffer()));
  const header = Buffer.alloc(6 + 16 * sizes.length);
  header.writeUInt16LE(1, 2);
  header.writeUInt16LE(sizes.length, 4);
  let offset = header.length;
  images.forEach((image, i) => {
    const entry = 6 + i * 16;
    header[entry] = header[entry + 1] = sizes[i];
    header.writeUInt16LE(1, entry + 4);
    header.writeUInt16LE(32, entry + 6);
    header.writeUInt32LE(image.length, entry + 8);
    header.writeUInt32LE(offset, entry + 12);
    offset += image.length;
  });
  await writeFile(path.join(root, 'favicon.ico'), Buffer.concat([header, ...images]));
  console.log('Rendered social-card.png, favicon.ico, and apple-touch-icon.png');
} finally {
  await browser.close();
}
