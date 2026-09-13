# -*- coding: utf-8 -*-
import base64, os, re, sys

FONT_DIR = r'D:/Преза лекций/шрифты/Кириллица'
SHOT_DIR = r'C:/Users/anank/Desktop/Локатор_скриншоты'
HERE = os.path.dirname(os.path.abspath(__file__))

def b64(p):
    with open(p, 'rb') as f:
        return base64.b64encode(f.read()).decode('ascii')

repl = {
    '__FONT_MANROPE__': b64(os.path.join(FONT_DIR, 'Manrope[wght].ttf')),
    '__FONT_INTER__':   b64(os.path.join(FONT_DIR, 'Inter[opsz,wght].ttf')),
}
for f in os.listdir(SHOT_DIR):
    if f.lower().endswith('.png'):
        key = '__IMG_' + f[:-4].upper() + '__'
        repl[key] = 'data:image/png;base64,' + b64(os.path.join(SHOT_DIR, f))

with open(os.path.join(HERE, 'template.html'), encoding='utf-8') as f:
    html = f.read()
for k, v in repl.items():
    html = html.replace(k, v)

left = set(re.findall(r'__[A-Z0-9_]+__', html))
if left:
    print('НЕ ЗАМЕНЕНО:', left); sys.exit(1)

out = r'D:/Преза лекций/Локатор.html'
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)
print('OK ->', out, '%.2f MB' % (len(html.encode('utf-8'))/1e6))
