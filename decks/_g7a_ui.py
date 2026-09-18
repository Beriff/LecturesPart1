# -*- coding: utf-8 -*-
# Компоненты «как на инфографике»: заголовки, панели, карточки, SVG-оборудование
from _g7a_lib import IC, esc, hexicon

# ---------------------------------------------------------------- SVG-оборудование (центр 0,0; ~±55)
def _slots(x, y0, w, n, dy):
    return "".join(f'<rect class="slot" x="{x}" y="{y0 + i * dy}" width="{w}" height="{dy - 5}"/><circle class="led" cx="{x + 5}" cy="{y0 + i * dy + (dy - 5) / 2}" r="1.8"/>'
                   f'<line class="sln" x1="{x + 11}" y1="{y0 + i * dy + (dy - 5) / 2}" x2="{x + w - 5}" y2="{y0 + i * dy + (dy - 5) / 2}"/>' for i in range(n))

def _screen(txt):
    if not txt:
        return ""
    if txt == ">_":
        return '<path class="scrt" d="M-24 -18l8 6-8 6 M-12 -4h14"/>'
    if txt == "folder":
        return '<path class="scri" d="M-16 -22h10l4 4h18v20h-32z"/>'
    if txt == "globe":
        return '<circle class="scri" cx="0" cy="-11" r="13"/><path class="scri" d="M-13 -11h26 M0 -24c6 6 6 20 0 26 M0 -24c-6 6-6 20 0 26"/>'
    if txt == "mail":
        return '<path class="scri" d="M-16 -22h32v22h-32z M-16 -22l16 12 16-12"/>'
    if txt == "page":
        return '<path class="scri" d="M-28 -28h56v8h-56z M-28 -16h24v20h-24z M2 -16h26 M2 -8h20 M2 0h26"/>'
    return f'<text class="scrx" x="0" y="-6" text-anchor="middle">{esc(txt)}</text>'

import json as _json, pathlib as _pl
REPO = _json.loads((_pl.Path(__file__).parent / "_g7a_svgrepo.json").read_text(encoding="utf-8"))
REPO_MAP = {"server": ("server", 1.0), "srv": ("server", 1.0), "dns": ("s2u", 1.0), "router": ("router", 1.05), "switch": ("switch", 1.15),
            "pc": ("pc", 1.0), "monitor": ("pc", 1.0), "fw": ("fw", 1.0), "cloud": ("cloud", 1.25), "db": ("db", 1.0)}
def sprite():
    return '<svg width="0" height="0" style="position:absolute" aria-hidden="true">' + ''.join(f'<symbol id="rp-{k}" viewBox="{vb}" overflow="visible">{b}</symbol>' for k, (vb, b) in REPO.items()) + '</svg>'
# CC0: Servers Isometric Icons, SVG Repo (svgrepo.com/collection/servers-isometric-icons)

def dev(kind, scr="", cls=""):
    k = kind
    if k in REPO_MAP:
        name, sc = REPO_MAP[k]
        vb, body = REPO[name]
        size = 116 * sc
        lab = ""
        if k == "dns":
            lab = '<text class="dvl2" x="0" y="50" text-anchor="middle">DNS</text>'
        if k == "cloud" and scr:
            lab = f'<text class="cldt" x="0" y="8" text-anchor="middle">{esc(scr)}</text>'
        return (f'<g class="dv rp {cls}"><use href="#rp-{name}" x="{-size / 2:.1f}" y="{-size / 2:.1f}" width="{size:.1f}" height="{size:.1f}"/>{lab}</g>')
    if k in ("server", "dns", "srv"):
        lab = '<text class="dvl" x="-6" y="44" text-anchor="middle">DNS</text>' if k == "dns" else ""
        body = ('<path class="dvt" d="M-26 -46L-8 -54H32L14 -46Z"/><path class="dvf" d="M-26 -46H14V50H-26Z"/><path class="dvs" d="M14 -46L32 -54V42L14 50Z"/>'
                + _slots(-21, -40, 30, 6, 13) + lab)
    elif k == "laptop" or k == "term":
        body = ('<path class="dvf" d="M-42 -40H42V16H-42Z"/><path class="scr" d="M-37 -35H37V11H-37Z"/>' + _screen(scr or (">_" if k == "term" else "")) +
                '<path class="dvt" d="M-48 16H48L56 28H-56Z"/><path class="sln" d="M-10 23H10"/>')
    elif k in ("pc", "monitor"):
        tower = '<path class="dvf" d="M34 -30H54V30H34Z"/><path class="sln" d="M38 -22H50 M38 -16H50"/><circle class="led" cx="44" cy="20" r="2"/>' if k == "pc" else ""
        body = ('<path class="dvf" d="M-44 -40H30V16H-44Z"/><path class="scr" d="M-39 -35H25V11H-39Z"/>' +
                f'<g transform="translate(-7 0)">{_screen(scr)}</g>' + '<path class="dvf" d="M-11 16H-3V28H-11Z"/><path class="dvt" d="M-26 28H12V33H-26Z"/>' + tower)
    elif k == "router":
        body = ('<path class="dvt" d="M-44 2L-34 -6H54L44 2Z"/><path class="dvf" d="M-44 2H44V22H-44Z"/><path class="dvs" d="M44 2L54 -6V14L44 22Z"/>'
                '<path class="ant" d="M-30 -2L-38 -42 M30 -2L38 -42"/>' + "".join(f'<circle class="led" cx="{-30 + i * 10}" cy="12" r="2"/>' for i in range(6)) +
                '<path class="wifi" d="M-8 -22a11 11 0 0 1 16 0 M-14 -29a20 20 0 0 1 28 0 M-2 -15h4"/>')
    elif k == "switch":
        body = ('<path class="dvt" d="M-52 -4L-42 -12H62L52 -4Z"/><path class="dvf" d="M-52 -4H52V16H-52Z"/><path class="dvs" d="M52 -4L62 -12V8L52 16Z"/>' +
                "".join(f'<rect class="port" x="{-46 + i * 11}" y="1" width="8" height="7"/>' for i in range(8)) + '<circle class="led" cx="-46" cy="12" r="1.6"/>')
    elif k == "cloud":
        body = '<path class="cld" d="M-34 22H36a18 18 0 0 0 2-36 26 26 0 0 0-48-6 20 20 0 0 0-24 42Z"/>'
        if scr:
            body += f'<text class="cldt" x="0" y="10" text-anchor="middle">{esc(scr)}</text>'
    elif k == "globe":
        body = ('<circle class="glb" r="40"/><ellipse class="gll" rx="16" ry="40"/><ellipse class="gll" rx="30" ry="40"/>'
                '<path class="gll" d="M-40 0H40 M-35 -20H35 M-35 20H35"/>')
    elif k == "fw":
        body = ('<path class="dvf" d="M-36 -34H36V34H-36Z"/><path class="sln" d="M-36 -17H36 M-36 0H36 M-36 17H36 M-12 -34V-17 M12 -17V0 M-12 0V17 M12 17V34"/>'
                '<path class="shd" d="M0 -18L16 -12V0C16 10 9 16 0 19-9 16-16 10-16 0V-12Z"/>')
    elif k == "phone":
        body = '<path class="dvf" d="M-14 -28H14V28H-14Z"/><path class="scr" d="M-10 -22H10V18H-10Z"/>'
    elif k == "hacker":
        body = ('<path class="hck" d="M-26 40C-26 10-18 -2 0 -2S26 10 26 40Z"/><path class="hck" d="M-18 -8C-18 -34-10 -44 0 -44S18 -34 18 -8C12 0-12 0-18 -8Z"/>'
                '<path class="hckf" d="M-10 -18H10 M-6 -14H6"/>')
    elif k == "ap":
        body = ('<path class="dvf" d="M-30 6H30V18H-30Z"/><path class="ant" d="M-20 6V-18 M20 6V-18"/>'
                '<path class="wifi" d="M-8 -14a11 11 0 0 1 16 0 M-14 -21a20 20 0 0 1 28 0"/>')
    else:
        body = f'<g transform="translate(-24 -24) scale(2)"><path class="sic" d="{IC[k]}"/></g>'
    return f'<g class="dv {cls}">{body}</g>'

def devsvg(kind, scr="", w="7rem", cls=""):
    return f'<svg class="dvs-in {cls}" viewBox="-62 -58 124 116" style="width:{w}" aria-hidden="true">{dev(kind, scr)}</svg>'

def devbox(kind, label, sub="", scr="", w="8rem", s=1):
    sb = f'<span class="dvbs">{sub}</span>' if sub else ""
    return f'<div class="dvb" data-s="{s}">{devsvg(kind, scr, w)}<span class="dvbl">{label}</span>{sb}</div>'

# ---------------------------------------------------------------- HTML-компоненты
def ih(w1, w2="", sub="", lead="", inline=False, big=False, s=0):
    t2 = f'{" " if inline else ""}<span class="o2{" in" if inline else ""}">{w2}</span>' if w2 else ""
    sb = f'<div class="ihs">{sub}</div>' if sub else ""
    ld = f'<p class="ihl">{lead}</p>' if lead else ""
    return f'<div class="ih{" big" if big else ""}"><h2>{w1}{t2}</h2>{sb}{ld}</div>'

def info(text, ic="info", s=1):
    return f'<div class="ibox" data-s="{s}">{hexicon(ic, "hx")}<div>{text}</div></div>'

def qt(text, s=1, ic=None):
    lead = hexicon(ic, "hx sm") if ic else '<span class="qm">&#8220;</span>'
    return f'<div class="qbar" data-s="{s}">{lead}<div>{text}</div></div>'

def pnl(title, body, cls="", s=1, style="", ic=None, sub=""):
    h = f'<div class="pnh">{hexicon(ic, "hx sm")}<h3>{title}</h3></div>' if ic else (f'<h3 class="uh">{title}</h3>' if title else "")
    sb = f'<div class="pns">{sub}</div>' if sub else ""
    st = f' style="{style}"' if style else ""
    ds = f' data-s="{s}"' if s else ""
    return f'<div class="card pn {cls}"{ds}{st}>{h}{sb}{body}</div>'

def pcd(num, title, sub, text, art, s=1, dl=0, cls=""):
    return (f'<div class="card pc {cls}" data-s="{s}" style="--dl:{dl}ms"><div class="pct"><span class="nb">{num:02d}</span><div><div class="nm">{title}</div>'
            f'<div class="full">{sub}</div></div></div><div class="pcb"><div class="d">{text}</div><div class="art">{art}</div></div></div>')

def tile(ic, title, text="", cls="", s=1, dl=0):
    t = f'<div class="tt">{text}</div>' if text else ""
    return f'<div class="tile {cls}" data-s="{s}" style="--dl:{dl}ms">{hexicon(ic, "hx")}<b>{title}</b>{t}</div>'

def lrow(ic, title, text="", s=1, dl=0, cls=""):
    t = f'<span>{text}</span>' if text else ""
    return f'<div class="lrow {cls}" data-s="{s}" style="--dl:{dl}ms">{hexicon(ic, "hx sm")}<div><b>{title}</b>{t}</div></div>'

def steps(items, s=1, cls=""):
    return f'<ol class="hsteps {cls}">' + "".join(f'<li data-s="{s}" style="--dl:{i * 90}ms"><span class="hn">{i + 1}</span><div>{t}</div></li>' for i, t in enumerate(items)) + '</ol>'

def bul(items, cls="", s=0):
    ds = f' data-s="{s}"' if s else ""
    return f'<ul class="dots {cls}"{ds}>' + "".join(f"<li>{t}</li>" for t in items) + "</ul>"

def irow(items, s=1):
    return '<div class="irow" data-s="%d">' % s + "".join(f'<div>{hexicon(ic, "hx")}<span>{t}</span></div>' for ic, t in items) + '</div>'

def G(cols, *kids, cls="", style=""):
    return f'<div class="G {cls}" style="--gc:{cols};{style}">' + "".join(kids) + '</div>'

def code(lines, s=1):
    return f'<pre class="code" data-s="{s}">' + "\n".join(lines) + '</pre>'

def kv(rows, cls=""):
    return f'<div class="kv {cls}">' + "".join(f'<span>{k}</span><b>{v}</b>' for k, v in rows) + '</div>'

def chip(t, cls=""):
    return f'<span class="chip {cls}">{t}</span>'

def ftile(ext, cls="", ic="file"):
    return f'<div class="ftile {cls}">{hexicon(ic, "hx sm") if False else ""}<svg viewBox="0 0 40 48" aria-hidden="true"><path class="fpg" d="M4 2h22l10 10v34H4z M26 2v10h10"/></svg><b>{ext}</b></div>'

def globe_deco(cls="gdeco"):
    lines = "".join(f'<ellipse class="gll" rx="{r}" ry="100"/>' for r in (25, 55, 80))
    lat = "".join(f'<ellipse class="gll" rx="{int((100 ** 2 - y ** 2) ** .5)}" ry="{int(abs(1) * 8)}" cy="{y}"/>' for y in (-70, -40, 0, 40, 70))
    dots = "".join(f'<circle class="gdot" cx="{x}" cy="{y}" r="2.4"/>' for x, y in ((-60, -30), (20, -60), (50, 20), (-20, 50), (70, -40), (-70, 30), (5, 5)))
    return f'<svg class="{cls}" viewBox="-110 -110 220 220" aria-hidden="true"><circle class="glb" r="100"/>{lines}{lat}{dots}</svg>'

CSS2 = r"""
/* ===== стиль инфографик ===== */
.ih{margin-bottom:.9rem}
.ih h2{font-size:3.6rem;line-height:.95;letter-spacing:.005em}
.ih.big h2{font-size:5rem}
.ih h2 .o2.in{display:inline}
.ihs{font-family:var(--hf);font-size:1rem;letter-spacing:.32em;text-transform:uppercase;color:var(--cyan);margin-top:.5rem}
.ihl{font-size:1.02rem;line-height:1.5;color:#d3f0ea;margin-top:.7rem;max-width:56ch}
.sh{display:none}
.ibox{display:flex;gap:1rem;align-items:center;padding:.9rem 1.2rem;border:1px solid var(--edge);background:rgba(6,26,24,.8);clip-path:polygon(18px 0,100% 0,100% calc(100% - 18px),calc(100% - 18px) 100%,0 100%,0 18px);font-size:.95rem;line-height:1.5;color:#d3f0ea;box-shadow:inset 0 0 30px rgba(46,230,200,.06)}
.ibox b{color:var(--cyan)}
.qbar{display:flex;gap:1rem;align-items:center;padding:.8rem 1.3rem;border:1px solid var(--edge);background:rgba(6,26,24,.8);clip-path:polygon(18px 0,100% 0,100% calc(100% - 18px),calc(100% - 18px) 100%,0 100%,0 18px);font-size:1rem;line-height:1.45;color:#eafffb}
.qbar .qm{font-family:var(--hf);font-size:3rem;line-height:.6;color:var(--cyan);text-shadow:0 0 14px rgba(46,230,200,.6);padding-top:.5rem}
.G{display:grid;grid-template-columns:var(--gc);gap:.8rem;align-items:stretch}
.G.ac{align-items:center}.G.as{align-items:start}
.card.pn{padding:.9rem 1.1rem;background:linear-gradient(180deg,rgba(10,40,38,.75),rgba(5,20,19,.85))}
.card.pn::before{display:none}
.card.pn.red{border-color:rgba(255,92,110,.6);background:linear-gradient(180deg,rgba(60,14,20,.6),rgba(20,6,8,.8))}.card.pn.red h3{color:var(--red)}
.card.pn.blue{border-color:rgba(74,168,255,.55);background:linear-gradient(180deg,rgba(10,30,60,.6),rgba(5,14,26,.8))}.card.pn.blue h3{color:var(--blue)}
.card.pn.vio{border-color:rgba(155,123,255,.55);background:linear-gradient(180deg,rgba(30,20,60,.6),rgba(12,8,26,.8))}.card.pn.vio h3{color:var(--violet)}
.card.pn.amb{border-color:rgba(245,184,61,.55);background:linear-gradient(180deg,rgba(50,36,10,.55),rgba(20,14,4,.8))}.card.pn.amb h3{color:var(--amber)}
.card.pn.grn h3{color:var(--green)}
h3.uh{font-size:1.25rem;color:#fff;letter-spacing:.02em;margin-bottom:.8rem;position:relative;padding-bottom:.45rem}
h3.uh::after{content:"";position:absolute;left:0;bottom:0;width:2.2rem;height:3px;background:var(--cyan);box-shadow:0 0 8px var(--cyan)}
.pns{font-size:.9rem;color:var(--dim);margin:-.4rem 0 .6rem}
.pn .pnh h3{color:#fff}
/* карточки протоколов */
.pc{padding:.8rem .95rem;background:linear-gradient(180deg,rgba(10,42,40,.75),rgba(4,18,17,.9))}
.pc::before{display:none}
.pct{display:flex;gap:.8rem;align-items:center;margin-bottom:.4rem}
.nb{flex:none;display:grid;place-items:center;width:2.7rem;height:2.4rem;background:var(--cyan);color:#03120f;font-family:var(--hf);font-size:1.25rem;clip-path:polygon(22% 0,78% 0,100% 50%,78% 100%,22% 100%,0 50%);box-shadow:0 0 14px rgba(46,230,200,.6)}
.pct .nm{font-family:var(--hf);font-size:1.5rem;line-height:1;color:#fff}
.pct .full{font-size:.82rem;color:var(--cyan);margin-top:.15rem}
.pcb{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:.6rem;align-items:center}
.pcb .d{font-size:.86rem;line-height:1.42;color:#d3f0ea}
.art{display:flex;align-items:center;justify-content:center}
.art .bigic{width:4.2rem;height:4.2rem;fill:none;stroke:var(--ice);stroke-width:1.2;stroke-linecap:round;stroke-linejoin:round;filter:drop-shadow(0 0 8px rgba(46,230,200,.7))}
.art .tag{font-family:var(--hf);font-size:.8rem;border:1px solid var(--cyan);padding:.05rem .35rem;color:#fff;background:#03120f;margin-left:-1.2rem;align-self:flex-end}
/* плитки, строки */
.tile{display:flex;flex-direction:column;align-items:center;text-align:center;gap:.35rem;padding:.8rem .6rem;border:1px solid var(--edge);background:rgba(8,32,30,.6);clip-path:var(--cut6)}
.tile b{font-family:var(--hf);font-size:1rem;text-transform:uppercase;color:#fff;letter-spacing:.02em;line-height:1.15}
.tile .tt{font-size:.8rem;line-height:1.35;color:var(--dim)}
.tile.red{border-color:rgba(255,92,110,.55);background:rgba(60,14,20,.45)}.tile.red .hxf{stroke:var(--red)}.tile.red .hxi{stroke:var(--red)}
.tile.blue{border-color:rgba(74,168,255,.55);background:rgba(10,30,60,.5)}.tile.blue .hxf{stroke:var(--blue)}.tile.blue .hxi{stroke:var(--blue)}
.tile.vio{border-color:rgba(155,123,255,.55);background:rgba(30,20,60,.5)}.tile.vio .hxf{stroke:var(--violet)}.tile.vio .hxi{stroke:var(--violet)}
.tile.amb{border-color:rgba(245,184,61,.55);background:rgba(50,36,10,.45)}.tile.amb .hxf{stroke:var(--amber)}.tile.amb .hxi{stroke:var(--amber)}
.tile.plain{border:0;background:none;clip-path:none}
.lrow{display:flex;gap:.8rem;align-items:center;padding:.45rem .6rem;border:1px solid rgba(45,230,200,.2);background:rgba(8,32,30,.5);clip-path:var(--cut6)}
.lrow b{display:block;font-size:.95rem;color:#fff}.lrow span{display:block;font-size:.82rem;color:var(--dim);line-height:1.35}
.lrow.hot{border-color:var(--cyan);box-shadow:0 0 14px rgba(46,230,200,.3)}
.lst{display:flex;flex-direction:column;gap:.45rem}
.hsteps{list-style:none;display:flex;flex-direction:column;gap:.55rem}
.hsteps li{display:flex;gap:.8rem;align-items:flex-start;font-size:.9rem;line-height:1.4;color:#d3f0ea}
.hn{flex:none;display:grid;place-items:center;width:2rem;height:1.8rem;background:var(--cyan);color:#03120f;font-family:var(--hf);font-size:1rem;clip-path:polygon(22% 0,78% 0,100% 50%,78% 100%,22% 100%,0 50%)}
.hsteps.blue .hn{background:var(--blue)}
.dots{list-style:none;display:flex;flex-direction:column;gap:.4rem}
.dots li{position:relative;padding-left:1.1rem;font-size:.9rem;line-height:1.42;color:#d3f0ea}
.dots li::before{content:"";position:absolute;left:0;top:.45em;width:.5em;height:.5em;border-radius:50%;background:var(--cyan);box-shadow:0 0 6px var(--cyan)}
.irow{display:flex;flex-wrap:wrap;justify-content:space-around;gap:.8rem;padding:.6rem .8rem;border:1px solid rgba(45,230,200,.25);background:rgba(8,32,30,.45);clip-path:var(--cut6)}
.irow>div{display:flex;flex-direction:column;align-items:center;gap:.3rem;font-family:var(--hf);font-size:.8rem;text-transform:uppercase;color:#dff;text-align:center;max-width:7rem}
.irow.h>div{flex-direction:row;max-width:none;gap:.6rem}
/* устройства */
.dvs-in{display:block;height:auto;overflow:visible}
.dv{filter:drop-shadow(0 0 7px rgba(46,230,200,.45))}
.dvf{fill:rgba(12,56,58,.85);stroke:var(--cyan);stroke-width:1.5;stroke-linejoin:round}
.dvt{fill:rgba(46,230,200,.28);stroke:var(--cyan);stroke-width:1.3;stroke-linejoin:round}
.dvs{fill:rgba(6,30,32,.95);stroke:var(--teal-dim);stroke-width:1.3;stroke-linejoin:round}
.scr{fill:#05333a;stroke:rgba(126,245,226,.7);stroke-width:1}
.scrt,.scri{fill:none;stroke:var(--ice);stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.scrx{font-family:var(--hf);font-size:15px;fill:var(--ice)}
.slot{fill:rgba(46,230,200,.1);stroke:rgba(46,230,200,.45);stroke-width:.8}
.sln{stroke:rgba(126,245,226,.5);stroke-width:1.2;fill:none}
.led{fill:var(--cyan)}
.port{fill:#031a1a;stroke:var(--cyan);stroke-width:.8}
.ant{stroke:var(--cyan);stroke-width:3;stroke-linecap:round;fill:none}
.wifi{fill:none;stroke:var(--ice);stroke-width:2.2;stroke-linecap:round}
.cld{fill:rgba(12,60,60,.75);stroke:var(--cyan);stroke-width:1.8}
.dg .cldt,.cldt{font-family:var(--hf);font-size:15px;fill:#fff}
.glb{fill:rgba(12,60,60,.45);stroke:var(--cyan);stroke-width:1.4}.gll{fill:none;stroke:rgba(46,230,200,.4);stroke-width:1}
.gdot{fill:var(--ice)}
.shd{fill:rgba(46,230,200,.3);stroke:var(--ice);stroke-width:1.5}
.hck{fill:#140b10;stroke:var(--red);stroke-width:1.6}.hckf{stroke:var(--red);stroke-width:2}
.dv.red .dvf,.dv.red .dvt,.dv.red .dvs{stroke:var(--red)}.dv.red{filter:drop-shadow(0 0 7px rgba(255,92,110,.6))}
.dv.blue .dvf,.dv.blue .dvt{stroke:var(--blue)}.dv.blue{filter:drop-shadow(0 0 7px rgba(74,168,255,.6))}
.dvl{font-family:var(--hf);font-size:12px;fill:var(--ice)}
.dvb{display:flex;flex-direction:column;align-items:center;gap:.35rem}
.dvbl{font-family:var(--hf);font-size:1.05rem;color:#fff;padding:.3rem .9rem;border:1px solid var(--edge);background:rgba(4,20,19,.85);clip-path:var(--cut6);text-align:center}
.dvbs{font-size:.78rem;color:var(--dim);text-align:center;font-family:var(--mono)}
.nd .dv{transition:filter .3s}.nd.hot .dv{filter:drop-shadow(0 0 16px rgba(126,245,226,.95))}.nd.bad .dv{filter:drop-shadow(0 0 14px rgba(255,92,110,.95))}
.nd.bad .dvf,.nd.bad .dvt{stroke:var(--red)}
.nlb{fill:rgba(4,20,19,.9);stroke:var(--edge);stroke-width:1}
.gdeco{position:absolute;pointer-events:none;opacity:.55;filter:drop-shadow(0 0 20px rgba(46,230,200,.4))}
/* прочее */
.code{font-family:var(--mono);font-size:.82rem;line-height:1.6;padding:.8rem 1rem;border:1px solid var(--edge);background:#021110;color:#cfe;white-space:pre-wrap;clip-path:var(--cut6)}
.code .k{color:var(--cyan)}.code .v{color:var(--amber)}.code .r{color:var(--red)}.code .b{color:var(--blue)}.code .g{color:var(--green)}.code .d{color:var(--dim)}
.kv{display:grid;grid-template-columns:auto 1fr;gap:.3rem .9rem;font-size:.86rem}.kv span{color:var(--dim)}.kv b{font-family:var(--mono);color:#eafffb;font-weight:500}
.chip{display:inline-block;font-family:var(--mono);font-size:.85rem;padding:.25rem .6rem;border:1px solid var(--cyan);color:#eafffb;background:rgba(46,230,200,.08);clip-path:var(--cut6)}
.chip.amb{border-color:var(--amber);color:var(--amber)}.chip.vio{border-color:var(--violet);color:var(--violet)}.chip.red{border-color:var(--red);color:var(--red)}.chip.blue{border-color:var(--blue);color:var(--blue)}
.ftile{position:relative;width:3.4rem;display:inline-flex;flex-direction:column;align-items:center}
.ftile svg{width:3.2rem;height:3.8rem}.fpg{fill:rgba(12,56,58,.8);stroke:var(--cyan);stroke-width:1.6;stroke-linejoin:round}
.ftile b{position:absolute;bottom:.5rem;font-family:var(--hf);font-size:.95rem;color:#fff}
.ftile.blue .fpg{stroke:var(--blue);fill:rgba(10,30,60,.8)}
.frow{display:flex;gap:1rem;justify-content:center;flex-wrap:wrap}
.stack3d{display:flex;flex-direction:column;gap:6px;perspective:900px}
.slab{display:flex;align-items:center;gap:.9rem;padding:.55rem 1rem;border:1px solid rgba(45,230,200,.45);background:linear-gradient(90deg,rgba(46,230,200,.18),rgba(8,40,40,.6));transform:rotateX(14deg) rotateY(-10deg);box-shadow:0 6px 0 -1px rgba(46,230,200,.25),0 0 18px rgba(46,230,200,.12);font-size:1rem;color:#eafffb;transition:box-shadow .4s,background .4s,transform .4s}
.slab .sn{font-family:var(--hf);font-size:1.25rem;width:1.8rem;height:1.8rem;display:grid;place-items:center;background:rgba(46,230,200,.25);border:1px solid var(--cyan)}
.slab.hi,.slab.in.hi{background:linear-gradient(90deg,rgba(46,230,200,.55),rgba(20,90,86,.7));box-shadow:0 6px 0 -1px rgba(46,230,200,.6),0 0 26px rgba(46,230,200,.55);color:#fff}
.slab.dim{opacity:.55}
.urlbar{display:flex;align-items:center;gap:.6rem;padding:.45rem .8rem;border:1px solid var(--edge);background:#031716;font-family:var(--mono);font-size:.9rem;color:#dff;clip-path:var(--cut6)}
.urlbar i{width:.55rem;height:.55rem;border-radius:50%;background:var(--dim);display:inline-block}
.urlbar i+i{background:var(--amber)}.urlbar i+i+i{background:var(--cyan)}
.lk2{stroke:var(--cyan);stroke-width:2;stroke-dasharray:4 5;fill:none;opacity:.7}
.relbox{position:relative}
.mini{display:block;width:100%;height:auto}
.mini text{font-family:var(--f);fill:#eafffb;font-size:13px}
.mini .ml2{font-family:var(--mono);font-size:12px;font-weight:700}
.addr{display:grid;grid-template-columns:1fr 1fr;gap:.5rem;margin-top:.35rem}
.addr>div{border:1px solid rgba(45,230,200,.3);background:rgba(3,20,19,.8);padding:.35rem .55rem;font-size:.76rem;color:var(--dim);display:grid;grid-template-columns:1fr 1fr;gap:.1rem .6rem;clip-path:var(--cut6)}
.addr b{font-family:var(--mono);color:#eafffb;font-weight:500;font-size:.8rem}
.msg{position:relative;padding:.2rem 0 .5rem}
.msg .mh{display:flex;align-items:center;gap:.6rem;font-family:var(--hf);font-size:1.25rem;color:#fff}
.msg .mh small{font-family:var(--f);font-size:.78rem;color:var(--dim);border:1px solid rgba(45,230,200,.3);padding:.1rem .5rem}
.mline{position:relative;height:4px;margin:.35rem 0;border-radius:0}
.mline::before{content:"";position:absolute;inset:0;background:currentColor;box-shadow:0 0 10px currentColor;transform:scaleX(0);transition:transform .7s linear;transform-origin:left}
.mline.l::before{transform-origin:right}
.mline::after{content:"";position:absolute;top:-7px;width:0;height:0;border-top:9px solid transparent;border-bottom:9px solid transparent;opacity:0;transition:opacity .15s .65s}
.mline.r::after{right:-4px;border-left:16px solid currentColor}.mline.l::after{left:-4px;border-right:16px solid currentColor}
.in .mline::before,.mline.in::before{transform:scaleX(1)}.in .mline::after{opacity:1}
.c-red{color:var(--red)}.c-blue{color:var(--blue)}.c-teal{color:var(--cyan)}.c-amb{color:var(--amber)}.c-vio{color:var(--violet)}.c-grn{color:var(--green)}
.col-dev{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.5rem;border:1px solid rgba(45,230,200,.25);background:rgba(6,26,24,.55);padding:1rem .5rem;clip-path:var(--cut)}
.srow{display:grid;grid-template-columns:auto minmax(0,1fr) minmax(0,1.05fr);gap:.8rem;align-items:center;padding:.35rem 0}
.srow .st b{display:block;font-family:var(--hf);font-size:1.08rem;color:#fff}.srow .st span{font-size:.8rem;color:var(--dim);line-height:1.35;display:block}
.srow .ar{position:relative;text-align:center;font-family:var(--hf);font-size:.95rem}
.srow .ar .mline{margin-top:.3rem}
.ports{display:flex;flex-direction:column;gap:.45rem}
.ports>div{display:flex;gap:.8rem;align-items:center;font-size:.86rem;color:#d3f0ea}
.ports .pb{flex:none;display:grid;place-items:center;width:3rem;height:2.2rem;border:1.5px solid var(--cyan);font-family:var(--hf);font-size:1.25rem;color:var(--cyan);background:rgba(46,230,200,.08)}
.ports .pb.blue{border-color:var(--blue);color:var(--blue);background:rgba(74,168,255,.08)}
.bigtitle{font-family:var(--hf);text-transform:uppercase}
.tbl2{width:100%;border-collapse:collapse;font-size:.86rem}
.tbl2 th{font-family:var(--hf);font-weight:700;color:var(--cyan);text-align:left;padding:.35rem .6rem;border-bottom:1px solid var(--edge);background:rgba(46,230,200,.08)}
.tbl2 td{padding:.32rem .6rem;border-bottom:1px solid rgba(45,230,200,.14);color:#d3f0ea}.tbl2 td:first-child{color:#fff;font-family:var(--mono)}
.ws{font-family:var(--mono);font-size:.8rem;line-height:1.55;background:#fbfdfd0a;border:1px solid var(--edge);padding:.7rem .9rem;color:#cfe;clip-path:var(--cut6);white-space:pre}
.ws .hl{background:rgba(46,230,200,.18);color:#fff;outline:1px solid var(--cyan);font-weight:400}
.ws .rd{outline:1.5px solid var(--red);color:#fff}
.ws .t{color:var(--dim)}
.pie{width:6rem;height:6rem;border-radius:50%;background:conic-gradient(var(--cyan) 0 62%,#0f4a46 62% 100%);box-shadow:0 0 18px rgba(46,230,200,.4);flex:none}
.ipc{display:flex;flex-direction:column;align-items:center;gap:.2rem;padding:.45rem .3rem;border:1px dashed rgba(45,230,200,.5);font-family:var(--mono);font-size:.72rem;color:#dff;background:rgba(8,32,30,.5)}
.ipc.off{border-color:rgba(255,92,110,.7);color:var(--red);background:rgba(60,14,20,.35)}
.form{display:grid;grid-template-columns:auto 1fr;gap:.45rem .8rem;align-items:center;font-size:.9rem}
.form span{color:#dff}.form b{font-family:var(--mono);font-weight:500;border:1px solid var(--edge);padding:.25rem .6rem;background:#031716;letter-spacing:.2em}
.alert{display:inline-flex;gap:.6rem;align-items:center;padding:.5rem .9rem;border:1px solid var(--red);background:rgba(60,14,20,.6);color:#fff;font-size:.9rem;clip-path:var(--cut6)}
.qtag{display:inline-block;font-size:.8rem;border:1px solid var(--edge);padding:.15rem .5rem;color:#dff;background:#031716;transform:rotate(-8deg)}
.mon{display:grid;grid-template-columns:repeat(5,1fr);gap:.4rem}
.tl{position:relative;height:3.2rem;margin:.4rem 1rem}
.tl .ln{position:absolute;left:0;right:0;top:1rem;height:3px;background:linear-gradient(90deg,var(--cyan),var(--green) 50%,var(--amber) 80%,var(--red) 95%,var(--blue))}
.tl .pt{position:absolute;top:.55rem;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;font-size:.8rem;color:var(--dim);text-align:center}
.tl .pt i{width:.95rem;height:.95rem;border-radius:50%;background:currentColor;box-shadow:0 0 10px currentColor;margin-bottom:.3rem}
.tl .mk{position:absolute;top:.3rem;width:1.4rem;height:1.4rem;margin-left:-.7rem;background:#fff;clip-path:var(--hex);box-shadow:0 0 12px #fff;transition:left 1.2s var(--ez)}
.clockbig{width:100%;max-width:17rem;margin:auto;display:block}
.hand{stroke:var(--ice);stroke-linecap:round;transform-origin:0 0;transition:transform 2.4s cubic-bezier(.3,.1,.2,1)}
.in .hand.h1{transform:rotate(120deg)}.in .hand.h2{transform:rotate(300deg)}
.tree text{font-family:var(--hf);font-size:18px;fill:#fff}
.tnode{fill:rgba(46,230,200,.18);stroke:var(--cyan);stroke-width:1.5}
.tlink{stroke:var(--cyan);stroke-width:2;fill:none;opacity:.8}
.bits2{display:grid;gap:3px}
@media (max-width:1279px){.G{grid-template-columns:repeat(2,minmax(0,1fr))!important}.G>*{grid-column:auto!important;grid-row:auto!important}}
@media (max-width:767px){.G{grid-template-columns:minmax(0,1fr)!important}.ih h2,.ih.big h2{font-size:min(2.2rem,30px)}.srow{grid-template-columns:auto 1fr}.srow .ar{grid-column:span 2}}
"""
