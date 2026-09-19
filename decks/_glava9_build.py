# -*- coding: utf-8 -*-
# Сборка decks/glava9-network.html — Глава 9. Сетевой уровень (IPv4, IPv6, маршрутизация)
import math, json, pathlib, re

HERE = pathlib.Path(__file__).parent
OUT = HERE / "glava9-network.html"

# ---------------------------------------------------------------- scene helpers
SCENES = {}

def track(n, keys, default):
    out, v = [], default
    for i in range(n + 1):
        if i in keys:
            v = keys[i]
        out.append(v)
    return out

def scene(name, n, els, waits=None):
    """els: {id: {"p": {step:(x,y)}, "o": {step:op}, "c": {step:cls}, "t": {step:text}}}"""
    spec = {"n": n, "w": [(waits or {}).get(i, 1100) for i in range(n + 1)], "e": {}}
    for eid, tr in els.items():
        e = {}
        if "p" in tr: e["p"] = track(n, tr["p"], (0, 0))
        if "o" in tr: e["o"] = track(n, tr["o"], 1)
        if "c" in tr: e["c"] = track(n, tr["c"], "")
        if "t" in tr: e["t"] = track(n, tr["t"], "")
        spec["e"][eid] = e
    SCENES[name] = spec
    return f'data-scene="{name}"'

def f1(v): return f"{v:.1f}".rstrip("0").rstrip(".")

# ---------------------------------------------------------------- symbols
def rt_arrows():
    s = ""
    for ang, out in ((45, True), (225, True), (135, False), (315, False)):
        a = math.radians(ang); ux, uy = math.cos(a), math.sin(a)
        r0, r1 = (7, 27) if out else (27, 9)
        x0, y0, x1, y1 = ux * r0, uy * r0, ux * r1, uy * r1
        dx, dy = (ux, uy) if out else (-ux, -uy)
        bx, by = x1 - dx * 9, y1 - dy * 9
        nx, ny = -dy, dx
        s += (f'<line x1="{f1(x0)}" y1="{f1(y0)}" x2="{f1(bx)}" y2="{f1(by)}"/>'
              f'<polygon points="{f1(x1)},{f1(y1)} {f1(bx+nx*5.5)},{f1(by+ny*5.5)} {f1(bx-nx*5.5)},{f1(by-ny*5.5)}"/>')
    return s

DEFS = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
        '<linearGradient id="gR" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fb4ff"/><stop offset="1" stop-color="#4b4fd8"/></linearGradient>'
        '<linearGradient id="gT" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b9d0ff"/><stop offset="1" stop-color="#8fb4ff"/></linearGradient>'
        '<symbol id="rt" viewBox="0 0 120 84"><path d="M2 26V58A58 18 0 0 0 118 58V26Z" fill="url(#gR)"/>'
        '<ellipse cx="60" cy="26" rx="58" ry="18" fill="url(#gT)" stroke="rgba(255,255,255,.7)" stroke-width="1.5"/>'
        '<g transform="translate(60 26) scale(1 .5)" stroke="#fff" stroke-width="4" fill="#fff" stroke-linecap="round">' + rt_arrows() + '</g></symbol>'
        '<symbol id="pc" viewBox="0 0 80 66"><rect x="2" y="2" width="76" height="48" rx="7" fill="rgba(255,255,255,.18)" stroke="#fff" stroke-width="2.5"/>'
        '<rect x="9" y="9" width="62" height="34" rx="3" fill="url(#gR)"/><path d="M33 51h14v7h9v5H24v-5h9z" fill="#fff" opacity=".85"/></symbol>'
        '<symbol id="sw" viewBox="0 0 120 54"><rect x="2" y="2" width="116" height="50" rx="10" fill="url(#gR)" stroke="rgba(255,255,255,.7)" stroke-width="1.5"/>'
        '<g stroke="#fff" stroke-width="4" fill="#fff" stroke-linecap="round"><line x1="34" y1="19" x2="80" y2="19"/><polygon points="90,19 79,13 79,25"/>'
        '<line x1="86" y1="35" x2="40" y2="35"/><polygon points="30,35 41,29 41,41"/></g></symbol>'
        '<symbol id="srv" viewBox="0 0 64 84"><rect x="2" y="2" width="60" height="80" rx="8" fill="url(#gR)" stroke="rgba(255,255,255,.7)" stroke-width="1.5"/>'
        '<g stroke="#fff" stroke-width="4" stroke-linecap="round"><line x1="14" y1="20" x2="50" y2="20"/><line x1="14" y1="34" x2="50" y2="34"/></g><circle cx="46" cy="66" r="4" fill="#5ddcb0"/></symbol>'
        '</defs></svg>')

def rt(cx, cy, w=124, label=""):
    h = w * .7
    s = f'<use href="#rt" x="{f1(cx-w/2)}" y="{f1(cy-h/2)}" width="{w}" height="{f1(h)}"/>'
    if label: s += f'<text class="nl" x="{cx}" y="{f1(cy+h/2+28)}" text-anchor="middle">{label}</text>'
    return s

def pcsym(cx, cy, label="", w=86, sym="pc"):
    h = w * (66 / 80) if sym == "pc" else (w * 84 / 64 if sym == "srv" else w * 54 / 120)
    s = f'<use href="#{sym}" x="{f1(cx-w/2)}" y="{f1(cy-h/2)}" width="{w}" height="{f1(h)}"/>'
    if label: s += f'<text class="nl" x="{cx}" y="{f1(cy+h/2+28)}" text-anchor="middle">{label}</text>'
    return s

def pkt(eid, label, cls="pk-m", w=110, h=40, extra="", sub=""):
    t2 = f'<text class="pks" y="{h/2+20}" text-anchor="middle" data-id="{eid}-s">{sub}</text>' if sub is not None else ""
    return (f'<g class="an" data-id="{eid}" {extra}><rect class="{cls}" x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="9"/>'
            f'<text class="pkt" y="7" text-anchor="middle" data-id="{eid}-t">{label}</text>{t2}</g>')

def cap(eid, x, y, anchor="middle", cls="cap"):
    return f'<text class="{cls} an" data-id="{eid}" x="{x}" y="{y}" text-anchor="{anchor}"></text>'

def svg(vb, body, cls="dg"):
    return f'<svg class="{cls}" viewBox="{vb}" role="img">{body}</svg>'

# ---------------------------------------------------------------- 1. encapsulation
ENC_ROWS = [(70, "Транспортный уровень (L4)"), (190, "Сетевой уровень (L3)"), (310, "Канальный уровень (L2)")]
enc = "".join(f'<line class="row" x1="20" y1="{y+42}" x2="980" y2="{y+42}"/><text class="rowt" x="24" y="{y-26}">{t}</text>' for y, t in ENC_ROWS)
enc += ('<g class="an" data-id="seg"><rect class="bx sky" x="0" y="0" width="130" height="58" rx="10"/><text class="bxt" x="65" y="37" text-anchor="middle">TCP</text>'
        '<rect class="bx mint" x="134" y="0" width="200" height="58" rx="10"/><text class="bxt" x="234" y="37" text-anchor="middle">Данные</text></g>'
        '<g class="an" data-id="ip"><rect class="bx pink" x="0" y="0" width="150" height="58" rx="10"/><text class="bxt" x="75" y="37" text-anchor="middle">Заголовок IP</text></g>'
        '<g class="an" data-id="fh"><rect class="bx fr" x="0" y="0" width="166" height="58" rx="10"/><text class="bxt" x="83" y="37" text-anchor="middle">Заголовок кадра</text></g>'
        '<g class="an" data-id="ft"><rect class="bx fr" x="0" y="0" width="72" height="58" rx="10"/><text class="bxt" x="36" y="37" text-anchor="middle">FCS</text></g>')
enc += cap("ecap", 500, 420)
L4, L3, L2 = (330, 42), (560, 162), (560, 282)
ENCAP = svg("0 0 1000 440", enc)
ENC_SC = scene("encap", 9, {
    "seg": {"p": {0: L4, 2: L3, 4: L2, 7: L3, 9: L4}, "o": {0: 0, 1: 1}},
    "ip": {"p": {0: (406, 60), 3: (406, 162), 4: (406, 282), 7: (406, 162), 8: (300, 100)}, "o": {0: 0, 3: 1, 8: 0}},
    "fh": {"p": {0: (236, 230), 5: (236, 282), 6: (160, 360)}, "o": {0: 0, 5: 1, 6: 0}},
    "ft": {"p": {0: (898, 230), 5: (898, 282), 6: (960, 360)}, "o": {0: 0, 5: 1, 6: 0}},
    "ecap": {"t": {1: "Сегмент приходит от транспортного уровня", 2: "Сегмент на сетевом уровне",
                   3: "Инкапсуляция: к данным добавляется заголовок IP", 4: "Пакет передаётся на канальный уровень",
                   5: "Инкапсуляция на L2: добавляются заголовок кадра и концевик (FCS) — получился кадр",
                   6: "У получателя: канальный уровень удаляет заголовок и концевик кадра",
                   7: "Пакет передаётся на сетевой уровень", 8: "Декапсуляция: заголовок пакета удаляется",
                   9: "Сегмент передаётся протоколу транспортного уровня"}},
}, {1: 900, 2: 1200, 3: 1200, 4: 1300, 5: 1600, 6: 1500, 7: 1200, 8: 1100, 9: 1200})

# ---------------------------------------------------------------- 2. connectionless
cl = pcsym(110, 210, "PC-1") + pcsym(890, 210, "PC-2")
cl += '<path class="dr an" data-id="ln" pathLength="1" d="M165 210H835"/>'
cl += pkt("cp", "IP-пакет", "pk-m", 120, 40, 'style="--md:1600ms"', None)
cl += ('<g class="an" data-id="b1"><rect class="bub" x="30" y="30" width="400" height="84" rx="16"/>'
       '<text class="bubt" x="50" y="64">Отправитель: способен ли получатель</text><text class="bubt" x="50" y="94">принять пакет и обработать его?</text></g>'
       '<g class="an" data-id="b2"><rect class="bub" x="570" y="30" width="400" height="84" rx="16"/>'
       '<text class="bubt" x="590" y="64">Получатель: неизвестно, когда</text><text class="bubt" x="590" y="94">и придёт ли пакет вообще</text></g>')
CONN = svg("0 0 1000 320", cl)
CONN_SC = scene("conn", 4, {
    "ln": {"c": {0: "", 1: "on"}},
    "cp": {"p": {0: (230, 170), 2: (770, 170)}, "o": {0: 0, 2: 1}},
    "b1": {"o": {0: 0, 3: 1}, "p": {0: (0, 10), 3: (0, 0)}},
    "b2": {"o": {0: 0, 4: 1}, "p": {0: (0, 10), 4: (0, 0)}},
}, {1: 900, 2: 1800, 3: 900, 4: 900})

# ---------------------------------------------------------------- 3. unreliable
ur = pcsym(90, 200, "Отправитель") + pcsym(910, 200, "Получатель")
for y in (110, 200, 290):
    ur += f'<line class="lane" x1="150" y1="{y}" x2="850" y2="{y}"/>'
ur += pkt("u1", "1", "pk-m", 64, 40, 'style="--md:2600ms"', None)
ur += pkt("u2", "2", "pk-m", 64, 40, 'style="--md:1300ms;--dl:150ms"', None)
ur += pkt("u3", "3", "pk-m", 64, 40, 'style="--md:1000ms;--dl:300ms"', None)
ur += '<g class="an" data-id="ux"><path class="xm" d="M478 272l44 36M522 272l-44 36"/><text class="lost" x="500" y="258" text-anchor="middle">потерян</text></g>'
ur += cap("uq", 910, 380, cls="capm")
ur += cap("ucap", 500, 40)
UNREL = svg("0 0 1000 400", ur)
UNREL_SC = scene("unrel", 4, {
    "u1": {"p": {0: (190, 110), 1: (800, 110)}},
    "u2": {"p": {0: (190, 290), 1: (500, 290)}, "o": {0: 1, 2: 0}},
    "u3": {"p": {0: (190, 200), 1: (800, 200)}},
    "ux": {"o": {0: 0, 2: 1}},
    "uq": {"t": {0: "", 3: "порядок: 3, 1"}},
    "ucap": {"t": {0: "Отправлены пакеты 1, 2, 3", 2: "Пакет 2 не дошёл", 3: "Пакет 3 пришёл раньше пакета 1",
                   4: "IP не предпринимает никаких действий: нет повтора, нет исправления порядка"}},
}, {1: 2800, 2: 1000, 3: 1000, 4: 1000})

# ---------------------------------------------------------------- 4. MTU
mt = ('<rect class="pipe" x="30" y="130" width="400" height="120" rx="14"/><text class="pipet" x="230" y="290" text-anchor="middle">Сеть 1: MTU больше</text>'
      '<rect class="pipe nar" x="570" y="160" width="410" height="60" rx="12"/><text class="pipet" x="775" y="260" text-anchor="middle">Сеть 2: MTU меньше</text>')
mt += rt(500, 190, 130, "R1")
mt += ('<g class="an" data-id="big" style="--md:1200ms"><rect class="pk-m" x="-130" y="-38" width="260" height="76" rx="10"/>'
       '<text class="pkt" y="-4" text-anchor="middle">Пакет</text><text class="pks2" y="24" text-anchor="middle">Identification = 0x1a2b</text></g>')
for i, (mf, off) in enumerate(((1, 0), (1, 60), (0, 120))):
    mt += (f'<g class="an" data-id="f{i}" style="--md:1000ms"><rect class="pk-s" x="-52" y="-20" width="104" height="40" rx="8"/>'
           f'<text class="pkt sm" y="6" text-anchor="middle">фрагм. {i+1}</text>'
           f'<g class="an" data-id="fl{i}"><text class="flg" y="-34" text-anchor="middle">MF={mf}</text><text class="flg" y="-56" text-anchor="middle">Offset={off}</text></g></g>')
mt += cap("mcap", 500, 360)
MTU = svg("0 0 1000 380", mt)
MTU_SC = scene("mtu", 6, {
    "big": {"p": {0: (170, 190), 1: (300, 190)}, "o": {0: 0, 1: 1, 2: 0}},
    "f0": {"p": {0: (500, 190), 3: (910, 190)}, "o": {0: 0, 2: 1}},
    "f1": {"p": {0: (500, 190), 4: (790, 190)}, "o": {0: 0, 2: 1}},
    "f2": {"p": {0: (500, 190), 5: (670, 190)}, "o": {0: 0, 2: 1}},
    "fl0": {"o": {0: 0, 6: 1}}, "fl1": {"o": {0: 0, 6: 1}}, "fl2": {"o": {0: 0, 6: 1}},
    "mcap": {"t": {1: "Пакет доходит до R1 и упирается в сеть с меньшим MTU", 2: "R1 фрагментирует пакет на три части",
                   3: "Фрагменты уходят по очереди", 6: "Identification одинаковый; MF=0 и смещение у последнего фрагмента"}},
}, {1: 1400, 2: 900, 3: 1100, 4: 1100, 5: 1100, 6: 900})

# ---------------------------------------------------------------- 5. TTL
tt = '<line class="lnk" x1="60" y1="230" x2="960" y2="230"/>'
tt += pcsym(60, 230, "PC") + pcsym(225, 230, "Коммутатор", 110, "sw") + rt(400, 230, 120, "R1")
tt += ('<g><ellipse cx="580" cy="232" rx="70" ry="38" fill="rgba(255,255,255,.85)"/><ellipse cx="555" cy="210" rx="36" ry="30" fill="rgba(255,255,255,.85)"/>'
       '<ellipse cx="605" cy="214" rx="30" ry="24" fill="rgba(255,255,255,.85)"/><text x="580" y="240" text-anchor="middle" class="cloudt">…</text></g>')
tt += rt(760, 230, 120, "R2") + pcsym(960, 230, "8.8.8.8", 58, "srv")
tt += pkt("tp", "TTL=128", "pk-p", 130, 40, 'style="--md:900ms"', None)
tt += pkt("tr", "ответ TTL=104", "pk-m", 190, 40, 'style="--md:2600ms"', None)
tt += cap("tcap", 520, 60)
TTLSVG = svg("0 0 1060 320", tt)
TTL_SC = scene("ttl", 10, {
    "tp": {"p": {0: (60, 150), 2: (225, 150), 3: (400, 150), 5: (580, 150), 7: (760, 150), 9: (960, 150)}, "o": {0: 0, 1: 1, 10: 0}},
    "tp-t": {"t": {0: "TTL=128", 4: "TTL=127", 6: "TTL=105", 8: "TTL=104"}, "c": {0: "pkt", 4: "pkt hit", 5: "pkt", 6: "pkt hit", 7: "pkt", 8: "pkt hit", 9: "pkt"}},
    "tr": {"p": {0: (960, 150), 10: (110, 150)}, "o": {0: 0, 10: 1}},
    "tcap": {"t": {1: "ping 8.8.8.8: пакет отправлен с TTL=128", 2: "Коммутатор не уменьшает TTL – он работает на канальном уровне",
                   3: "Маршрутизатор обрабатывает пакет", 4: "Маршрутизатор уменьшает TTL на 1: 127", 5: "Пакет проходит через другие маршрутизаторы сети",
                   6: "…каждый уменьшает TTL на 1", 7: "Последний маршрутизатор на пути", 8: "Уменьшает TTL на 1: 104",
                   9: "8.8.8.8 формирует эхо-ответ с оставшимся значением TTL=104", 10: "Пришёл ответ TTL=104: пакет сделал 128 – 104 = 24 прыжка"}},
}, {1: 900, 2: 1100, 3: 1000, 4: 900, 5: 1000, 6: 900, 7: 1000, 8: 900, 9: 1300, 10: 2800})

te = '<line class="lnk" x1="90" y1="220" x2="1010" y2="220"/>'
te += pcsym(90, 220, "Отправитель") + rt(400, 220, 124, "R1") + rt(700, 220, 124, "R2") + pcsym(1010, 220, "Назначение", 58, "srv")
te += pkt("ep", "TTL=1", "pk-m", 110, 40, "", None)
te += '<g class="an" data-id="ex"><path class="xm" d="M378 108l44 36M422 108l-44 36"/></g>'
te += pkt("eb", "Time Exceeded", "pk-p", 190, 40, 'style="--md:1500ms"', None)
te += cap("ecp", 550, 50)
TESVG = svg("0 0 1100 310", te)
TE_SC = scene("te", 5, {
    "ep": {"p": {0: (90, 126), 1: (400, 126)}, "o": {0: 1, 3: 0}},
    "ep-t": {"t": {0: "TTL=1", 2: "TTL=0"}, "c": {0: "pkt", 2: "pkt hit"}},
    "ex": {"o": {0: 0, 3: 1}},
    "eb": {"p": {0: (400, 126), 5: (130, 126)}, "o": {0: 0, 4: 1}},
    "ecp": {"t": {1: "Пакет с TTL=1 приходит на R1", 2: "R1 сначала обрабатывает пакет", 3: "…и лишь затем отбрасывает его",
                  4: "R1 уведомляет отправителя сообщением Time Exceeded", 5: "Отправитель узнаёт, что время жизни пакета истекло"}},
}, {1: 1200, 2: 900, 3: 900, 4: 900, 5: 1700})

# ---------------------------------------------------------------- 6. extension headers chain
ch = ""
BOX = [("hd0", 20, "Основной заголовок IPv6", "Routing"), ("hd1", 330, "Routing Header", "Fragment"),
       ("hd2", 640, "Fragment Header", "TCP (6)")]
for eid, x, t, nh in BOX:
    ch += (f'<g class="an" data-id="{eid}"><rect class="bx glass" x="{x}" y="60" width="260" height="130" rx="16"/>'
           f'<text class="bxt" x="{x+20}" y="100">{t}</text><text class="rowt" x="{x+20}" y="128">…</text>'
           f'<rect class="bx sky" x="{x+16}" y="140" width="228" height="36" rx="8"/><text class="nh" x="{x+30}" y="165">Next Header: {nh}</text></g>')
ch += ('<g class="an" data-id="hd3"><rect class="bx mint" x="950" y="60" width="130" height="130" rx="16"/>'
       '<text class="bxt" x="1015" y="118" text-anchor="middle">TCP-</text><text class="bxt" x="1015" y="146" text-anchor="middle">сегмент</text></g>')
for i, x in enumerate((260, 570, 880)):
    ch += f'<path class="dr an" data-id="ha{i}" pathLength="1" d="M{x} 158 C{x+30} 158 {x+40} 125 {x+68} 125"/>'
EXT = svg("0 0 1100 230", ch)
_ext = {"hd0": {"o": {0: 0, 1: 1}}}
for i in range(1, 4):
    st = 2 * i
    _ext[f"ha{i-1}"] = {"c": {0: "", st: "on"}}
    _ext[f"hd{i}"] = {"p": {0: (-150, 0), st + 1: (0, 0)}, "o": {0: 0, st + 1: 1}}
EXT_SC = scene("ext", 7, _ext, {1: 700, 2: 800, 3: 1100, 4: 800, 5: 1100, 6: 800, 7: 1100})

# ---------------------------------------------------------------- 7. topology / path of packet
X = {"PCA": 70, "R1": 300, "R2": 600, "R3": 900, "PCB": 1130}
LY = 290  # link y
IFS = [("E1", 212, "192.168.1.1", "AA-AA-AA-AA-AA-AA", 0), ("E2", 388, "10.10.0.1", "AA-BB-BB-BB-BB-BB", 1),
       ("T1", 512, "10.10.0.2", "AA-CC-CC-CC-CC-CC", 0), ("T2", 688, "10.10.1.1", "AA-DD-DD-DD-DD-DD", 1),
       ("G1", 812, "10.10.1.2", "AA-EE-EE-EE-EE-EE", 0), ("G2", 988, "192.168.3.1", "AA-FF-FF-FF-FF-FF", 1)]
ROUTES = {
    "R1": ["C 192.168.1.0/24 E1", "C 10.10.0.0/30 E2", "S 192.168.3.0/24 via 10.10.0.2"],
    "R2": ["C 10.10.0.0/30 T1", "C 10.10.1.0/30 T2", "S 192.168.3.0/24 via 10.10.1.2", "S 192.168.1.0/24 via 10.10.0.1"],
    "R3": ["C 10.10.1.0/30 G1", "C 192.168.3.0/24 G2", "S 192.168.1.0/24 via 10.10.1.1"],
}

def topo(build=False, tables=False, addr=True):
    def s(k, dl=0):
        return f' data-s="{k}" style="--dl:{dl}ms"' if build else ""
    b = ""
    y0 = 250 if tables else 0
    # links
    links = [(110, 190, None), (410, 490, "10.10.0.0/30"), (710, 790, "10.10.1.0/30"), (1010, 1090, None)]
    for i, (a, c, lab) in enumerate(links):
        b += f'<g class="arr c-mint"{s(2, i*120)}><path class="draw" pathLength="1" d="M{a} {LY}H{c}"/></g>' if build else f'<line class="lnk" x1="{a}" y1="{LY}" x2="{c}" y2="{LY}"/>'
    b += f'<line class="lnk" x1="{X["PCA"]}" y1="{LY}" x2="110" y2="{LY}"/><line class="lnk" x1="1090" y1="{LY}" x2="{X["PCB"]}" y2="{LY}"/>' if not build else ""
    # nodes
    b += f'<g{s(1,0)}>' + pcsym(X["PCA"], LY, "PC-A") + '</g>'
    for i, r in enumerate(("R1", "R2", "R3")):
        b += f'<g{s(1,(i+1)*110)}>' + rt(X[r], LY, 128, r) + '</g>'
    b += f'<g{s(1,440)}>' + pcsym(X["PCB"], LY, "PC-B") + '</g>'
    # interfaces
    for i, (n, x, ip, mac, row) in enumerate(IFS):
        b += (f'<g{s(3, i*80)}><rect class="ifb" x="{x-19}" y="{LY-15}" width="38" height="30" rx="7"/>'
              f'<text class="ift" x="{x}" y="{LY+6}" text-anchor="middle">{n}</text>')
        if addr:
            yy = LY + 72 + row * 46
            b += (f'<text class="adr" x="{x}" y="{yy}" text-anchor="middle">{ip}</text>'
                  f'<text class="adr dim" x="{x}" y="{yy+18}" text-anchor="middle">{mac}</text>')
        b += '</g>'
    # subnets
    b += (f'<g{s(4,0)}><rect class="sn" x="382" y="{LY+20}" width="136" height="28" rx="14"/><text class="snt" x="450" y="{LY+39}" text-anchor="middle">10.10.0.0/30</text>'
          f'<rect class="sn" x="682" y="{LY+20}" width="136" height="28" rx="14"/><text class="snt" x="750" y="{LY+39}" text-anchor="middle">10.10.1.0/30</text></g>'
          f'<g{s(4,150)}><rect class="sn lan" x="8" y="{LY+136}" width="160" height="28" rx="14"/><text class="snt" x="88" y="{LY+155}" text-anchor="middle">192.168.1.0/24</text>'
          f'<rect class="sn lan" x="1032" y="{LY+136}" width="160" height="28" rx="14"/><text class="snt" x="1112" y="{LY+155}" text-anchor="middle">192.168.3.0/24</text></g>')
    b += (f'<g{s(3, 500)}><text class="adr" x="8" y="{LY+186}" text-anchor="start">192.168.1.2</text>'
          f'<text class="adr dim" x="8" y="{LY+204}" text-anchor="start">AA-BB-CC-11-22-33</text>'
          f'<text class="adr" x="1192" y="{LY+186}" text-anchor="end">192.168.3.2</text>'
          f'<text class="adr dim" x="1192" y="{LY+204}" text-anchor="end">AA-BB-CC-22-33-44</text></g>')
    return b

def rtables():
    b = ""
    for r, rows in ROUTES.items():
        x = X[r] - 140
        h = 34 + len(rows) * 26
        b += (f'<g data-id="tb{r}" class="an"><rect class="rtb" x="{x}" y="{190-h}" width="280" height="{h}" rx="12"/>'
              f'<text class="rth" x="{x+14}" y="{190-h+23}">{r}# show ip route</text>')
        for i, row in enumerate(rows):
            yy = 190 - h + 34 + i * 26
            b += (f'<rect class="rhit an" data-id="h{r}{i}" x="{x+6}" y="{yy}" width="268" height="24" rx="6"/>'
                  f'<text class="rtr" x="{x+14}" y="{yy+17}"><tspan class="{"cC" if row[0]=="C" else "cS"}">{row[0]}</tspan>{row[1:]}</text>')
        b += '</g>'
    return b

TOPO_BUILD = svg("0 205 1200 300", topo(build=True))

# path scene
PY = 222
path_body = topo(False, True) + rtables()
path_body += ('<g class="an" data-id="pp" style="--md:1300ms"><rect class="pk-m" x="-62" y="-20" width="124" height="40" rx="9"/>'
              '<text class="pkt sm" y="6" text-anchor="middle" data-id="ppt">TTL 255</text></g>')
PATH_SVG = svg("0 40 1200 465", path_body.replace(f'y1="{LY}"', f'y1="{LY}"'))

FWD = [  # pos, ttl, smac, dmac, panel, hit, caption
    ("PCA", 255, "—", "—", 0, None, "PC-A: сеть 192.168.3.0/24 чужая – пакет поручается шлюзу по умолчанию"),
    ("PCA", 255, "AA-BB-CC-11-22-33", "AA-AA-AA-AA-AA-AA", 0, None, "PC-A узнал MAC шлюза через ARP и сформировал кадр"),
    ("R1", 255, "AA-BB-CC-11-22-33", "AA-AA-AA-AA-AA-AA", 1, "R12", "R1 распаковывает кадр и сверяет DstIP с таблицей маршрутизации"),
    ("R1", 254, "AA-BB-BB-BB-BB-BB", "AA-CC-CC-CC-CC-CC", 1, "R12", "R1: новый кадр с интерфейса E2, TTL 255 – 1 = 254"),
    ("R2", 254, "AA-BB-BB-BB-BB-BB", "AA-CC-CC-CC-CC-CC", 2, "R22", "R2 отбрасывает заголовок L2 и сверяет DstIP с таблицей"),
    ("R2", 253, "AA-DD-DD-DD-DD-DD", "AA-EE-EE-EE-EE-EE", 2, "R22", "R2: новый кадр с интерфейса T2, TTL 254 – 1 = 253"),
    ("R3", 253, "AA-DD-DD-DD-DD-DD", "AA-EE-EE-EE-EE-EE", 3, "R31", "R3: сеть назначения подключена за интерфейсом G2"),
    ("R3", 252, "AA-FF-FF-FF-FF-FF", "AA-BB-CC-22-33-44", 3, "R31", "R3: кадр непосредственно получателю, TTL 253 – 1 = 252"),
    ("PCB", 252, "AA-FF-FF-FF-FF-FF", "AA-BB-CC-22-33-44", 4, None, "PC-B получил пакет. IP-адреса не менялись, MAC – на каждом участке"),
]
REV = [
    ("PCB", 255, "—", "—", 4, None, "Ответ: PC-B отправляет пакет на PC-A через шлюз 192.168.3.1"),
    ("PCB", 255, "AA-BB-CC-22-33-44", "AA-FF-FF-FF-FF-FF", 4, None, "PC-B формирует кадр на MAC шлюза R3"),
    ("R3", 255, "AA-BB-CC-22-33-44", "AA-FF-FF-FF-FF-FF", 3, "R32", "R3: сеть 192.168.1.0/24 известна через соседа 10.10.1.1"),
    ("R3", 254, "AA-EE-EE-EE-EE-EE", "AA-DD-DD-DD-DD-DD", 3, "R32", "R3: кадр с интерфейса G1, TTL 254"),
    ("R2", 254, "AA-EE-EE-EE-EE-EE", "AA-DD-DD-DD-DD-DD", 2, "R23", "R2: сеть 192.168.1.0/24 известна через соседа 10.10.0.1"),
    ("R2", 253, "AA-CC-CC-CC-CC-CC", "AA-BB-BB-BB-BB-BB", 2, "R23", "R2: кадр с интерфейса T1, TTL 253"),
    ("R1", 253, "AA-CC-CC-CC-CC-CC", "AA-BB-BB-BB-BB-BB", 1, "R10", "R1: сеть 192.168.1.0/24 подключена за интерфейсом E1"),
    ("R1", 252, "AA-AA-AA-AA-AA-AA", "AA-BB-CC-11-22-33", 1, "R10", "R1: кадр непосредственно PC-A, TTL 252"),
    ("PCA", 252, "AA-AA-AA-AA-AA-AA", "AA-BB-CC-11-22-33", 0, None, "PC-A получил ответ – весь процесс повторился в обратном порядке"),
]

def path_scene(name, seq, rev):
    n = len(seq) - 1
    els = {"pp": {"p": {}}, "ppt": {"t": {}, "c": {}}, "sip": {"t": {}}, "dip": {"t": {}}, "ttl": {"t": {}},
           "smac": {"t": {}}, "dmac": {"t": {}}, "pcap": {"t": {}}}
    for r, rows in ROUTES.items():
        for i in range(len(rows)): els[f"h{r}{i}"] = {"o": {0: 0}}
    waits = {}
    prev = None
    for k, (pos, ttl, sm, dm, pan, hit, capt) in enumerate(seq):
        els["pp"]["p"][k] = (X[pos], PY)
        els["ppt"]["t"][k] = f"TTL {ttl}"
        els["ppt"]["c"][k] = "pkt sm hit" if prev and prev[1] != ttl else "pkt sm"
        els["sip"]["t"][k] = "192.168.3.2" if rev else "192.168.1.2"
        els["dip"]["t"][k] = "192.168.1.2" if rev else "192.168.3.2"
        els["ttl"]["t"][k] = str(ttl); els["smac"]["t"][k] = sm; els["dmac"]["t"][k] = dm
        els["pcap"]["t"][k] = capt
        for r, rows in ROUTES.items():
            for i in range(len(rows)):
                els[f"h{r}{i}"]["o"][k] = 1 if hit == f"{r}{i}" else 0
        moved = prev is not None and prev[0] != pos
        waits[k] = 1800 if moved else 1500
        prev = seq[k]
    return scene(name, n, els, waits)

def path_slide(label, title, text, name, seq, rev=False):
    sc = path_scene(name, seq, rev)
    slide(label, "Передача данных", title, f"""
<div class="pathwrap" {sc}>
  <div class="card dgcard pathsvg">{PATH_SVG}</div>
  <div class="pbar">
    <div class="vstack">
      <div class="card pcap"><p data-id="pcap"></p></div>
      <div class="card pkp">
        <div class="pkg"><span class="pkh">IP-пакет</span><div class="kv"><span>SrcIP</span><b class="mono" data-id="sip"></b></div><div class="kv"><span>DstIP</span><b class="mono" data-id="dip"></b></div><div class="kv"><span>TTL</span><b class="mono cM" data-id="ttl"></b></div></div>
        <div class="pkg"><span class="pkh">Кадр Ethernet</span><div class="kv"><span>Src MAC</span><b class="mono cP" data-id="smac"></b></div><div class="kv"><span>Dst MAC</span><b class="mono cP" data-id="dmac"></b></div></div>
      </div>
    </div>
    <div class="card ptext">{text}</div>
  </div>
</div>""", "tight")

PANELS = [
    ("PC-A", "Логика оконечного устройства: я не знаю, как доставить пакет в другую сеть, поэтому я поручаю это сделать шлюзу по умолчанию."),
    ("R1", "Маршрут S 192.168.3.0/24 via 10.10.0.2. Интерфейс E2 в той же сети, что и сосед: MAC отправителя AA-BB-BB-BB-BB-BB, MAC получателя – через ARP."),
    ("R2", "Сеть назначения известна через соседа 10.10.1.2, интерфейс T2 в той же сети. TTL 254 до 253, контрольная сумма пересчитывается."),
    ("R3", "Сеть назначения подключена за интерфейсом G2. MAC PC-B – из таблицы ARP или ARP-запросом."),
    ("PC-B", "Адреса внутри пакета не меняются в процессе передачи. Меняются MAC-адреса кадра и значение TTL."),
]

# ---------------------------------------------------------------- 8. ARP
ar = '<line class="lnk" x1="120" y1="250" x2="860" y2="250"/>'
ar += pcsym(120, 250, "PC-A") + rt(480, 250, 128, "R1") + rt(860, 250, 128, "R2")
ar += '<text class="adr" x="120" y="338" text-anchor="middle">192.168.1.2</text><text class="adr" x="290" y="320" text-anchor="middle">E1 192.168.1.1</text>'
ar += '<text class="adr dim" x="290" y="340" text-anchor="middle">AA-AA-AA-AA-AA-AA</text>'
ar += ('<g class="an" data-id="bd"><rect class="dom" x="20" y="96" width="545" height="284" rx="18"/>'
       '<text class="domt" x="40" y="122">широковещательный домен 192.168.1.0/24</text></g>')
ar += ('<g class="an" data-id="ab"><rect class="bub" x="150" y="12" width="640" height="60" rx="16"/>'
       '<text class="bubt" x="172" y="50">192.168.3.2 не в моей сети – отправляю шлюзу 192.168.1.1</text></g>')
ar += pkt("aq", "ARP-запрос: кто 192.168.1.1?", "pk-s", 310, 40, 'style="--md:1300ms"', None)
ar += pkt("aq2", "ARP-запрос", "pk-s", 150, 40, 'style="--md:700ms"', None)
ar += '<g class="an" data-id="ax"><path class="xm" d="M660 150l40 34M700 150l-40 34"/><text class="lost" x="680" y="210" text-anchor="middle">не проходит</text></g>'
ar += pkt("ar", "ARP-ответ: AA-AA-AA-AA-AA-AA", "pk-m", 330, 40, 'style="--md:1300ms"', None)
ar += ('<g class="an" data-id="af"><rect class="bx glass" x="140" y="390" width="720" height="60" rx="14"/>'
       '<text class="frm" x="160" y="427">Кадр: Src MAC <tspan class="cM">AA-BB-CC-11-22-33</tspan>   Dst MAC <tspan class="cM">AA-AA-AA-AA-AA-AA</tspan></text></g>')
ARP = svg("0 0 1000 470", ar)
ARP_SC = scene("arp", 6, {
    "ab": {"o": {0: 0, 1: 1}},
    "aq": {"p": {0: (200, 168), 2: (300, 168)}, "o": {0: 0, 2: 1, 4: 0}},
    "bd": {"o": {0: 0, 3: 1}},
    "aq2": {"p": {0: (560, 168), 3: (680, 168)}, "o": {0: 0, 3: 1, 4: 0}},
    "ax": {"o": {0: 0, 3: 1}},
    "ar": {"p": {0: (440, 168), 5: (290, 168)}, "o": {0: 0, 5: 1, 6: 0}},
    "af": {"o": {0: 0, 6: 1}, "p": {0: (0, 12), 6: (0, 0)}},
}, {1: 900, 2: 1500, 3: 1300, 4: 500, 5: 1500, 6: 900})

# ---------------------------------------------------------------- markup helpers
def steps(items, start=1, cls=""):
    return f'<ol class="steps {cls}">' + "".join(
        f'<li data-s="{start+i}"><span class="badge">{i+1}</span><div>{t}</div></li>' for i, t in enumerate(items)) + '</ol>'

def fcards(items, start=1, cols="g2"):
    return f'<div class="{cols}">' + "".join(
        f'<article class="card fc {c}" data-s="{start+i}"><div class="ftag mono">{n}</div><p>{t}</p></article>'
        for i, (n, c, t) in enumerate(items)) + '</div>'

def scbox(svgcode, sc, cls=""):
    return f'<div class="card dgcard {cls}" {sc}>{svgcode}</div>'

def kvtable(rows, head=("Поле", "Значение в дампе", "Что оно означает")):
    r = "".join(f'<tr data-s="{i+1}"><th>{a}</th><td class="mono">{b}</td><td>{c}</td></tr>' for i, (a, b, c) in enumerate(rows))
    return f'<div class="tw card"><table class="tbl"><thead><tr><th>{head[0]}</th><th>{head[1]}</th><th>{head[2]}</th></tr></thead><tbody>{r}</tbody></table></div>'

HDR4 = [
    [("Version", 4, "sky", "Четырехбитное поле обозначает версию протокола IP: 4 (0100) для IPv4 и 6 (0110) для IPv6."),
     ("IHL", 4, "lilac", "Длина заголовка в «словах» по 32 бита. Минимальное значение – 5, максимальное – 15."),
     ("DSCP", 6, "sky", "6 бит, приоритет пакета. Используется сервисами Quality of Service (QoS)."),
     ("ECN", 2, "sky", "2 бита, уведомление о заторе: возможность отбрасывания пакета при заторе."),
     ("Total Length", 16, "lilac", "Общая длина пакета (заголовок + сегмент) в байтах. Не более 65535, минимум – 20 байт.")],
    [("Identification", 16, "lilac", "Уникальный идентификатор пакета. При фрагментации копируется во все фрагменты."),
     ("Flags", 3, "sky", "Три однобитных поля: 0 – резерв, DF – «не фрагментировать», MF – «больше фрагментов»."),
     ("Fragment Offset", 13, "lilac", "13 бит: какая часть оригинального пакета содержится во фрагменте. Для первого фрагмента – 0.")],
    [("TTL", 8, "mint", "Время жизни пакета, 8 бит: максимальное количество прыжков до отбрасывания."),
     ("Protocol", 8, "sky", "Номер инкапсулированного протокола: ICMP – 0х01, IGMP – 0х02, OSPF – 0х59."),
     ("Header Checksum", 16, "sky", "Вычисляется по всем полям заголовка. Пересчитывается маршрутизатором после изменения TTL.")],
    [("Source IP Address", 32, "pink", "Адрес устройства-отправителя. Всегда одноадресной рассылки (unicast).")],
    [("Destination IP Address", 32, "pink", "Адрес устройства-получателя: одноадресная, многоадресная или широковещательная рассылка.")],
    [("Options", 32, "dim", "Необязательные параметры. Их наличие учитывается в поле IHL (если оно больше 5).")],
]

def hdr_grid(rows):
    s = '<div class="hdr">'
    for r, row in enumerate(rows):
        s += f'<div class="hrow" data-s="{r+1}">'
        for lab, bits, c, tip in row:
            s += (f'<div class="fld {c}" tabindex="0" style="grid-column:span {bits}"><b>{lab}</b>'
                  f'<span class="mono">{bits} бит</span><span class="tip">{tip}</span></div>')
        s += '</div>'
    return s + '</div>'

V4 = [("Version", "k"), ("IHL", "x"), ("DSCP / ECN", "k"), ("Total Length", "k"), ("Identification", "x"), ("Flags (DF, MF)", "g"),
      ("Fragment Offset", "g"), ("TTL", "k"), ("Protocol", "k"), ("Header Checksum", "g"), ("Source IP Address", "k"),
      ("Destination IP Address", "k"), ("Options", "x")]
V6 = [("Version", "sky"), ("Traffic Class", "sky"), ("Flow Label", "lilac"), ("Payload Length", "lilac"), ("Next Header", "sky"),
      ("Hop Limit", "mint"), ("Source Address", "pink"), ("Destination Address", "pink")]

ATTR46 = {"g": ' data-p="1" data-k="2"', "x": ' data-k="2"', "k": ""}

def cmp46():
    a = "".join(
        '<div class="chipf ' + ("gone" if t != "k" else "") + '"' + ATTR46[t] + '>' + n + '</div>'
        for n, t in V4)
    b = "".join(f'<div class="chipf {c}" data-s="3" style="--dl:{i*70}ms">{n}</div>' for i, (n, c) in enumerate(V6))
    return (f'<div class="g2 cmp46"><div class="card col46"><h3>IPv4</h3>{a}</div>'
            f'<div class="card col46"><h3>IPv6</h3>{b}</div></div>')

QUIZ = [
    {"q": "Дамп IPv6 (справа): откуда и куда передаётся пакет?", "o": ["2603:1026:c0d:101f::2 в 2a01:620:c12a:a500:953:6c6e:487:5201", "2a01:620:c12a:a500:953:6c6e:487:5201 в 2603:1026:c0d:101f::2", "с порта 56867 на порт 443", "Адреса в дампе не указаны"], "a": 0,
     "e": "Source Address – 2603:1026:c0d:101f::2, Destination Address – 2a01:620:c12a:a500:953:6c6e:487:5201."},
    {"q": "Дамп IPv6: каков размер полезной нагрузки?", "o": ["116 октетов", "20 октетов", "6 октетов", "16383 октета"], "a": 1,
     "e": "Payload Length: 20 – длина полезной нагрузки в октетах. 116 – это Hop Limit."},
    {"q": "Дамп IPv6: пакет перехвачен на маршрутизаторе-отправителе?", "o": ["Да, Hop Limit ещё не уменьшался", "Нет: Hop Limit = 116, значит пакет уже прошёл маршрутизаторы", "Нельзя сказать: в IPv6 нет лимита переходов", "Да, так как Next Header = TCP"], "a": 1,
     "e": "Каждый маршрутизатор уменьшает Hop Limit на 1 (максимум 255). Значение 116 показывает, что пакет уже совершил переходы."},
    {"q": "Дамп IPv6: к какому протоколу относится полезная нагрузка?", "o": ["UDP", "ICMPv6", "TCP", "Routing Header"], "a": 2,
     "e": "Next Header: TCP (6) – указан номер протокола уровня L4, значит заголовок IPv6 единственный."},
    {"q": "ping показывает TTL=104, начальное значение 128. Сколько прыжков совершил пакет?", "o": ["104", "24", "128", "232"], "a": 1,
     "e": "128 – 104 = 24 «прыжка». Начальное значение можно узнать командой ping 127.0.0.1."},
    {"q": "Маршрутизатор принимает транзитный пакет с TTL=1. Что произойдёт?", "o": ["Перешлёт с TTL=0", "Отбросит, не обрабатывая", "Обработает, отбросит и отправит отправителю Time Exceeded", "Вернёт пакет с TTL=128"], "a": 2,
     "e": "Маршрутизатор сначала обработает пакет и лишь затем отбросит, уведомив отправителя сообщением Time Exceeded."},
    {"q": "Каких полей IPv4 нет в основном заголовке IPv6?", "o": ["Source и Destination", "Header Checksum и Fragment Offset", "Version и Hop Limit", "Traffic Class и Flow Label"], "a": 1,
     "e": "Контроль целостности выполняет L4 (TCP), а для фрагментации предусмотрен дополнительный заголовок."},
    {"q": "Что меняется в пакете PC-A – PC-B при прохождении R1, R2, R3?", "o": ["IP-адрес назначения", "IP-адрес источника", "TTL; а MAC-адреса меняются в кадре на каждом участке", "Ничего не меняется"], "a": 2,
     "e": "Адреса внутри пакета не меняются. TTL уменьшается 255, 254, 253, 252, MAC-адреса кадра задаются заново на каждом участке."},
]

def qa(items):
    return '<div class="qas">' + "".join(
        f'<article class="card qa" data-s="{i+1}"><div class="qq"><span class="badge">{i+1}</span><b>{q}</b></div>'
        f'<button class="btn qa-b" type="button">Показать ответ</button><p class="qa-a" hidden>{a}</p></article>'
        for i, (q, a) in enumerate(items)) + '</div>'

DUMP4 = ('<div class="card term mono dump"><div class="dimt">Internet Protocol Version 4</div><div>Version: 4</div><div>Header Length: 20 bytes (5)</div>'
         '<div>DSCP: CS0, ECN: Not-ECT</div><div>Total Length: 1480</div><div>Identification: 0xd06a (53354)</div><div>Flags: 0x40, Don’t fragment</div>'
         '<div>Fragment Offset: 0</div><div>Time to Live: 64</div><div>Protocol: TCP (6)</div><div>Header Checksum: 0xc0c0</div>'
         '<div>Source Address: 10.25.200.60</div><div>Destination Address: 3.164.206.11</div></div>')
DUMP6 = ('<div class="card term mono dump"><div class="dimt">Internet Protocol Version 6</div>'
         '<div>Version: 6</div><div>Traffic Class: 0x00</div><div>Flow Label: 0xf476c</div><div>Payload Length: 20</div>'
         '<div>Next Header: TCP (6)</div><div>Hop Limit: 116</div><div>Source Address: 2603:1026:c0d:101f::2</div>'
         '<div>Destination Address: 2a01:620:c12a:a500:953:6c6e:487:5201</div></div>')

# ---------------------------------------------------------------- slides
S = []
def slide(label, kick, title, body, cls=""):
    S.append((label, kick, title, body, cls))

slide("Титул", "", "", """
<div class="title">
  <div class="kick big">Глава 9</div>
  <h1>Сетевой уровень</h1>
  <p class="lead">Протоколы IPv4 и IPv6, поля заголовков и передача данных между различными подсетями</p>
  <div class="tchips"><span class="chip mono">IPv4</span><span class="chip mono">IPv6</span><span class="chip mono">TTL</span><span class="chip mono">show ip route</span></div>
  <p class="authors">Ананко Софья Михайловна<br>Качур Анна Юрьевна</p>
</div>""", "tslide")

slide("Цели главы", "Введение", "Цели данной главы", steps([
    "Функции сетевого уровня;", "Поля заголовков пакета протоколов IPv4 и IPv6 и их назначение;",
    "Пример передачи данных между различными подсетями."], cls="big"))

slide("Функции уровня", "Функции", "Функции сетевого уровня", """
<p class="p wide">Основные функции сетевого уровня при передаче данных:</p>""" + fcards([
    ("Адресация", "c-pink", "Адресация оконечных устройств – назначение уникальных IP-адресов оконечным устройствам (узлам). Для того чтобы в сети устройства могли обмениваться данными между собой, их необходимо идентифицировать. Это реализуется при помощи IP-адресов."),
    ("Маршрутизация", "c-mint", "Маршрутизация – обработка пакета маршрутизатором. Маршрутизатор выбирает путь, по которому необходимо отправить пакет, и направляет пакет по этому пути. Пакет может совершить один или несколько переходов, прежде чем достигнет узла назначения."),
    ("Инкапсуляция", "c-sky", "Инкапсуляция/декапсуляция – добавление/удаление собственного заголовка L3 к блоку данных протокола транспортного уровня."),
], cols="g3"))

slide("Инкапсуляция", "Функции", "Инкапсуляция и декапсуляция", """
<div class="two">
  <div>
    <p class="p">После того, как на сетевой уровень приходит сегмент от транспортного уровня, происходит <b>инкапсуляция</b>, т.е. к данным добавляется заголовок IP, который содержит информацию о функционале протокола, а также IP-адреса источника и назначения.</p>
    <p class="p">Если же на сетевой уровень приходит пакет с канального уровня, происходит <b>декапсуляция</b>: удаление заголовка пакета для последующей передачи сегмента соответствующему протоколу транспортного уровня.</p>
  </div>""" + scbox(ENCAP, ENC_SC) + "</div>")

slide("Протокол IP", "Протоколы", "Протоколы сетевого уровня и их свойства", """
<p class="p wide"><b>Internet Protocol (IP)</b> – основной протокол стека протоколов TCP/IP и основной протокол сетевого уровня. Версии IP-протокола, используемые в настоящее время: <b>IPv4</b> и <b>IPv6</b>.</p>
<div class="tw card"><table class="tbl ipt"><thead><tr><th>Характеристики IP-адресации</th><th>IPv4</th><th>IPv6</th></tr></thead><tbody>
<tr data-s="1"><th>Размер адреса</th><td>32 бита (4 байта)</td><td>128 бит (16 байт)</td></tr>
<tr data-s="2"><th>Количество поддерживаемых адресов</th><td>4 миллиарда</td><td>340 · 10<sup>36</sup></td></tr>
<tr data-s="3"><th>Форма записи</th><td>десятичные числа, разделенные точками</td><td>шестнадцатеричные числа, разделенные двоеточиями</td></tr>
<tr data-s="4"><th>Пример</th><td class="mono c4">192.168.10.15</td><td class="mono c4">0000:0000:0000:0000:0000:ffff:c0a8:0a0f</td></tr>
</tbody></table></div>""")

slide("Без соединения", "Свойства IP", "Пересылка без установления соединения", """
<div class="two">
  <div>
    <p class="p">Протокол IP является протоколом без установления соединения: каждый IP-пакет обрабатывается независимо от других пакетов. Перед отправкой пакетов не требуется обмен контрольной информацией, а заголовок IP не содержит полей, поддерживающих процесс установки соединения.</p>
    <p class="p callout">Однако отсутствие предварительного соединения означает, что невозможно определить, способен ли получатель принять пакет и обработать его.</p>
  </div>""" + scbox(CONN, CONN_SC) + "</div>")

slide("Негарантированная доставка", "Свойства IP", "Негарантированная доставка", """
<div class="two">
  <div>
    <p class="p">В протоколе IP отсутствуют механизмы, которые обеспечивают гарантированную доставку и достоверность конечных данных. Если в процессе передачи пакета происходит ошибка, протокол не предпримет никаких действий для ее исправления или повторной отправки этого пакета.</p>
    <p class="p">Пакеты могут дойти до узла назначения в неправильном порядке или не дойти вовсе: в заголовке IP не содержится информация о том, что необходимо сделать в таких ситуациях.</p>
  </div>""" + scbox(UNREL, UNREL_SC) + "</div>")

MEDIA_ICONS = {
    "cu": '<svg viewBox="0 0 120 60" class="ico"><path class="sig" d="M5 45H25V15H45V45H65V15H85V45H115"/></svg>',
    "fo": '<svg viewBox="0 0 120 60" class="ico"><path class="sig" d="M5 30H115"/><circle class="dot" cx="35" cy="30" r="7"/><circle class="dot" cx="70" cy="30" r="7"/><circle class="dot" cx="100" cy="30" r="4"/></svg>',
    "rf": '<svg viewBox="0 0 120 60" class="ico"><path class="sig" d="M5 30C15 5 25 5 35 30S55 55 65 30 85 5 95 30 115 55 115 30"/></svg>',
}
slide("Независимость от среды", "Свойства IP", "Независимость от среды", """
<p class="p wide">Протокол IP обеспечивает возможность передачи пакетов через различные среды передачи данных, включая проводные и беспроводные сети.</p>
<div class="g3">
  <article class="card media" data-s="1">""" + MEDIA_ICONS["cu"] + """<h3>Проводные сети</h3><p>Данные передаются в виде электрических импульсов.</p></article>
  <article class="card media" data-s="2">""" + MEDIA_ICONS["fo"] + """<h3>Оптоволоконные кабели</h3><p>Данные передаются в виде оптических сигналов.</p></article>
  <article class="card media" data-s="3">""" + MEDIA_ICONS["rf"] + """<h3>Беспроводные сети</h3><p>Данные передаются в виде радиосигналов.</p></article>
</div>""")

slide("MTU и фрагментация", "Свойства IP", "MTU и фрагментация", """
<div class="two">
  <div>
    <p class="p sm">Важной характеристикой протокола IP является его возможность фрагментировать пакеты во время передачи между сетями, имеющими разные максимально допустимые размеры передаваемых блоков данных (<b>MTU – Maximum Transmission Unit</b>).</p>
    <p class="p sm">MTU представляет собой максимальный размер пакета, который может быть передан по сети определенной среды передачи без необходимости деления его на более мелкие фрагменты.</p>
    <p class="p sm">При пересылке пакета из одной среды передачи в другую с меньшим MTU промежуточное устройство (к примеру, маршрутизатор) фрагментирует пакет на более мелкие части (фрагменты) перед отправкой их в назначенную сеть.</p>
  </div>""" + scbox(MTU, MTU_SC) + "</div>")

slide("Заголовок IPv4", "Протокол IPv4", "Заголовок протокола IPv4", """
<p class="p wide">Заголовок пакета протокола IPv4 представляет собой последовательность двоичных цифр длиной от <b class="mono">160</b> до <b class="mono">480</b> бит. Наведите курсор на поле, чтобы увидеть его назначение.</p>
<div class="card hdrcard"><div class="ruler mono"><span>0</span><span>8</span><span>16</span><span>24</span><span>31</span></div>""" + hdr_grid(HDR4) + "</div>")

slide("Поля IPv4: 1", "Протокол IPv4", "Version, IHL, DS, Total Length", fcards([
    ("Version", "c-sky", "Четырехбитное поле обозначает версию протокола IP, к которой принадлежит данный пакет. В настоящее время используются два значения: 4 (0100) для версии IPv4 и 6 (0110) для версии IPv6. Судя по емкости поля, его хватит до версии IPv15."),
    ("IHL", "c-lilac", "Длина заголовка. Разграничивает заголовок и сегмент. Единица измерения – «слово», то есть 32 бита или 4 байта. Минимальное значение – 5, максимальное – 15. Если IHL больше 5, в заголовке используются опции."),
    ("DSCP / ECN", "c-sky", "Differentiated Services: DSCP – 6 бит, приоритет пакета для сервисов QoS; ECN – 2 бита, уведомление о заторе, возможность отбрасывания пакета при слишком «длинной» очереди на передающем интерфейсе."),
    ("Total Length", "c-lilac", "Общая длина пакета (заголовок + инкапсулированный сегмент) в байтах. Размер поля – 16 бит, длина пакета не может превышать 65535 байт. Минимальный размер – 20 байт. Фрагментация – крайне нежелательный процесс: она может сильно замедлить пересылку и обратную сборку пакета."),
]))

slide("Поля IPv4: 2", "Протокол IPv4", "Identification, Flags, Fragment Offset", fcards([
    ("Identification", "c-lilac", "16-битное поле – уникальный идентификатор пакета. При фрагментации значение поля не меняется и копируется во все фрагменты, так устройство-получатель определяет «принадлежность» фрагментов к одному пакету."),
    ("0", "c-dim", "Первый флаг всегда устанавливается равным нулю, так как это поле зарезервировано для возможного использования в будущем."),
    ("DF", "c-pink", "Don’t Fragment, «не фрагментировать». Если флаг равен 1, пересылающее устройство не выполняет фрагментацию; если без фрагментации пакет обработать невозможно, устройство его отбрасывает. Используется для подбора максимального размера пакета на маршруте."),
    ("MF и Fragment Offset", "c-sky", "More Fragments: 1 – за пакетом последуют еще фрагменты, у последнего фрагмента 0, без фрагментации 0. Fragment Offset – 13 бит, какая часть оригинального пакета в этом фрагменте; для первого фрагмента равно 0."),
]))

slide("Поля IPv4: 3", "Протокол IPv4", "TTL, Protocol, Header Checksum", fcards([
    ("TTL", "c-mint", "Time to Live – время жизни пакета. Подробно разбирается в следующем разделе."),
    ("Protocol", "c-sky", "Номер протокола, для которого на стороне получателя предназначена «полезная нагрузка» пакета. Обычно указывается в шестнадцатеричном формате (0х00). Списки номеров назначает IANA (RFC 790): ICMP – 0х01 (1), IGMP – 0х02 (2), OSPF – 0х59 (89)."),
    ("Header Checksum", "c-sky", "Значение, вычисляемое маршрутизатором исходя из значений всех полей заголовка. Если вычисленное значение отличается, пакет отбрасывается. Поскольку TTL меняется маршрутизатором, перед отправкой контрольная сумма пересчитывается."),
], cols="g3"))

slide("Поля IPv4: 4", "Протокол IPv4", "Адреса и опции", fcards([
    ("Source IP Address", "c-pink", "Адрес устройства-отправителя. Всегда относится к адресам одноадресной рассылки (unicast). Адрес многоадресной или широковещательной рассылки в качестве источника вызывает подозрение на атаку IP-spoofing – такой пакет должен быть отфильтрован."),
    ("Destination IP Address", "c-pink", "Адрес устройства-получателя. Может принадлежать ко всем видам рассылок: одноадресной, многоадресной и широковещательной."),
    ("Options", "c-dim", "Дополнительная информация, необходимая при пересылке пакета. Количество опций учитывается в поле IHL (если оно больше 5, в заголовке есть опции). Поле не является обязательным."),
], cols="g3"))

slide("IPv4 в Wireshark", "Протокол IPv4", "Заголовок IPv4 в Wireshark: разбор полей", kvtable([
    ("Version", "4 (0100)", "Пакет принадлежит версии IPv4"),
    ("Header Length", "20 bytes (5)", "IHL = 5: опций нет, заголовок оканчивается после адреса назначения"),
    ("DSCP / ECN", "CS0 (0) / Not-ECT (0)", "Приоритет по умолчанию, уведомление о заторе не используется"),
    ("Total Length", "1480", "Длина пакета (заголовок + сегмент) в байтах"),
    ("Identification", "0xd06a (53354)", "Уникальный идентификатор пакета"),
    ("Flags", "0x40: DF = 1, MF = 0", "Фрагментация запрещена, фрагментов за пакетом нет"),
    ("Fragment Offset", "0", "Пакет не фрагментирован"),
    ("Time to Live", "64", "Оставшееся время жизни пакета"),
    ("Protocol", "TCP (6)", "Полезная нагрузка предназначена протоколу TCP"),
    ("Header Checksum", "0xc0c0", "Контрольная сумма заголовка"),
    ("Source / Destination", "10.25.200.60 / 3.164.206.11", "IP-адреса отправителя и получателя"),
]))

slide("Вопросы: IPv4", "Протокол IPv4", "Заголовок IPv4 в Wireshark: вопросы", '<div class="two quizrow">' + qa([
    ("Откуда и куда передается данный пакет?", "С адреса 10.25.200.60 на адрес 3.164.206.11 (Source Address и Destination Address)."),
    ("Какова длина заголовка? Есть ли в нем опции?", "20 байт: IHL = 5, значит опций нет – заголовок оканчивается после адреса назначения."),
    ("Разрешена ли фрагментация этого пакета?", "Нет: Flags 0x40 – флаг Don’t Fragment (DF) равен 1."),
    ("Каков размер инкапсулированного сегмента?", "Total Length минус длина заголовка: 1480 – 20 = 1460 байт."),
    ("К какому протоколу относится полезная нагрузка?", "TCP: поле Protocol равно 6."),
]) + DUMP4 + '</div>')

slide("TTL", "Поле TTL", "Поле TTL (Time To Live)", """
<div class="two">
  <div>
    <p class="p sm"><b>Время жизни (TTL)</b> – поле в заголовке IP-пакета длиной 8 бит, которое определяет максимальное количество прыжков (hop-лимит), которые пакет может совершить по сети перед тем, как будет отброшен. Каждый маршрутизатор или другое устройство уровня L3 и выше уменьшают значение TTL на 1. Поле TTL позволяет избежать образования «петель маршрутизации».</p>
    <p class="p sm">Коммутатор не снижает значение TTL, так как работает на канальном уровне, а не на сетевом.</p>
    <div class="card term mono"><div>$ ping 8.8.8.8</div><div>64 bytes from 8.8.8.8: icmp_seq=1 <b class="cM">ttl=104</b></div></div>
    <p class="p sm">TTL=104 означает, что пакет совершил <b class="mono">128 – 104 = 24</b> «прыжка». Исходное значение можно узнать командой <span class="mono">ping 127.0.0.1</span>.</p>
  </div>""" + scbox(TTLSVG, TTL_SC).replace('data-scene="ttl"', 'data-scene="ttl"') + "</div>")

slide("Time Exceeded", "Поле TTL", "Когда время жизни заканчивается", """
<div class="two">
  <div>
    <p class="p sm">В процессе перехода пакета по сети его время жизни может закончиться раньше, чем он дойдет до точки назначения. Тогда маршрутизатор, который принимает пакет с <b class="mono">TTL=1</b>, сначала обработает его и лишь затем отбросит. При этом маршрутизатор уведомит отправителя сообщением о превышении времени жизни пакета (<b>Time Exceeded</b>).</p>
    <p class="p sm">В команде <span class="mono">ping -t 8</span> указывается начальное значение TTL – так моделируется ситуация, когда время жизни пакета заканчивается.</p>
    <p class="p sm callout">Если пакет с TTL=1 предназначается самому маршрутизатору, он будет принят и обработан устройством.</p>
  </div>""" + scbox(TESVG, TE_SC) + "</div>")

slide("Заголовок IPv6", "Протокол IPv6", "Заголовок пакета IPv6", """
<div class="two">
  <div>
    <p class="p sm">Главной особенностью заголовка IPv6 является <b>сокращение числа полей</b>: такой пакет легче обрабатывать маршрутизаторам, пересылка проходит быстрее.</p>
    <p class="p sm" data-s="1">Отсутствуют поля контроля пересылки – <b>Header Checksum</b> и <b>Fragment Offset</b>. Контроль целостности данных осуществляется средствами L4 (TCP), и дублировать его на L3 означает сознательно замедлять обработку пакетов.</p>
    <p class="p sm" data-s="2">Поля Fragment Offset и «флагов» DF и MF нет, потому что для них предусмотрен дополнительный заголовок.</p>
  </div>""" + cmp46() + "</div>")

slide("Поля IPv6: 1", "Протокол IPv6", "Version, Traffic Class, Flow Label", fcards([
    ("Version", "c-sky", "Версия. 4-битное поле, в котором указывается версия протокола."),
    ("Traffic Class", "c-sky", "Класс трафика. Определяет приоритет трафика, так же как и в IPv4."),
    ("Flow Label", "c-lilac", "Метка потока. Как и в IPv4, это идентификатор сессии TCP либо потока сегментов UDP, представляющих один медиа-поток. Благодаря этой метке устройство-получатель быстро определяет, какому из протоколов уровня L4 предназначается данный пакет, а протокол L4 быстро «собирает» пакеты в нужные потоки или сессии."),
], cols="g3"))

slide("Поля IPv6: 2", "Протокол IPv6", "Payload Length, Next Header, Hop Limit", fcards([
    ("Payload Length", "c-lilac", "Длина (размер) полезной нагрузки в октетах."),
    ("Next Header", "c-sky", "В отличие от пакета IPv4, пакет IPv6 может содержать несколько заголовков: один основной и несколько заголовков-расширений. Если в поле указывается номер протокола уровня L4 (аналогично полю Protocol IPv4), то данный заголовок является единственным. Если указывается номер заголовка-расширения, присутствуют дополнительные заголовки."),
    ("Hop Limit", "c-mint", "Лимит переходов. Поле из 8 бит с максимальным значением 255. Каждый следующий маршрутизатор уменьшает его значение на 1, а получивший пакет с HL = 0 промежуточный маршрутизатор информирует отправителя о достижении лимита переходов и отбрасывает пакет. Маршрутизатор назначения, получивший пакет с HL = 0, обрабатывает его как любой действительный пакет."),
], cols="g3"))

slide("Заголовки расширения", "Протокол IPv6", "Заголовки расширения", """
<p class="p wide">Дополнительные заголовки (<b>extension headers</b>) – отличительная особенность IPv6. Если достаточно полей основного заголовка, используются только они. Если необходимо учесть фрагментацию или внести дополнительные параметры маршрутизации, используются дополнительные заголовки, на наличие которых указывает поле <b>Next Header</b>.</p>""" + scbox(EXT, EXT_SC, "wide2"))

slide("IPv6 в Wireshark", "Протокол IPv6", "Заголовок IPv6 в Wireshark: разбор полей", kvtable([
    ("Version", "6 (0110)", "Пакет принадлежит версии IPv6"),
    ("Traffic Class", "0x00 (CS0, Not-ECT)", "Приоритет трафика по умолчанию"),
    ("Flow Label", "0xf476c", "Метка потока – идентификатор сессии TCP"),
    ("Payload Length", "20", "Длина полезной нагрузки в октетах"),
    ("Next Header", "TCP (6)", "Номер протокола L4 – заголовок-расширений нет"),
    ("Hop Limit", "116", "Пакет уже прошёл маршрутизаторы: каждый уменьшает значение на 1"),
    ("Source Address", "2603:1026:c0d:101f::2", "Адрес отправителя"),
    ("Destination Address", "2a01:620:c12a:a500:953:6c6e:487:5201", "Адрес получателя"),
]))

slide("Вопросы: IPv6", "Протокол IPv6", "Заголовок IPv6 в Wireshark: вопросы", '<div class="two quizrow">' + qa([
    ("Откуда и куда передается данный пакет?", "С адреса 2603:1026:c0d:101f::2 на адрес 2a01:620:c12a:a500:953:6c6e:487:5201."),
    ("Каков размер полезной нагрузки?", "20 октетов (Payload Length: 20)."),
    ("Данный пакет перехвачен на маршрутизаторе-отправителе, получателе или на промежуточном маршрутизаторе?", "Не на отправителе: Hop Limit = 116 – значение уже уменьшалось маршрутизаторами на пути (максимум 255)."),
    ("К какому протоколу относится данный пакет?", "К TCP: Next Header: TCP (6) – указан протокол L4, заголовков-расширений нет."),
]) + DUMP6 + '</div>')

slide("Передача между сетями", "Передача данных", "Сетевой уровень в процессе передачи данных", """
<p class="p wide">Именно на сетевом уровне осуществляется адресация, которая обеспечивает передачу пакета между различными сетями. Пакет нужно передать из сети <b class="mono">192.168.1.0/24</b> в сеть <b class="mono">192.168.3.0/24</b>. Маршрутизатор, в отличие от коммутатора, не пересылает широковещательные кадры на все порты: широковещательные домены разделены.</p>
<div class="card dgcard wide2">""" + TOPO_BUILD + "</div>")

slide("Шлюз по умолчанию", "Передача данных", "Шлюз по умолчанию", """
<div class="two">
  <div>
    <p class="p">Теперь вспомним, как компьютер принимает решение об отправке ARP-запроса, если IP-адрес назначения не принадлежит его собственной сети.</p>
    <p class="p callout">Логика у оконечного устройства следующая: <b>я не знаю, как доставить пакет в другую сеть, поэтому я поручаю это сделать шлюзу по умолчанию.</b></p>
    <p class="p"><b>Шлюз по умолчанию</b> – это сетевое устройство или интерфейс сетевого уровня, через который осуществляется отправка трафика из сети отправителя в другую сеть, в т.ч. сеть Интернет.</p>
  </div>
  <div class="card gw">
    <div class="gwr" data-s="1"><span>Мой адрес PC-A</span><b class="mono">192.168.1.2/24</b><span class="mono cM">сеть 192.168.1.0</span></div>
    <div class="gwr" data-s="2"><span>DstIP</span><b class="mono cP">192.168.3.2</b><span class="mono cP">сеть 192.168.3.0</span></div>
    <div class="gwr big" data-s="3"><b>192.168.3.0 ≠ 192.168.1.0</b><span>сеть назначения чужая</span></div>
    <div class="gwr big ok" data-s="4"><b>Поручаю шлюзу по умолчанию</b><span class="mono">192.168.1.1 (R1, интерфейс E1)</span></div>
    <div class="gwr" data-s="5"><span>MAC шлюза</span><b class="mono">ARP-запрос на 192.168.1.1</b></div>
  </div>
</div>""")

slide("ARP и маршрутизатор", "Передача данных", "ARP-запрос к шлюзу", """
<div class="two">
  <div>
    <p class="p sm">В нашем случае: компьютер PC-A отправит ARP-запрос на IP-адрес шлюза по умолчанию <span class="mono">192.168.1.1</span>, узнав таким образом его MAC-адрес, сформирует кадр и отправит его в среду.</p>
    <p class="p sm">Шлюз по умолчанию (на схеме это маршрутизатор R1) получает кадр, распаковывает из него пакет и смотрит на поле Destination IP Address, определяя, как быть дальше.</p>
    <p class="p sm">Для того чтобы отправить пакет дальше, у маршрутизатора имеется <b>таблица маршрутизации</b>, в которой содержатся все сети, которые «знает» маршрутизатор, а также адреса соседей, через которых можно переслать пакет в нужную сеть.</p>
  </div>""" + scbox(ARP, ARP_SC) + "</div>")

slide("Таблица маршрутизации", "Передача данных", "Маршрут и таблица маршрутизации", """
<div class="two">
  <div>
    <p class="p sm"><b>Маршрут</b> – это сочетание IP-адреса сети и IP-адреса соседа, через которого можно переслать пакет в эту сеть.</p>
    <p class="p sm" data-s="1">В таблицу маршрутизации автоматически вносятся сети, которые установлены на интерфейсах маршрутизатора, они называются <b>подключенными</b> и обозначаются латинской буквой <b>C</b> (от англ. connected).</p>
    <p class="p sm" data-s="2">Маршруты, которые введены администратором вручную, называются <b>статическими</b> и обозначаются латинской буквой <b>S</b> (от англ. static).</p>
    <p class="p sm" data-s="3">Маршрутизатору R1 известны три сети: две из них находятся непосредственно за интерфейсами Е1 (192.168.1.0/24) и Е2 (10.10.0.0/30), а третья – по адресу соседа 10.10.0.2.</p>
  </div>
  <div class="card term mono big"><div class="dimt">R1# show ip route</div>
    <div data-s="1" data-p="1" class="rowp"><b class="cC">C</b> 192.168.1.0/24 E1</div><div data-s="1" data-p="1" class="rowp"><b class="cC">C</b> 10.10.0.0/30 E2</div>
    <div data-s="2" data-p="2" class="rowp"><b class="cS">S</b> 192.168.3.0/24 via 10.10.0.2</div></div>
</div>""")

path_slide("R1 формирует кадр", "R1: кадр до маршрутизатора R2", """
<p class="p sm">Перед R1 возникает вопрос о том, как получить два MAC-адреса, чтобы сформировать кадр. Проделав операцию побитовая «И», R1 определяет, что интерфейс Е2 принадлежит той же сети, что и сосед (10.10.0.1 и 10.10.0.2 принадлежат сети 10.10.0.0/30). Значит, MAC-адрес отправителя – MAC интерфейса E2 <span class="mono">AA-BB-BB-BB-BB-BB</span>.</p>
<p class="p sm">MAC-адрес получателя определяется ARP-запросом: <span class="mono">AA-CC-CC-CC-CC-CC</span>. Адреса внутри пакета не меняются в процессе передачи. Однако поле TTL изменяется: R1 уменьшает значение на единицу, так что оно теперь равно <b class="mono">254</b>, а не 255.</p>""", "p26", FWD[1:4])

path_slide("R2 получает кадр", "R2: получение кадра", """
<p class="p">Маршрутизатор R2, получив кадр на интерфейсе <b>Т1</b>, отбрасывает заголовок уровня 2 (L2), читает заголовок пакета и сверяет адрес в поле Destination IP Address (IP-адрес назначения) с данными в его таблице маршрутизации.</p>""", "p27", FWD[3:5])

path_slide("R2 пересылает", "R2: пересылка к R3", """
<p class="p sm">Сеть назначения известна маршрутизатору через соседа с IP-адресом <span class="mono">10.10.1.2</span>. Один из собственных интерфейсов R2 (<b>T2</b>) находится в той же сети, что и нужный сосед, поэтому маршрутизатор может начать формирование кадра. MAC-адрес соседа берется из таблицы ARP-соответствий или ARP-запросом.</p>
<p class="p sm">Перед отправкой значение TTL уменьшается с 254 до <b class="mono">253</b>, а также пересчитывается контрольная сумма пакета (речь идет о протоколе IPv4).</p>""", "p28", FWD[4:6])

path_slide("R3 получает кадр", "R3: получение кадра", """
<p class="p">Маршрутизатор R3 получает кадр на интерфейсе <b>G1</b>, декапсулирует, смотрит поле DstIP и тут же сравнивает его значение с собственной таблицей маршрутизации, чтобы обнаружить, что нужная сеть известна ему как подключенная за его собственным интерфейсом <b>G2</b>.</p>""", "p29", FWD[5:7])

path_slide("R3 доставляет", "R3: доставка получателю PC-B", """
<p class="p">R3 выясняет MAC-адрес конечного получателя PC-B путем просмотра таблицы ARP-соответствий или отправки ARP-запроса, формирует Ethernet-кадр и отправляет его непосредственно получателю с интерфейса G2, уменьшив TTL в заголовке IP-пакета на единицу – теперь это значение составляет <b class="mono">252</b>.</p>""", "p30", FWD[6:9])

path_slide("Обратный путь", "Ответ PC-B: обратный путь", """
<p class="p">В случае, если компьютер PC-B отправит ответ компьютеру PC-A, весь процесс повторится в обратном порядке: IP-адреса источника и назначения меняются местами, на каждом участке формируется новый кадр, а TTL уменьшается каждым маршрутизатором.</p>""", "p31", REV, True)

path_slide("Путь пакета целиком", "Путь пакета PC-A – PC-B целиком", """
<p class="p">Итог: адреса внутри пакета не меняются в процессе передачи. На каждом участке меняются MAC-адреса кадра, а каждый маршрутизатор уменьшает TTL на 1 и пересчитывает контрольную сумму.</p>""", "pall", FWD)

slide("Тренажёр: TTL", "Тренажёры", "Тренажёр: TTL и прыжки", """
<div class="two">
  <div class="card trn">
    <div class="tq" id="tt-q"></div>
    <div class="trow"><input id="tt-in" class="mono" inputmode="numeric" autocomplete="off" aria-label="Ответ"><button class="btn pri" id="tt-ok" type="button">Проверить</button><button class="btn" id="tt-nx" type="button">Новая задача</button></div>
    <div class="tres" id="tt-r" aria-live="polite"></div>
    <div class="tscore mono" id="tt-sc">0 / 0</div>
  </div>
  <div class="card lst">
    <h3>Правила из лекции</h3>
    <p class="p sm">Каждый маршрутизатор или другое устройство уровня L3 и выше уменьшает TTL на 1. Коммутатор TTL не меняет.</p>
    <p class="p sm">Число прыжков = начальное значение TTL – значение TTL в ответе.</p>
    <p class="p sm">Маршрутизатор, принявший транзитный пакет с TTL=1, обрабатывает его, отбрасывает и отправляет Time Exceeded.</p>
  </div>
</div>""")

slide("Тренажёр: маршрут", "Тренажёры", "Тренажёр: маршрут, MAC и поля", """
<div class="two">
  <div class="card trn">
    <div class="tq" id="tr-q"></div>
    <div class="opts col" id="tr-o"></div>
    <div class="tres" id="tr-r" aria-live="polite"></div>
    <div class="trow"><button class="btn" id="tr-nx" type="button">Новый вопрос</button><span class="tscore mono" id="tr-sc">0 / 0</span></div>
  </div>
  <div class="card trn">
    <div class="tq" id="tf-q"></div>
    <div class="opts" id="tf-o"></div>
    <div class="tres" id="tf-r" aria-live="polite"></div>
    <button class="btn" id="tf-nx" type="button">Другое поле</button>
  </div>
</div>""")

slide("Проверь себя", "Итог", "Проверь себя", """
<div class="two quizrow">
  <div class="card quiz" id="quiz">
    <div class="qtop"><span class="mono" id="qz-n">1 / 8</span><span class="mono" id="qz-sc">верно: 0</span></div>
    <div class="tq" id="qz-q"></div>
    <div class="opts col" id="qz-o"></div>
    <div class="tres" id="qz-e" aria-live="polite"></div>
    <div class="trow"><button class="btn" id="qz-pv" type="button">Предыдущий</button><button class="btn pri" id="qz-nx" type="button">Следующий вопрос</button></div>
  </div>
  <div class="card term mono dump"><div class="dimt">Internet Protocol Version 6</div>
    <div>Version: 6</div><div>Traffic Class: 0x00</div><div>Flow Label: 0xf476c</div><div>Payload Length: 20</div>
    <div>Next Header: TCP (6)</div><div>Hop Limit: 116</div><div>Source Address: 2603:1026:c0d:101f::2</div>
    <div>Destination Address: 2a01:620:c12a:a500:953:6c6e:487:5201</div></div>
</div>""")

# ---------------------------------------------------------------- CSS
CSS = r"""
:root{
  --glass:rgba(255,255,255,.13);--glass2:rgba(255,255,255,.2);--edge:rgba(255,255,255,.30);
  --ink:#fff;--dim:rgba(255,255,255,.76);--mint:#5ddcb0;--sky:#6fb2ff;--pink:#f07ab4;--lilac:#c9a6ff;
  --deep:#3b2fa8;
  --f:"Golos Text","Inter","Manrope","Segoe UI",system-ui,sans-serif;
  --mono:"JetBrains Mono","Cascadia Mono","Consolas","Roboto Mono",ui-monospace,monospace;
  --r:18px;--hl:inset 0 1px 0 rgba(255,255,255,.28);--sh:0 10px 30px rgba(40,20,120,.18);
  --ez:cubic-bezier(.22,.7,.3,1);--sp:1;
  color-scheme:dark;
}
*{box-sizing:border-box;margin:0;padding:0}
html{font-size:clamp(14px,min(1.02vw,1.86vh),28px)}
html,body{height:100%;overflow:hidden;color:var(--ink);font-family:var(--f)}
body{background:linear-gradient(180deg,rgba(28,18,78,.55),rgba(40,24,96,.42) 55%,rgba(28,18,78,.6)),url(__BGIMG__) center/cover no-repeat;background-color:#3f358f;background-attachment:fixed}
.mono{font-family:var(--mono);font-variant-numeric:tabular-nums;letter-spacing:-.01em}
b{font-weight:700}
#prog{position:fixed;left:0;top:0;height:4px;width:100%;z-index:30;background:rgba(255,255,255,.18)}
#prog i{display:block;height:100%;width:0;background:var(--mint);transition:width .3s var(--ez)}
.slide{position:fixed;inset:0;z-index:1;display:none}
.slide.on{display:block}
.sc{height:100%;overflow-y:auto;overflow-x:hidden;display:flex;flex-direction:column;
  padding:clamp(18px,5vh,64px) clamp(16px,5vw,110px) calc(5.4rem + 12px);scrollbar-width:thin;scrollbar-color:rgba(255,255,255,.4) transparent}
.tight .sc{padding-top:clamp(14px,3vh,36px)}
.wrap{margin:auto;width:100%;max-width:100rem}
.sh{margin-bottom:1.4rem}
.tight .sh{margin-bottom:.7rem}
.kick{font-size:.8rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--dim);margin-bottom:.4rem}
h2{font-size:2.4rem;line-height:1.08;font-weight:800;color:var(--ink);letter-spacing:-.01em;max-width:40ch}
.tight h2{font-size:1.9rem}
h3{font-size:1.1rem;font-weight:700;margin-bottom:.6rem;line-height:1.3}
.p{font-size:1.2rem;line-height:1.5;margin-bottom:1rem;max-width:62ch;color:var(--ink)}
.p.sm{font-size:1.04rem;margin-bottom:.75rem}
.p.wide{max-width:none;margin-bottom:1.2rem}
sup{font-size:.65em}
.two{display:grid;grid-template-columns:minmax(0,1fr);gap:1.4rem 2.6rem;align-items:center}
.g2{display:grid;grid-template-columns:minmax(0,1fr);gap:1rem}
.g3{display:grid;grid-template-columns:minmax(0,1fr);gap:1rem}
.vstack{display:flex;flex-direction:column;gap:1rem}
.card{background:var(--glass);border:1px solid var(--edge);border-radius:var(--r);box-shadow:var(--hl),var(--sh);
  -webkit-backdrop-filter:blur(16px) saturate(140%);backdrop-filter:blur(16px) saturate(140%)}
.dgcard{padding:1rem 1.2rem}
.dg{display:block;width:100%;height:auto;max-height:64vh;overflow:visible}
.wide2 .dg{max-height:52vh}
.callout{background:var(--glass2);border-radius:var(--r);padding:.9rem 1.1rem}
.cM{color:var(--mint)}.cP{color:var(--pink)}.cS{color:var(--sky);fill:var(--sky)}.cC{color:var(--mint);fill:var(--mint)}.dimt{color:var(--dim)}
.c-mint{--c:var(--mint)}.c-sky{--c:var(--sky)}.c-pink{--c:var(--pink)}.c-lilac{--c:var(--lilac)}.c-dim{--c:var(--dim)}
/* steps */
.steps{list-style:none;display:flex;flex-direction:column;gap:1rem}
.steps li{display:flex;gap:1rem;align-items:flex-start;font-size:1.2rem;line-height:1.45}
.steps.big li{font-size:1.65rem;align-items:center}
.badge{flex:none;display:grid;place-items:center;width:2.1em;height:2.1em;border-radius:10px;color:var(--deep);font-weight:800;font-family:var(--mono);font-size:.85em;background:#fff}
.fc{padding:1.2rem 1.35rem}.fc p{font-size:1.02rem;line-height:1.5}
.ftag{font-weight:800;font-size:1.35rem;color:var(--c);margin-bottom:.45rem}
/* reveal engine */
[data-s]{opacity:0;transform:translateY(10px);
  transition:opacity calc(280ms / var(--sp)) var(--ez) calc(var(--dl,0ms) / var(--sp)),transform calc(280ms / var(--sp)) var(--ez) calc(var(--dl,0ms) / var(--sp))}
[data-s].in{opacity:1;transform:none}
tr[data-s]{transform:none}
svg [data-s]{transform:none}
.arr[data-s]{opacity:1}
.arr .draw{fill:none;stroke:var(--c);stroke-width:4;stroke-linecap:round;stroke-dasharray:1;stroke-dashoffset:1;transition:stroke-dashoffset calc(700ms / var(--sp)) linear calc(var(--dl,0ms) / var(--sp))}
.arr.in .draw{stroke-dashoffset:0}
.an{transition:transform calc(var(--md,1000ms) / var(--sp)) cubic-bezier(.45,.05,.35,1) calc(var(--dl,0ms) / var(--sp)),opacity calc(280ms / var(--sp)) var(--ez)}
.dr{fill:none;stroke:var(--mint);stroke-width:4;stroke-linecap:round;stroke-dasharray:1;stroke-dashoffset:1;transition:stroke-dashoffset calc(700ms / var(--sp)) linear}
.dr.on{stroke-dashoffset:0}
.ni,.ni *{transition:none!important}
.flash{animation:fl calc(700ms / var(--sp)) var(--ez) 1}
@keyframes fl{0%{background:rgba(93,220,176,.55)}100%{background:transparent}}
.pulse{animation:pl calc(700ms / var(--sp)) var(--ez) 1}
@keyframes pl{0%,100%{background:transparent}40%{background:rgba(111,178,255,.45)}}
.gone{transition:opacity calc(280ms / var(--sp)) var(--ez),max-height calc(500ms / var(--sp)) var(--ez) calc(200ms / var(--sp)),padding calc(500ms / var(--sp)) var(--ez) calc(200ms / var(--sp)),margin calc(500ms / var(--sp)) var(--ez) calc(200ms / var(--sp)),border-width 0s linear calc(700ms / var(--sp))}
.gone.pulse{animation:none;border-color:var(--pink);background:rgba(240,122,180,.3)}
.chipf.kl{opacity:0;max-height:0;padding-top:0;padding-bottom:0;margin-top:-.45rem;border-width:0}
/* svg primitives */
.dg text{font-family:var(--f);font-size:22px;fill:var(--ink)}
.dg .nl{font-size:20px;font-weight:700}
.row{stroke:rgba(255,255,255,.3);stroke-width:2;stroke-dasharray:6 8}
.dg .rowt{fill:var(--dim);font-size:18px}
.bx{stroke:rgba(255,255,255,.55);stroke-width:1.5}
.bx.sky{fill:rgba(111,178,255,.55)}.bx.mint{fill:rgba(93,220,176,.5)}.bx.pink{fill:rgba(240,122,180,.6)}
.bx.fr{fill:rgba(255,196,110,.62)}.bx.glass{fill:rgba(255,255,255,.14)}
.dg .bxt{font-weight:700;font-size:21px}
.dg .cap,.dg .capm{font-size:22px;font-weight:600}
.dg .capm{fill:var(--mint);font-family:var(--mono)}
.bub{fill:rgba(255,255,255,.16);stroke:var(--edge);stroke-width:1.5}
.dg .bubt{font-size:19px}
.lane{stroke:rgba(255,255,255,.28);stroke-width:2;stroke-dasharray:4 8}
.lnk{stroke:rgba(255,255,255,.55);stroke-width:4}
.pk-m{fill:var(--mint);stroke:#fff;stroke-width:1.5}.pk-p{fill:var(--pink);stroke:#fff;stroke-width:1.5}.pk-s{fill:var(--sky);stroke:#fff;stroke-width:1.5}
.dg .pkt{fill:#1d1760;font-weight:800;font-family:var(--mono);font-size:19px}
.dg .pkt.sm{font-size:16px}
.dg .pkt.hit{fill:#1d1760;animation:tf calc(700ms / var(--sp)) var(--ez) 1}
@keyframes tf{0%{opacity:.2}100%{opacity:1}}
.dg .pks2{fill:#1d1760;font-size:15px;font-family:var(--mono)}
.dg .cloudt{fill:#4b4fd8;font-size:34px;font-weight:800}
.dg .flg{fill:var(--ink);font-family:var(--mono);font-size:15px;font-weight:700}
.xm{stroke:var(--pink);stroke-width:6;stroke-linecap:round;fill:none}
.dg .lost{fill:var(--pink);font-weight:700;font-size:19px}
.pipe{fill:rgba(255,255,255,.12);stroke:var(--edge);stroke-width:1.5}
.dg .pipet{fill:var(--dim);font-size:19px}
.dg .nh{font-family:var(--mono);font-size:16px;font-weight:700;fill:#1d1760}
.ifb{fill:rgba(255,255,255,.2);stroke:var(--edge)}
.dg .ift{font-size:15px;font-weight:700;font-family:var(--mono)}
.dg .adr{font-family:var(--mono);font-size:14px;fill:var(--ink)}
.dg .adr.dim{fill:var(--dim)}
.sn{fill:rgba(93,220,176,.3);stroke:var(--mint)}.sn.lan{fill:rgba(240,122,180,.25);stroke:var(--pink)}
.dg .snt{font-family:var(--mono);font-size:15px;font-weight:700}
.rtb{fill:rgba(30,20,110,.35);stroke:var(--edge)}
.dg .rth{font-family:var(--mono);font-size:14px;fill:var(--dim)}
.dg .rtr{font-family:var(--mono);font-size:14px}
.rhit{fill:rgba(93,220,176,.35);stroke:var(--mint)}
.dom{fill:none;stroke:var(--pink);stroke-width:2.5;stroke-dasharray:10 8}
.dg .domt{fill:var(--pink);font-size:17px;font-weight:600}
.dg .frm{font-family:var(--mono);font-size:18px}
.dg .cM{fill:var(--mint)}
.ico{width:100%;height:4.2rem;margin-bottom:.6rem}
.sig{fill:none;stroke:var(--mint);stroke-width:4;stroke-linecap:round;stroke-linejoin:round}.dot{fill:var(--sky)}
.media{padding:1.3rem}.media p{font-size:1.05rem;line-height:1.5;color:var(--dim)}
/* title */
.tslide .sc{padding-left:clamp(16px,10vw,220px)}
.title h1{font-size:clamp(2.4rem,6.5vw,5.6rem);line-height:1;font-weight:800;letter-spacing:-.02em;max-width:14ch;margin:.3rem 0 1.4rem}
.kick.big{font-size:1rem}
.lead{font-size:1.45rem;line-height:1.45;color:var(--dim);max-width:44ch;margin-bottom:2rem}
.tchips{display:flex;flex-wrap:wrap;gap:.7rem;margin-bottom:3rem}
.chip{border:1px solid var(--edge);background:var(--glass);border-radius:var(--r);padding:.5rem .95rem;font-weight:700;font-size:1.1rem;box-shadow:var(--hl)}
.authors{font-size:1.05rem;line-height:1.6}
/* tables */
.tw{overflow-x:auto}
.tbl{width:100%;border-collapse:collapse;font-size:1.02rem}
.tbl th,.tbl td{text-align:left;padding:.55rem 1rem;border-bottom:1px solid rgba(255,255,255,.2);vertical-align:top}
.tbl thead th{background:rgba(255,255,255,.16);font-weight:700}
.tbl tbody th{font-weight:600}
.tbl td.mono{color:var(--mint);white-space:nowrap}
.ipt{font-size:1.2rem}.ipt td{color:var(--ink)}.ipt td.c4{color:var(--pink)}
/* header grid */
.hdrcard{padding:1.2rem 1.4rem}
.ruler{display:flex;justify-content:space-between;color:var(--dim);font-size:.8rem;margin-bottom:.3rem}
.hdr{display:flex;flex-direction:column;gap:.4rem}
.hrow{display:grid;grid-template-columns:repeat(32,minmax(0,1fr));gap:.4rem}
.fld{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:.1rem;
  min-height:3.3rem;padding:.35rem;border:1.5px solid var(--c);border-radius:12px;background:rgba(255,255,255,.1);cursor:help;outline:none;transition:background .15s}
.fld.sky{--c:var(--sky)}.fld.lilac{--c:var(--lilac)}.fld.pink{--c:var(--pink)}.fld.mint{--c:var(--mint)}.fld.dim{--c:rgba(255,255,255,.4);border-style:dashed}
.fld b{font-size:.98rem;line-height:1.15}.fld .mono{font-size:.75rem;color:var(--dim)}
.fld:hover,.fld:focus-visible{background:rgba(255,255,255,.26);z-index:5}
.tip{position:absolute;left:50%;bottom:calc(100% + 10px);transform:translate(-50%,4px);width:min(24rem,80vw);background:#2d2490;border:1px solid var(--edge);color:#fff;
  font-size:.95rem;line-height:1.4;text-align:left;padding:.7rem .9rem;border-radius:12px;opacity:0;pointer-events:none;transition:opacity .15s,transform .15s}
.fld:hover .tip,.fld:focus-visible .tip{opacity:1;transform:translate(-50%,0)}
.hrow:first-child .tip{bottom:auto;top:calc(100% + 10px)}
/* ipv6 compare */
.col46{padding:1rem 1.1rem;display:flex;flex-direction:column;gap:.45rem;align-self:start}
.chipf{max-height:3rem;overflow:hidden;padding:.42rem .8rem;border-radius:10px;border:1.5px solid rgba(255,255,255,.35);background:rgba(255,255,255,.1);font-size:.98rem;font-weight:600}
.chipf.sky{border-color:var(--sky)}.chipf.lilac{border-color:var(--lilac)}.chipf.mint{border-color:var(--mint)}.chipf.pink{border-color:var(--pink)}
/* terminal */
.term{padding:1rem 1.2rem;font-size:1rem;line-height:1.7;background:rgba(30,20,110,.35)}
.rowp{border-radius:6px;padding:0 .3rem;margin:0 -.3rem}
.dump{font-size:.88rem;align-self:start;word-break:break-all}
/* path */
.pathwrap{display:flex;flex-direction:column;gap:.7rem}
.pathsvg{padding:.5rem .8rem}.pathsvg .dg{max-height:46vh}
.pbar{display:grid;grid-template-columns:minmax(0,1fr);gap:.7rem}
.pkp{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;padding:.7rem 1rem}
.pkh{font-size:.8rem;letter-spacing:.1em;text-transform:uppercase;color:var(--dim)}
.kv{display:flex;justify-content:space-between;gap:.8rem;font-size:.95rem;padding:.18rem .3rem;border-bottom:1px solid rgba(255,255,255,.18);border-radius:4px}
.kv span{color:var(--dim)}
.pcap{display:flex;align-items:center;gap:1rem;justify-content:space-between;padding:.7rem 1rem}
.pcap .btn{white-space:nowrap;flex:none}
.pcap p{font-size:1.1rem;font-weight:600;line-height:1.35}
.panels{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:.6rem}
.pnl{padding:.6rem .8rem;opacity:.5;transition:opacity .28s var(--ez),background .28s var(--ez),border-color .28s}
.pnl b{font-size:.95rem}.pnl p{font-size:.82rem;line-height:1.35;color:var(--dim);margin-top:.2rem}
.pnl.on{opacity:1;background:rgba(255,255,255,.24);border-color:var(--mint)}
.ptext{padding:1rem 1.2rem}.ptext .p{max-width:none}
.gw{padding:1.2rem;display:flex;flex-direction:column;gap:.7rem}
.gwr{display:flex;flex-wrap:wrap;gap:.4rem 1rem;align-items:baseline;justify-content:space-between;padding:.7rem 1rem;border-radius:12px;background:rgba(255,255,255,.1);font-size:1.1rem}
.gwr span{color:var(--dim)}.gwr.big{font-size:1.3rem;border:1.5px solid var(--pink)}.gwr.ok{border-color:var(--mint)}
.term.big{font-size:1.35rem}
.qas{display:flex;flex-direction:column;gap:.7rem}
.qa{padding:.9rem 1.1rem;display:flex;flex-wrap:wrap;gap:.6rem;align-items:center;justify-content:space-between}
.qq{display:flex;gap:.8rem;align-items:center;flex:1 1 26rem;font-size:1.08rem}
.qa-a{flex:1 1 100%;color:var(--mint);font-size:1.05rem;line-height:1.45}
/* trainers */
.lst{padding:1.3rem 1.5rem}
.trn,.quiz{padding:1.4rem 1.5rem}
.tq{font-size:1.3rem;line-height:1.4;margin-bottom:1rem}
.trow{display:flex;flex-wrap:wrap;gap:.6rem;align-items:center;margin-bottom:.8rem}
.trow input{font-size:1.3rem;width:8em;padding:.5rem .7rem;border:1.5px solid var(--edge);border-radius:12px;color:#fff;background:rgba(255,255,255,.14)}
.trow input:focus-visible{outline:3px solid var(--mint);outline-offset:1px}
.btn{font:inherit;font-size:.95rem;font-weight:600;padding:.55rem .95rem;border-radius:12px;border:1.5px solid var(--edge);background:rgba(255,255,255,.12);color:#fff;cursor:pointer;transition:background .15s,border-color .15s}
.btn:hover{background:rgba(255,255,255,.24)}
.btn:active{background:rgba(255,255,255,.32)}
.btn.pri{background:#fff;border-color:#fff;color:var(--deep)}
.btn.pri:hover{background:var(--mint);border-color:var(--mint)}
.btn:disabled{opacity:.45;cursor:default}
.btn:focus-visible,.opt:focus-visible,#nav button:focus-visible,.ovi:focus-visible,.fld:focus-visible{outline:3px solid var(--mint);outline-offset:2px}
.tres{min-height:2.6rem;font-size:1.08rem;line-height:1.45;margin-bottom:.6rem}
.tres.ok{color:var(--mint)}.tres.no{color:var(--pink)}
.tscore{color:var(--dim)}
.opts{display:grid;grid-template-columns:1fr 1fr;gap:.6rem;margin-bottom:1rem}
.opts.col{grid-template-columns:1fr}
.opt{font:inherit;text-align:left;font-size:1.02rem;padding:.7rem 1rem;border-radius:12px;border:1.5px solid var(--edge);background:rgba(255,255,255,.1);color:#fff;cursor:pointer;word-break:break-word}
.opt:hover{background:rgba(255,255,255,.22)}
.opt.ok{border-color:var(--mint);background:rgba(93,220,176,.3)}.opt.no{border-color:var(--pink);background:rgba(240,122,180,.3)}
.qtop{display:flex;justify-content:space-between;color:var(--dim);margin-bottom:.6rem}
.quizrow{align-items:start}
/* nav */
#nav{position:fixed;z-index:40;left:50%;bottom:12px;transform:translateX(-50%);display:flex;align-items:center;gap:.3rem;flex-wrap:wrap;justify-content:center;
  background:rgba(45,35,150,.5);-webkit-backdrop-filter:blur(16px) saturate(140%);backdrop-filter:blur(16px) saturate(140%);border:1px solid var(--edge);border-radius:var(--r);box-shadow:var(--hl),var(--sh);padding:.35rem .5rem;font-size:14px;max-width:calc(100vw - 24px)}
#nav button{font:inherit;font-size:13px;font-weight:600;border:1px solid transparent;background:transparent;color:#fff;border-radius:10px;padding:.42rem .6rem;cursor:pointer;display:inline-flex;align-items:center;gap:.3rem}
#nav button:hover{background:rgba(255,255,255,.18)}
#nav button[aria-pressed="true"]{background:#fff;color:var(--deep)}
#nav svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round}
.nsep{width:1px;height:22px;background:var(--edge);margin:0 .2rem}
#ind{font-family:var(--mono);font-size:13px;padding:0 .4rem;white-space:nowrap}
#ind .st{color:var(--dim);margin-left:.6rem}
.seg{display:inline-flex;border:1px solid var(--edge);border-radius:10px;padding:2px}
#ov{position:fixed;inset:0;z-index:60;background:rgba(70,55,190,.9);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);overflow:auto;padding:clamp(16px,5vh,60px) clamp(16px,6vw,120px)}
#ov h2{margin-bottom:1.2rem;font-size:1.8rem}
.ovg{display:grid;grid-template-columns:repeat(auto-fill,minmax(14rem,1fr));gap:.7rem}
.ovi{font:inherit;text-align:left;display:flex;gap:.8rem;align-items:center;padding:.8rem 1rem;background:var(--glass);border:1px solid var(--edge);border-radius:14px;cursor:pointer;color:#fff;font-size:1rem}
.ovi:hover{background:rgba(255,255,255,.24)}.ovi.cur{border-color:var(--mint);box-shadow:inset 0 0 0 1px var(--mint)}
.ovi .mono{color:var(--mint);font-weight:700;width:2rem}
@media (min-width:768px){.g2{grid-template-columns:repeat(2,minmax(0,1fr))}.g3{grid-template-columns:repeat(3,minmax(0,1fr))}.pbar{grid-template-columns:minmax(0,1.3fr) minmax(0,1fr)}}
@media (min-width:768px) and (max-width:1279px){.g3{grid-template-columns:repeat(2,minmax(0,1fr))}.panels{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (min-width:1280px){.two{grid-template-columns:repeat(2,minmax(0,1fr))}.two:has(> [data-scene]){grid-template-columns:minmax(0,.75fr) minmax(0,1.25fr)}}
@media (max-width:767px){
  html{font-size:15px}
  h2,.tight h2{font-size:min(1.8rem,30px)}
  .sc{padding-bottom:10rem}
  .steps.big li{font-size:1.3rem}
  .hrow{gap:.2rem}.fld b{font-size:.62rem}.fld .mono{font-size:.55rem}.fld{min-height:2.8rem;padding:.2rem}
  .opts{grid-template-columns:1fr}
  .dg,.pathsvg .dg{max-height:none}
  .panels{grid-template-columns:1fr 1fr}
  .pkp{grid-template-columns:1fr}
  .pcap{flex-direction:column;align-items:flex-start}
  .tbl{min-width:40rem}
  #nav{bottom:6px;font-size:12px;width:calc(100vw - 12px)}
  #nav .lbl2{display:none}
}
.figs .wrap{max-width:none;width:100%}.figs .sh{margin-bottom:.4rem}.figs .sh h2{font-size:1.5rem}.figx{margin:0;display:flex;justify-content:center}.figx img{width:auto;max-width:100%;max-height:80vh;image-rendering:auto;height:auto;border-radius:16px;box-shadow:0 14px 44px rgba(10,6,40,.35)}
.wsx{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:1.6rem;align-items:start}
@media (max-width:900px){.wsx{grid-template-columns:1fr}}
.wsk{background:#fff;color:#1b1d33;border-radius:14px;overflow:hidden;box-shadow:0 12px 36px rgba(10,6,40,.3);font-size:.8rem}
.wsd{padding:.9em 1.1em;font-family:var(--mono);line-height:1.8;background:#fafbfe;overflow-x:auto}
.wl{white-space:nowrap}.wl.i1{padding-left:1.4em}.wl.i2{padding-left:2.8em;color:#445}.wl.dim{color:#8a8fa8}
.whl{background:#fff1a8;border-radius:5px;padding:.1em .35em}
.wn{display:inline-grid;place-items:center;width:1.45em;height:1.45em;border-radius:50%;background:#e5383b;color:#fff;font:700 .8em/1 var(--f);margin-right:.45em;vertical-align:.1em}
.wbad{background:#e5383b!important;color:#fff!important}
.wsl li{font-size:.95rem!important;line-height:1.4}
.slide.on .wsx [data-s],.wsx [data-s]{opacity:1;transform:none}
.chr{position:absolute;bottom:3.2rem;width:clamp(120px,15vw,300px);height:auto;pointer-events:none;z-index:3;filter:drop-shadow(0 12px 24px rgba(10,6,40,.35));animation:bob 4s ease-in-out infinite}
.chr-r{right:2.2rem}.chr-l{left:2.2rem}
@keyframes bob{50%{transform:translateY(-10px)}}
.ovg{grid-template-columns:repeat(auto-fill,minmax(17rem,1fr));gap:1rem}
.ovi{flex-direction:column;align-items:stretch;gap:.45rem;padding:.5rem}
.ovt{position:relative;width:100%;aspect-ratio:16/9;overflow:hidden;border-radius:8px;border:1px solid rgba(255,255,255,.25);pointer-events:none;background:#3f358f}
.ovt>.slide{position:absolute!important;inset:auto!important;left:0;top:0;display:block!important;transform-origin:0 0}
.ovt [data-s]{opacity:1!important;transform:none!important}
.ovi .ovn{display:flex;gap:.6rem;align-items:baseline;font-size:.95rem}
.fld.off{opacity:.3;filter:saturate(.4)}
.fld.big{min-height:6.4rem}
.figh{max-width:92rem;margin:0 auto}.figh .fld{min-height:4.2rem}.figh .fld b{font-size:1.15rem}.figh .fld.big{min-height:7rem}
.htot{text-align:center;margin-top:.9rem;font-size:1.05rem;opacity:.9}
.flow{display:flex;flex-direction:column;align-items:center;gap:0;max-width:64rem;margin:0 auto}
.fl-b{background:var(--glass);border:1px solid var(--edge);border-radius:16px;padding:1rem 1.6rem;text-align:center;font-size:1.25rem;line-height:1.45;box-shadow:var(--hl),var(--sh)}
.fl-a{width:3px;height:2rem;background:rgba(255,255,255,.7);position:relative}
.fl-a::after{content:"";position:absolute;left:50%;bottom:-2px;transform:translateX(-50%);border:8px solid transparent;border-top-color:rgba(255,255,255,.85)}
.fl-d{width:15rem;height:15rem;display:grid;place-items:center;margin:1.2rem 0}
.fl-d span{display:grid;place-items:center;width:10.6rem;height:10.6rem;transform:rotate(45deg);background:rgba(93,220,176,.28);border:2px solid var(--mint);border-radius:18px}
.fl-d span{font-size:0;position:relative}
.fl-d span::after{content:"IP-адреса в одной сети?";position:absolute;inset:0;display:grid;place-items:center;transform:rotate(-45deg);font-size:1.15rem;font-weight:700;text-align:center;padding:1.4rem}
.fl-split{display:grid;grid-template-columns:1fr 1fr;gap:2.4rem;width:100%}
.fl-br{display:flex;flex-direction:column;align-items:center;gap:.6rem}
.fl-tag{font-weight:800;font-family:var(--mono);padding:.25rem .9rem;border-radius:999px}
.fl-tag.ok{background:var(--mint);color:var(--deep)}.fl-tag.no{background:var(--pink);color:#fff}
.fl-b.ok{border-color:var(--mint)}.fl-b.no{border-color:var(--pink)}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{transition:none!important;animation:none!important}}
@media print{.slide{display:block;position:relative;height:auto;page-break-after:always}[data-s]{opacity:1;transform:none}#nav,#prog{display:none}html,body{overflow:visible;height:auto}}
"""

# ---------------------------------------------------------------- JS
JS = r"""
(function(){
'use strict';
var $=function(s,r){return (r||document).querySelector(s)}, $$=function(s,r){return [].slice.call((r||document).querySelectorAll(s))};
var SCENES=__SCENES__;
var slides=$$('.slide'), N=slides.length, cur=0, step=0, mode='steps', speed=1, timer=null, playing=false, paused=false;
var RM=window.matchMedia('(prefers-reduced-motion: reduce)');
var root=document.documentElement;
slides.forEach(function(s){
  var els=$$('[data-s],[data-k],[data-p]',s), mx=0;
  els.forEach(function(e){['s','k','p'].forEach(function(a){var v=+e.dataset[a]||0; if(v>mx)mx=v;});});
  var sc=$('[data-scene]',s);
  if(sc){ var sp=SCENES[sc.dataset.scene]; sc._sp=sp; sc._map={};
    Object.keys(sp.e).forEach(function(id){ var el=$('[data-id="'+id+'"]',sc); if(el){ el._b=el.getAttribute('class')||''; sc._map[id]=el; } });
    s._scene=sc; mx=Math.max(mx,sp.n); }
  s._els=els; s._max=mx;
});
function applyScene(sc,k,instant){
  var sp=sc._sp; k=Math.min(k,sp.n);
  Object.keys(sp.e).forEach(function(id){
    var el=sc._map[id], t=sp.e[id]; if(!el) return;
    if(t.p){ el.style.transform='translate('+t.p[k][0]+'px,'+t.p[k][1]+'px)'; }
    if(t.o){ el.style.opacity=t.o[k]; }
    if(t.c){ var c=t.c[k]; el.setAttribute('class',(el._b+' '+c).trim()); }
    if(t.t){ if(el.textContent!==t.t[k]){ el.textContent=t.t[k];
      if(!instant && el.tagName!=='text' && el.tagName!=='P'){ var kv=el.parentNode; kv.classList.remove('flash'); void kv.offsetWidth; kv.classList.add('flash'); } } }
  });
}
function waitFor(sl,k){
  if(sl._scene && k<=sl._scene._sp.n) return sl._scene._sp.w[k]||1100;
  var w=0;
  sl._els.forEach(function(e){ if(+e.dataset.s===k||+e.dataset.k===k){ w=Math.max(w,+e.dataset.w||0); } });
  return w||300;
}
function setStep(k,instant){
  var sl=slides[cur]; step=Math.max(0,Math.min(sl._max,k));
  if(instant) sl.classList.add('ni');
  sl._els.forEach(function(e){
    var d=e.dataset;
    if(d.s) e.classList.toggle('in',+d.s<=step);
    if(d.k) e.classList.toggle('kl',+d.k<=step);
    if(d.p!==undefined){
      if(d.k!==undefined) e.classList.toggle('pulse',+d.p<=step && +d.k>step);
      else { e.classList.remove('pulse'); if(!instant && +d.p===step){ void e.getBoundingClientRect(); e.classList.add('pulse'); } } }
  });
  if(sl._scene) applyScene(sl._scene,step,instant);
  if(instant){ void sl.offsetWidth; sl.classList.remove('ni'); }
  ui();
}
function stopPlay(){ clearTimeout(timer); timer=null; playing=false; paused=false; ui(); }
function schedule(ms){ clearTimeout(timer); timer=setTimeout(tick, ms/speed); }
function tick(){
  var sl=slides[cur];
  if(step>=sl._max){ playing=false; paused=false; ui();
    if(sl.dataset.anim==='loop'&&!RM.matches){ var me=cur; timer=setTimeout(function(){ if(cur===me&&ov.hidden) play(); },2600); }
    return; }
  setStep(step+1,false);
  schedule(waitFor(sl,step));
}
function play(from){
  stopPlay();
  if(RM.matches){ setStep(slides[cur]._max,true); return; }
  if(!slides[cur]._max) return;
  setStep(from||0,true); playing=true; ui(); schedule(280);
}
function togglePause(){
  if(!playing) return false;
  if(paused){ paused=false; schedule(280); } else { paused=true; clearTimeout(timer); }
  ui(); return true;
}
function go(i,atEnd){
  i=Math.max(0,Math.min(N-1,i));
  stopPlay();
  slides.forEach(function(s){s.classList.remove('on')}); cur=i; slides[cur].classList.add('on');
  var sc=$('.sc',slides[cur]); if(sc) sc.scrollTop=0;
  var hasSc=!!slides[cur]._scene;
  setStep((hasSc&&!RM.matches)?0:slides[cur]._max,true);
  try{ history.replaceState(null,'','#'+(cur+1)); }catch(e){}
  if(hasSc && !RM.matches) play();
}
function next(){ if(cur<N-1) go(cur+1); }
function prev(){ if(cur>0) go(cur-1); }
var ind=$('#ind'), bPlay=$('#b-play');
function ui(){
  var mx=slides[cur]._max;
  ind.textContent=(cur+1)+' / '+N;
  $('#prog i').style.width=((cur+1)/N*100)+'%';
  bPlay.disabled=!slides[cur]._scene; bPlay.style.visibility=slides[cur]._scene?'':'hidden';
}
$('#b-prev').onclick=prev; $('#b-next').onclick=next;
bPlay.onclick=function(){ play(); };
document.addEventListener('click',function(e){ var b=e.target.closest&&e.target.closest('.qa-b'); if(!b) return;
  var a=b.nextElementSibling; a.hidden=!a.hidden; b.textContent=a.hidden?'Показать ответ':'Скрыть ответ'; });
var ov=$('#ov'), ovg=$('.ovg',ov);
slides.forEach(function(s,k){
  var b=document.createElement('button'); b.className='ovi'; b.type='button';
  b.innerHTML='<span class="ovt"></span><span class="ovn"><span class="mono">'+(k+1)+'</span><span></span></span>'; b.querySelector('.ovn').lastChild.textContent=s.dataset.label;
  b.onclick=function(){ closeOv(); go(k); }; ovg.appendChild(b);
});
var ovBuilt=false;
function buildThumbs(){
  var W=innerWidth, H=innerHeight;
  $$('.ovi',ov).forEach(function(b,k){
    var box=$('.ovt',b); box.innerHTML='';
    var c=slides[k].cloneNode(true); c.classList.add('on'); c.removeAttribute('id');
    $$('[id]',c).forEach(function(e){e.removeAttribute('id')});
    $$('input,button,select,textarea',c).forEach(function(e){e.tabIndex=-1});
    c.setAttribute('aria-hidden','true'); c.style.width=W+'px'; c.style.height=H+'px';
    box.appendChild(c); c.style.transform='scale('+(box.clientWidth/W)+')';
  });
  ovBuilt=true;
}
addEventListener('resize',function(){ ovBuilt=false; if(!ov.hidden) buildThumbs(); });
function openOv(){ stopPlay(); ov.hidden=false; if(!ovBuilt) buildThumbs(); $$('.ovi',ov).forEach(function(b,k){b.classList.toggle('cur',k===cur)}); var c=$('.ovi.cur',ov); if(c)c.focus(); }
function closeOv(){ ov.hidden=true; }
$('#b-ov').onclick=openOv;
var dbuf='', dtm=null;
document.addEventListener('keydown',function(e){
  var t=e.target, tag=t.tagName;
  if(e.ctrlKey||e.metaKey||e.altKey) return;
  if(tag==='INPUT'||tag==='TEXTAREA'){ if(e.key==='Escape') t.blur(); return; }
  if(e.key==='Escape'){ e.preventDefault(); ov.hidden?openOv():closeOv(); return; }
  if(!ov.hidden) return;
  switch(e.key){
    case 'ArrowRight': case 'ArrowDown': case 'PageDown': e.preventDefault(); next(); return;
    case 'ArrowLeft': case 'ArrowUp': case 'PageUp': e.preventDefault(); prev(); return;
    case ' ': if(tag==='BUTTON') return; e.preventDefault(); next(); return;
    case 'Home': e.preventDefault(); go(0); return;
    case 'End': e.preventDefault(); go(N-1); return;
  }
  var k=e.key.toLowerCase();
  if(k==='r'||k==='к'){ play(); return; }
  if(/^[0-9]$/.test(e.key)){
    dbuf+=e.key; clearTimeout(dtm);
    dtm=setTimeout(function(){ var n=parseInt(dbuf,10); dbuf=''; if(n>=1&&n<=N) go(n-1); },550);
  }
});
var lastWheel=0;
window.addEventListener('wheel',function(e){
  if(!ov.hidden) return;
  var sc=$('.sc',slides[cur]); if(!sc) return;
  var dy=e.deltaY; if(Math.abs(dy)<4) return;
  if(dy>0 && sc.scrollTop+sc.clientHeight<sc.scrollHeight-2) return;
  if(dy<0 && sc.scrollTop>0) return;
  var now=Date.now(); if(now-lastWheel<420) return; lastWheel=now;
  if(dy>0){ if(cur<N-1) go(cur+1); } else { if(cur>0) go(cur-1); }
},{passive:true});
var tx=0, ty=0, tt=0;
window.addEventListener('touchstart',function(e){ var p=e.changedTouches[0]; tx=p.clientX; ty=p.clientY; tt=Date.now(); },{passive:true});
window.addEventListener('touchend',function(e){
  var p=e.changedTouches[0], dx=p.clientX-tx, dy=p.clientY-ty;
  if(Date.now()-tt>700||Math.abs(dx)<60||Math.abs(dx)<Math.abs(dy)*1.4) return;
  if(e.target.closest&&e.target.closest('input,.tw')) return;
  dx<0?next():prev();
},{passive:true});

/* ---- trainers ---- */
function rnd(n){ return Math.floor(Math.random()*n); }
function shuffle(a){ a=a.slice(); for(var i=a.length-1;i>0;i--){ var j=rnd(i+1), t=a[i]; a[i]=a[j]; a[j]=t; } return a; }
(function(){
  var ans=0, expl='', tot=0, ok=0, answered=false, inp=$('#tt-in'), res=$('#tt-r');
  function nx(){
    var t=rnd(3), st=[64,128,255][rnd(3)];
    if(t===0){ var h=3+rnd(25), got=st-h; $('#tt-q').innerHTML='Начальное значение TTL на узле – <b class="mono">'+st+'</b>. Эхо-ответ пришёл с <b class="mono">TTL='+got+'</b>. Сколько «прыжков» совершил пакет?'; ans=h; expl=st+' – '+got+' = '+h; }
    else if(t===1){ var r=1+rnd(6), s=1+rnd(4); $('#tt-q').innerHTML='Пакет отправлен с <b class="mono">TTL='+st+'</b> и прошёл через <b class="mono">'+r+'</b> маршрутизатор(а) и <b class="mono">'+s+'</b> коммутатор(а). Какой TTL у пакета теперь?'; ans=st-r; expl='коммутаторы TTL не меняют: '+st+' – '+r+' = '+ans; }
    else { var i=2+rnd(8); $('#tt-q').innerHTML='Команда <span class="mono">ping -t '+i+'</span>. На каком по счёту маршрутизаторе пакет будет отброшен с сообщением Time Exceeded (узел назначения дальше)?'; ans=i; expl='маршрутизатор, принявший пакет с TTL=1, – '+i+'-й по счёту'; }
    inp.value=''; res.textContent=''; res.className='tres'; answered=false;
  }
  function chk(){
    var v=inp.value.trim(); if(!/^\d+$/.test(v)){ res.textContent='Введите ответ числом.'; res.className='tres no'; return; }
    if(!answered){ tot++; if(+v===ans) ok++; answered=true; }
    res.textContent=(+v===ans?'Верно: ':'Неверно: ')+expl+'.'; res.className='tres '+(+v===ans?'ok':'no');
    $('#tt-sc').textContent=ok+' / '+tot;
  }
  $('#tt-ok').onclick=chk; $('#tt-nx').onclick=nx;
  inp.addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); answered?nx():chk(); } });
  nx();
})();
function choiceTrainer(qid,oid,rid,nid,scid,gen){
  var tot=0, ok=0;
  function nx(){
    var q=gen(), o=$(oid), done=false; $(qid).innerHTML=q.q; o.innerHTML=''; $(rid).textContent=''; $(rid).className='tres';
    shuffle(q.o).forEach(function(t){
      var b=document.createElement('button'); b.type='button'; b.className='opt'; b.textContent=t;
      b.onclick=function(){
        if(done) return; done=true; var good=t===q.o[0];
        $$('.opt',o).forEach(function(x){ if(x.textContent===q.o[0]) x.classList.add('ok'); });
        if(!good) b.classList.add('no');
        tot++; if(good) ok++;
        $(rid).textContent=(good?'Верно. ':'Неверно. ')+q.e; $(rid).className='tres '+(good?'ok':'no');
        if(scid) $(scid).textContent=ok+' / '+tot;
      };
      o.appendChild(b);
    });
  }
  $(nid).onclick=nx; nx();
}
var SEGS=[['PC-A – R1','AA-BB-CC-11-22-33','AA-AA-AA-AA-AA-AA'],['R1 – R2','AA-BB-BB-BB-BB-BB','AA-CC-CC-CC-CC-CC'],['R2 – R3','AA-DD-DD-DD-DD-DD','AA-EE-EE-EE-EE-EE'],['R3 – PC-B','AA-FF-FF-FF-FF-FF','AA-BB-CC-22-33-44']];
var RT=__ROUTES__;
choiceTrainer('#tr-q','#tr-o','#tr-r','#tr-nx','#tr-sc',function(){
  var t=rnd(3);
  if(t<2){ var s=SEGS[rnd(4)], dst=t===0;
    var all=[]; SEGS.forEach(function(x){ all.push(x[1],x[2]); });
    var right=dst?s[2]:s[1], other=shuffle(all.filter(function(m){return m!==right})).slice(0,3);
    return {q:'Пакет PC-A – PC-B на участке <b>'+s[0]+'</b>. Какой MAC-адрес '+(dst?'<b>назначения</b>':'<b>источника</b>')+' в кадре?', o:[right].concat(other),
      e:'На участке '+s[0]+': Src MAC '+s[1]+', Dst MAC '+s[2]+'. MAC-адреса меняются на каждом участке.'}; }
  var r=['R1','R2','R3'][rnd(3)], toB=rnd(2)===0, net=toB?'192.168.3.0/24':'192.168.1.0/24', dip=toB?'192.168.3.2':'192.168.1.2';
  var rows=RT[r], right=rows.filter(function(x){return x.indexOf(net)>=0})[0];
  var others=rows.filter(function(x){return x!==right});
  while(others.length<3) others.push('маршрут не найден – пакет отбрасывается');
  return {q:'Маршрутизатор <b>'+r+'</b> получил пакет с DstIP <b class="mono">'+dip+'</b>. Какой строкой таблицы он воспользуется?', o:[right].concat(others.slice(0,3)),
    e:r+' сравнивает DstIP с сетями таблицы: подходит «'+right+'».'};
});
var FIELDS=__FIELDS__;
choiceTrainer('#tf-q','#tf-o','#tf-r','#tf-nx',null,function(){
  var f=FIELDS[rnd(FIELDS.length)], opts=[4,8,13,16,20,32].map(String);
  var right=String(f[1]); var o=[right].concat(shuffle(opts.filter(function(x){return x!==right})).slice(0,3));
  return {q:'Какова длина поля <b>'+f[0]+'</b> в заголовке '+f[2]+' (бит)?', o:o, e:f[0]+' – '+f[1]+' бит. '+f[3]};
});
(function(){
  var Q=__QUIZ__, i=0, got=Q.map(function(){return -1});
  function score(){ return got.filter(function(g,k){return g===Q[k].a}).length; }
  function render(){
    var q=Q[i]; $('#qz-n').textContent=(i+1)+' / '+Q.length; $('#qz-q').textContent=q.q;
    var o=$('#qz-o'); o.innerHTML=''; var e=$('#qz-e'); e.textContent=''; e.className='tres';
    q.o.forEach(function(t,k){
      var b=document.createElement('button'); b.type='button'; b.className='opt'; b.textContent=t;
      b.onclick=function(){ if(got[i]<0) got[i]=k; show(); };
      o.appendChild(b);
    });
    if(got[i]>=0) show();
    $('#qz-sc').textContent='верно: '+score();
    $('#qz-pv').disabled=i===0; $('#qz-nx').textContent=i===Q.length-1?'Начать заново':'Следующий вопрос';
  }
  function show(){
    var q=Q[i], bs=$$('.opt',$('#qz-o'));
    bs[q.a].classList.add('ok'); if(got[i]!==q.a) bs[got[i]].classList.add('no');
    var e=$('#qz-e'); e.textContent=(got[i]===q.a?'Верно. ':'Неверно. ')+q.e; e.className='tres '+(got[i]===q.a?'ok':'no');
    $('#qz-sc').textContent='верно: '+score();
  }
  $('#qz-nx').onclick=function(){ if(i===Q.length-1){ got=Q.map(function(){return -1}); i=0; } else i++; render(); };
  $('#qz-pv').onclick=function(){ if(i>0){ i--; render(); } };
  render();
})();

var h=parseInt((location.hash||'').slice(1),10);
go(h>=1&&h<=N?h-1:0);
if(RM.addEventListener) RM.addEventListener('change',function(){ go(cur,true); });
})();
"""

FIELDS = [["Version", 4, "IPv4", "Версия протокола."], ["IHL", 4, "IPv4", "Длина заголовка в «словах»."],
          ["DSCP", 6, "IPv4", "Приоритет пакета для QoS."], ["Total Length", 16, "IPv4", "Длина пакета не превышает 65535 байт."],
          ["Identification", 16, "IPv4", "Копируется во все фрагменты."], ["Fragment Offset", 13, "IPv4", "Для первого фрагмента равно 0."],
          ["TTL", 8, "IPv4", "Максимальное количество прыжков."], ["Protocol", 8, "IPv4", "Номер инкапсулированного протокола."],
          ["Header Checksum", 16, "IPv4", "Пересчитывается после изменения TTL."], ["Source IP Address", 32, "IPv4", "Адрес отправителя."],
          ["Version", 4, "IPv6", "Версия протокола."], ["Hop Limit", 8, "IPv6", "Максимальное значение 255."]]
FIELDS = [f for f in FIELDS if f[1] in (4, 8, 13, 16, 20, 32)]

ICON_L = '<svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg>'
ICON_R = '<svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg>'
ICON_LL = '<svg viewBox="0 0 24 24"><path d="M12 5l-7 7 7 7M19 5l-7 7 7 7"/></svg>'
ICON_RR = '<svg viewBox="0 0 24 24"><path d="M12 5l7 7-7 7M5 5l7 7-7 7"/></svg>'

def render():
    out = ['<!doctype html><html lang="ru"><head><meta charset="utf-8">'
           '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
           '<title>Глава 9. Сетевой уровень</title><style>' + CSS.replace('__BGIMG__', BGIMG) + '</style></head><body>' + DEFS +
           '<div id="prog"><i></i></div><main id="deck">']
    for label, kick, title, body, cls in S:
        head = "" if not title else f'<header class="sh">{"<div class=kick>"+kick+"</div>" if kick else ""}<h2>{title}</h2></header>'
        anim = 'loop' if label in ANIM_LOOP else ''
        out.append(f'<section class="slide {cls}" data-label="{label}" data-anim="{anim}"><div class="sc"><div class="wrap">{head}{body}</div></div></section>')
    out.append('</main>')
    out.append('<nav id="nav" aria-label="Навигация по слайдам">'
               f'<button id="b-prev" type="button" aria-label="Предыдущий слайд">{ICON_L}</button>'
               '<span id="ind" aria-live="polite"></span>'
               f'<button id="b-next" type="button" aria-label="Следующий слайд">{ICON_R}</button>'
               '<span class="nsep"></span>'
               '<button id="b-play" type="button" title="Клавиша R"><svg viewBox="0 0 24 24"><path d="M4 12a8 8 0 1 0 2.5-5.8M4 4v5h5"/></svg><span class="lbl2">Повторить анимацию</span></button>'
               '<button id="b-ov" type="button" title="Esc"><svg viewBox="0 0 24 24"><path d="M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h6v6h-6z"/></svg><span class="lbl2">Меню</span></button>'
               '</nav>')
    out.append('<div id="ov" hidden><h2>Содержание</h2><div class="ovg"></div></div>')
    js = (JS.replace("__SCENES__", json.dumps(SCENES, ensure_ascii=False, separators=(",", ":")))
            .replace("__QUIZ__", json.dumps(QUIZ, ensure_ascii=False))
            .replace("__ROUTES__", json.dumps(ROUTES, ensure_ascii=False))
            .replace("__FIELDS__", json.dumps(FIELDS, ensure_ascii=False))
            )
    out.append('<script>' + js + '</script></body></html>')
    OUT.write_text("".join(out), encoding="utf-8")
    print(len(S), "slides", OUT.stat().st_size, "bytes")

# ==== доработка по ЛК9: схемы, Wireshark вёрсткой, задник, персонажи, анимация по месту ====
import base64, io, glob
from PIL import Image as _Im
DL = r"C:/Users/anank/Downloads/"
PP = r"C:/Users/anank/AppData/Local/Temp/claude/p9/"
CH = r"C:/Users/anank/AppData/Local/Temp/claude/chars/"
def _jpg(path, w=2400, q=92):
    im = _Im.open(path).convert("RGB")
    if im.width > w: im = im.resize((w, round(im.height*w/im.width)), _Im.LANCZOS)
    b = io.BytesIO(); im.save(b, "JPEG", quality=q, optimize=True, progressive=True, subsampling=0)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
def _png(path, w=420):
    im = _Im.open(path).convert("RGBA"); im.thumbnail((w, w))
    b = io.BytesIO(); im.save(b, "WEBP", quality=82, method=6)
    return "data:image/webp;base64," + base64.b64encode(b.getvalue()).decode()
def _dl(pref): return glob.glob(DL + pref + "*.jpg")[0]
def figslide(label, kick, title, src):
    return (label, kick, title, f'<figure class="figx"><img src="{_jpg(src)}" alt="{title}"></figure>', "figs")
FIGS = [
 ("Без соединения", "Без соединения: схема", "Свойства IP", "Отправитель и получатель", _dl("STVkwuJj")),
 ("Негарантированная доставка", "Доставка: схема", "Свойства IP", "Пакет 1 потерян, повторно не отправлен", _dl("cMFpXyip")),
 ("Независимость от среды", "Среда: схема", "Свойства IP", "Разные среды передачи на одном пути", _dl("7HpxaUIe")),
 ("Заголовок IPv4", "Заголовок IPv4: схема", "Протокол IPv4", "Заголовок IPv4 целиком", _dl("sjGAyQie")),
 ("Поля IPv4: 1", "Поля IPv4 1: схема", "Протокол IPv4", "Version, IHL, DSCP, ECN, Total Length", _dl("bwPcBH1b")),
 ("Поля IPv4: 2", "Поля IPv4 2: схема", "Протокол IPv4", "Identification, флаги DF и MF, Fragment Offset", _dl("sBNfj5_G")),
 ("Поля IPv4: 3", "Поля IPv4 3: схема", "Протокол IPv4", "TTL, Protocol, Header Checksum", _dl("GReUSjuZ")),
 ("Поля IPv4: 4", "Поля IPv4 4: схема", "Протокол IPv4", "Адреса источника и назначения, опции", _dl("9ElgQHnp")),
 ("TTL", "TTL: схема", "Поле TTL", "TTL уменьшается на каждом маршрутизаторе", _dl("J74fdwjR")),
 ("Time Exceeded", "Time Exceeded: схема", "Поле TTL", "ping -t: время жизни закончилось в пути", _dl("p3OFeTg3")),
 ("Заголовок IPv6", "Заголовок IPv6: схема", "Протокол IPv6", "Заголовок IPv6 целиком", _dl("BU1ZScN0")),
 ("Поля IPv6: 1", "Поля IPv6 1: схема", "Протокол IPv6", "Version, Traffic Class, Flow Label", _dl("aMYwESFP")),
 ("Поля IPv6: 2", "Поля IPv6 2: схема", "Протокол IPv6", "Payload Length, Next Header, Hop Limit", _dl("iX5-go-0")),
 ("Передача между сетями", "Топология: схема", "Передача данных", "Топология: PC-A, R1, R2, R3, PC-B", _dl("9z-naJ_k")),
 ("Шлюз по умолчанию", "Шлюз: схема", "Передача данных", "Решение: своя сеть или шлюз", _dl("lq-iXLPS")),
 ("ARP и маршрутизатор", "ARP: схема", "Передача данных", "PC-A формирует пакет и кадр", _dl("sbjUBUIe")),
 ("Таблица маршрутизации", "Таблица R1: схема", "Передача данных", "Таблица маршрутизации R1", _dl("Ytg4lBI3")),
 ("R1 формирует кадр", "R1: схема", "Передача данных", "Кадр от R1 к R2, TTL = 254", _dl("ptT2Sh3M")),
 ("R2 получает кадр", "R2: схема", "Передача данных", "R2 сверяется с таблицей маршрутизации", _dl("bfdHO6RJ")),
 ("R2 пересылает", "R2 → R3: схема", "Передача данных", "Кадр от R2 к R3, TTL = 253", _dl("KZVdVLOA")),
 ("R3 получает кадр", "R3: схема", "Передача данных", "R3: сеть получателя подключена к G2", PP + "s30_1.png"),
 ("R3 доставляет", "R3 → PC-B: схема", "Передача данных", "Кадр от R3 к PC-B, TTL = 252", PP + "s31_1.png"),
]
# --- Wireshark вёрсткой ---
def _b(n): return f'<span class="wn">{n}</span>'
def _hl(txt, n=None): return f'<span class="whl">{_b(n) if n else ""}{txt}</span>'
def _wl(txt, lvl=0, cls=""): return f'<div class="wl i{lvl} {cls}">{txt}</div>'
def ws4(marks=True):
    m = (lambda n: n) if marks else (lambda n: None)
    h = (lambda t, n: _hl(t, m(n))) if marks else (lambda t, n: t)
    return ('<div class="wsk"><div class="wsd">'
      + _wl("▸ Frame 59: 1494 bytes on wire (11952 bits), 1494 bytes captured (11952 bits)", 0, "dim")
      + _wl("▸ Ethernet II, Src: Giga-Byt_d6:a9:2a, Dst: EltexEnt_f9:b0:80", 0, "dim")
      + _wl("▾ Internet Protocol Version 4, Src: 10.25.200.60, Dst: 3.164.206.11")
      + _wl(h("0100 .... = Version: 4", 1), 1)
      + _wl(h(".... 0101 = Header Length: 20 bytes (5)", 2), 1)
      + _wl(h("▸ Differentiated Services Field: 0x00 (DSCP: CS0, ECN: Not-ECT)", 3), 1)
      + _wl(h("Total Length: 1480", 4), 1)
      + _wl(h("Identification: 0xd06a (53354)", 5), 1)
      + _wl(h("▾ Flags: 0x40, Don't fragment", 6), 1)
      + _wl("0... .... = Reserved bit: Not set", 2) + _wl(".1.. .... = Don't fragment: Set", 2) + _wl("..0. .... = More fragments: Not set", 2)
      + _wl(h("...0 0000 0000 0000 = Fragment Offset: 0", 7), 1)
      + _wl(h("Time to Live: 64", 8), 1)
      + _wl(h("Protocol: TCP (6)", 9), 1)
      + _wl(h("Header Checksum: 0xc0c0 [validation disabled]", 10), 1)
      + _wl(h("Source Address: 10.25.200.60", 11), 1)
      + _wl(h("Destination Address: 3.164.206.11", None), 1)
      + '</div></div>')
def ws6(marks=True):
    m = (lambda n: n) if marks else (lambda n: None)
    h = (lambda t, n: _hl(t, m(n))) if marks else (lambda t, n: t)
    return ('<div class="wsk"><div class="wsd">'
      + _wl("▾ Internet Protocol Version 6, Src: 2603:1026:c0d:101f::2, Dst: 2a01:620:c12a:a500:953:6c6e:487:5201")
      + _wl(h("0110 .... = Version: 6", 1), 1)
      + _wl(h(".... 0000 0000 .... = Traffic Class: 0x00 (DSCP: CS0, ECN: Not-ECT)", 2), 1)
      + _wl(h(".... 1111 0100 0111 0110 1100 = Flow Label: 0xf476c", 3), 1)
      + _wl(h("Payload Length: 20", 4), 1)
      + _wl(h("Next Header: TCP (6)", 5), 1)
      + _wl(h("Hop Limit: 116", 6), 1)
      + _wl(h("Source Address: 2603:1026:c0d:101f::2", 7), 1)
      + _wl(h("Destination Address: 2a01:620:c12a:a500:953:6c6e:487:5201", 8), 1)
      + _wl("▸ Transmission Control Protocol, Src Port: 443, Dst Port: 50067, Seq: 1, Ack: 516, Len: 0", 0, "dim")
      + '</div></div>')
def wsexpl(rows):
    li = "".join(f'<li><span class="badge wbad">{k+1}</span><span><b>{a}</b> — <span class="mono">{b}</span>. {c}</span></li>' for k, (a, b, c) in enumerate(rows))
    return f'<ol class="steps sm wsl">{li}</ol>'
R4 = [("Version", "4 (0100)", "Пакет принадлежит версии IPv4"),
    ("Header Length", "20 bytes (5)", "IHL = 5: опций нет"),
    ("DSCP / ECN", "CS0 / Not-ECT", "Приоритет по умолчанию, уведомление о заторе не используется"),
    ("Total Length", "1480", "Длина пакета (заголовок + сегмент) в байтах"),
    ("Identification", "0xd06a (53354)", "Уникальный идентификатор пакета"),
    ("Flags", "0x40: DF = 1, MF = 0", "Фрагментация запрещена, фрагментов за пакетом нет"),
    ("Fragment Offset", "0", "Пакет не фрагментирован"),
    ("Time to Live", "64", "Оставшееся время жизни пакета"),
    ("Protocol", "TCP (6)", "Полезная нагрузка предназначена протоколу TCP"),
    ("Header Checksum", "0xc0c0", "Контрольная сумма заголовка"),
    ("Source / Destination", "10.25.200.60 → 3.164.206.11", "Адреса отправителя и получателя")]
R6 = [("Version", "6 (0110)", "Пакет принадлежит версии IPv6"),
    ("Traffic Class", "0x00", "Приоритет трафика по умолчанию"),
    ("Flow Label", "0xf476c", "Метка потока – идентификатор сессии TCP"),
    ("Payload Length", "20", "Длина полезной нагрузки в октетах"),
    ("Next Header", "TCP (6)", "Протокол L4, заголовков-расширений нет"),
    ("Hop Limit", "116", "Каждый маршрутизатор уменьшает значение на 1"),
    ("Source Address", "2603:1026:c0d:101f::2", "Адрес отправителя"),
    ("Destination Address", "2a01:620:c12a:a500:953:6c6e:487:5201", "Адрес получателя")]
for k, it in enumerate(S):
    if it[0] == "IPv4 в Wireshark":
        S[k] = (it[0], it[1], it[2], f'<div class="wsx">{ws4()}{wsexpl(R4)}</div>', "figs")
    if it[0] == "IPv6 в Wireshark":
        S[k] = (it[0], it[1], it[2], f'<div class="wsx">{ws6()}{wsexpl(R6)}</div>', "figs")
    if it[0] == "Вопросы: IPv4":
        S[k] = (it[0], it[1], it[2], it[3].replace(DUMP4, ws4(False)), it[4])
    if it[0] == "Вопросы: IPv6":
        S[k] = (it[0], it[1], it[2], it[3].replace(DUMP6, ws6(False)), it[4])
_new = []
for it in S:
    _new.append(it)
    for a, lab, kick, title, src in FIGS:
        if a == it[0]: _new.append(figslide(lab, kick, title, src))
S[:] = _new
# ==== слайды-схемы вёрсткой (как слайд «Заголовок IPv4») ====
def hdr_focus(rows, focus, total=None):
    out = []
    for row in rows:
        out.append([(l, b, c if (focus is None or l in focus) else c + " off", t) for (l, b, c, t) in row])
    ruler = '<div class="ruler mono"><span>0</span><span>8</span><span>16</span><span>24</span><span>31</span></div>'
    tot = f'<div class="htot mono">{total}</div>' if total else ""
    g = hdr_grid(out)
    if rows is HDR6: g = g.replace('Address</b><span class="mono">32 бит', 'Address</b><span class="mono">128 бит')
    return f'<div class="card hdrcard figh">{ruler}{g}{tot}</div>'
HDR6 = [
    [("Version", 4, "sky", "Версия протокола: 6 (0110)."), ("Traffic Class", 8, "sky", "Класс трафика: приоритет, как DSCP/ECN в IPv4."),
     ("Flow Label", 20, "lilac", "Метка потока: идентификатор сессии TCP или медиапотока UDP.")],
    [("Payload Length", 16, "lilac", "Длина полезной нагрузки в октетах."), ("Next Header", 8, "sky", "Номер протокола L4 или заголовка-расширения."),
     ("Hop Limit", 8, "mint", "Лимит переходов: каждый маршрутизатор уменьшает на 1.")],
    [("Source Address", 32, "pink big", "128-битный адрес отправителя.")],
    [("Destination Address", 32, "pink big", "128-битный адрес получателя.")],
]
FLOW = """<div class="flow">
  <div class="fl-b">Мой адрес <b class="mono">192.168.1.2/24</b><br>Отправляю пакет на <b class="mono">192.168.3.2</b></div>
  <div class="fl-a"></div>
  <div class="fl-b">Операция побитового «И» над адресами и маской</div>
  <div class="fl-a"></div>
  <div class="fl-d"><span>IP-адреса в одной сети?</span></div>
  <div class="fl-split">
    <div class="fl-br"><div class="fl-tag ok">ДА</div><div class="fl-b ok">Отправить ARP-запрос для получения MAC-адреса <b>получателя</b></div></div>
    <div class="fl-br"><div class="fl-tag no">НЕТ</div><div class="fl-b no">Отправить ARP-запрос для получения MAC-адреса <b>шлюза по умолчанию</b></div></div>
  </div>
</div>"""
REDRAW = {
 "Поля IPv4 1: схема": hdr_focus(HDR4, {"Version", "IHL", "DSCP", "ECN", "Total Length"}, "первые 32 бита из 160"),
 "Поля IPv4 2: схема": hdr_focus(HDR4, {"Identification", "Flags", "Fragment Offset"}, "биты 32–63 из 160"),
 "Поля IPv4 3: схема": hdr_focus(HDR4, {"TTL", "Protocol", "Header Checksum"}, "биты 64–95 из 160"),
 "Поля IPv4 4: схема": hdr_focus(HDR4, {"Source IP Address", "Destination IP Address", "Options"}, "адреса: 64 бита из 160 · опции: до 320 бит"),
 "Заголовок IPv6: схема": hdr_focus(HDR6, None, "фиксированный заголовок: 320 бит (40 байт)"),
 "Поля IPv6 1: схема": hdr_focus(HDR6, {"Version", "Traffic Class", "Flow Label"}, "первые 32 бита из 320"),
 "Поля IPv6 2: схема": hdr_focus(HDR6, {"Payload Length", "Next Header", "Hop Limit"}, "биты 32–63 из 320"),
 "Шлюз: схема": FLOW,
}
for k, it in enumerate(S):
    if it[0] in REDRAW:
        S[k] = (it[0], it[1], it[2], REDRAW[it[0]], "")

# персонажи
CHARS = {"Титул": ("wiz_happy", "r"), "Цели главы": ("star_blob", "r"), "Тренажёр: TTL": ("wiz_happy", "r"), "Тренажёр: маршрут": ("wiz_star", "r"),
         "Проверь себя": ("star_blob", "r")}
_cc = {}
for k, it in enumerate(S):
    if it[0] in CHARS:
        n, side = CHARS[it[0]]
        if n not in _cc: _cc[n] = _png(CH + n + ".png")
        S[k] = (it[0], it[1], it[2], it[3] + f'<img class="chr chr-{side}" src="{_cc[n]}" alt="" aria-hidden="true">', it[4])
BGIMG = _jpg(DL + "ChatGPT Image 5 сент. 2026 г., 19_47_48.png", 1920, 70)
ANIM_LOOP = {"Инкапсуляция", "Путь пакета целиком"}

render()
