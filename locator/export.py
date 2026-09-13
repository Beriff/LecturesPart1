# -*- coding: utf-8 -*-
"""Рендер 19 слайдов Локатора в PNG (headless Chrome) -> сборка PDF и PPTX."""
import os, subprocess, sys, glob
from PIL import Image

FINAL   = r'D:/Преза лекций/Локатор.html'
WORKDIR = r'C:/Users/anank/AppData/Local/Temp/claude/D--------------/d22b2183-2b83-47c8-be05-17af6a9ad686/scratchpad/export'
CHROME  = r'C:/Program Files/Google/Chrome/Application/chrome.exe'
N       = 19
OUT_DIR = r'D:/Преза лекций'

os.makedirs(WORKDIR, exist_ok=True)
OUTPNG = os.path.join(WORKDIR, 'png'); os.makedirs(OUTPNG, exist_ok=True)

# 1) render-вариант: показать слайд из #hash, без анимаций, без служебных элементов
with open(FINAL, encoding='utf-8') as f:
    html = f.read()
inject = """
<style id="rov">#dots,.hint{display:none!important}.slide{transition:none!important}</style>
<script id="rjs">(function(){function pick(){var n=parseInt(location.hash.slice(1))||0;if(window.go)go(n);}window.addEventListener('hashchange',pick);if(document.readyState!=='loading')pick();else window.addEventListener('load',pick);})();</script>
</body>"""
html = html.replace('</body>', inject, 1)
render = os.path.join(WORKDIR, 'render.html')
with open(render, 'w', encoding='utf-8') as f:
    f.write(html)
render_url = 'file:///' + render.replace('\\', '/')

# 2) рендер каждого слайда
pngs = []
for n in range(N):
    out = os.path.join(OUTPNG, f'slide_{n:02d}.png')
    if os.path.exists(out): os.remove(out)
    cmd = [CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
           '--force-device-scale-factor=1', '--default-background-color=00000000',
           '--window-size=1920,1080', '--virtual-time-budget=4000',
           f'--screenshot={out}', f'{render_url}#{n}']
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    im = Image.open(out).convert('RGB')
    if im.size != (1920, 1080):
        im = im.resize((1920, 1080))
    im.save(out)
    pngs.append(out)
    print(f'slide {n+1:02d}/{N} -> {im.size}')

# 3) PDF (19 страниц 1920x1080) через PyMuPDF — отдельный файл из HTML
import fitz
pdf_path = os.path.join(OUT_DIR, 'Локатор (HTML).pdf')
doc = fitz.open()
for p in pngs:
    page = doc.new_page(width=1920, height=1080)
    page.insert_image(fitz.Rect(0, 0, 1920, 1080), filename=p)
doc.save(pdf_path, garbage=4, deflate=True, deflate_images=True)
doc.close()
print('PDF ->', pdf_path)
import sys; sys.exit(0)  # PPTX не трогаем — редактируемая версия уже готова

# 4) PPTX (16:9, каждый слайд = картинка на весь лист)
from pptx import Presentation
from pptx.util import Inches
prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]
for p in pngs:
    s = prs.slides.add_slide(blank)
    s.shapes.add_picture(p, 0, 0, width=prs.slide_width, height=prs.slide_height)
pptx_path = os.path.join(OUT_DIR, 'Локатор.pptx')
prs.save(pptx_path)
print('PPTX ->', pptx_path)
print('DONE')
