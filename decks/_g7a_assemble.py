# Склейка сборщика: база (сцены, движок) + три части слайдов
import pathlib
H = pathlib.Path(__file__).parent
b = (H / "_glava7app_build.py").read_text(encoding="utf-8")
if "# ================================================================ SLIDES — повторяют" in b:
    b = b[:b.index("\n# ================================================================ SLIDES — повторяют")] + "\n"
    b = b.rstrip()
    if b.endswith("render()"):
        b = b[:-len("render()")]
else:
    b = b.replace("from _g7a_lib import SCENES, scene, esc, icon, hexicon, svgicon, hexnode, flow, seq, arrow, COLS",
                  "from _g7a_lib import SCENES, scene, esc, icon, hexicon, svgicon, hexnode, flow, seq, arrow, COLS, IC")
    b = b.replace('CSS.replace("__OSW__", osw).replace("__BGI__", BGI)', '(CSS + CSS2 + CSS3).replace("__OSW__", osw).replace("__BGI__", BGI)')
    b = b.rstrip()
    assert b.endswith("render()")
    b = b[:-len("render()")]
a = (H / "_g7a_part_a.py").read_text(encoding="utf-8").replace("from _g7a_ui import (", "from _g7a_css3 import CSS3\nfrom _g7a_ui import (", 1)
pb = (H / "_g7a_part_b.py").read_text(encoding="utf-8").replace(
    """URLBAR.replace('data-id="url"', 'data-id="url0" class="url split"', 1).replace('class="url" ', '')""",
    """URLBAR.replace('class="url" data-id="url"', 'class="url split"', 1)""")
c = (H / "_g7a_part_c.py").read_text(encoding="utf-8")
(H / "_glava7app_build.py").write_text(b + "\n" + a + pb + c + "\nrender()\n", encoding="utf-8")
print("ok")
