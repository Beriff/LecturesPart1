// Сборщик: встраивает шрифты и скриншоты в base64 внутрь template.html -> Локатор.html
const fs = require('fs');
const path = require('path');

const FONT_DIR = 'D:/Преза лекций/шрифты/Кириллица';
const SHOT_DIR = 'C:/Users/anank/Desktop/Локатор_скриншоты';
const HERE = __dirname;

function b64(p) { return fs.readFileSync(p).toString('base64'); }

const fonts = {
  __FONT_MANROPE__: b64(path.join(FONT_DIR, 'Manrope[wght].ttf')),
  __FONT_INTER__:   b64(path.join(FONT_DIR, 'Inter[opsz,wght].ttf')),
};

const shots = {};
for (const f of fs.readdirSync(SHOT_DIR)) {
  if (!/\.png$/i.test(f)) continue;
  const key = '__IMG_' + f.replace(/\.png$/i, '').toUpperCase() + '__'; // __IMG_01_MAIN__
  shots[key] = 'data:image/png;base64,' + b64(path.join(SHOT_DIR, f));
}

let html = fs.readFileSync(path.join(HERE, 'template.html'), 'utf8');
for (const [k, v] of Object.entries(fonts)) html = html.split(k).join(v);
for (const [k, v] of Object.entries(shots)) html = html.split(k).join(v);

// проверка на незаменённые плейсхолдеры
const left = html.match(/__[A-Z0-9_]+__/g);
if (left) { console.error('НЕ ЗАМЕНЕНО:', [...new Set(left)]); process.exit(1); }

const out = path.join('D:/Преза лекций', 'Локатор.html');
fs.writeFileSync(out, html);
console.log('OK ->', out, (html.length/1e6).toFixed(2)+' MB');
console.log('shots:', Object.keys(shots).join(', '));
