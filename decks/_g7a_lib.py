# -*- coding: utf-8 -*-
# Библиотека сцен для decks/glava7-application.html (Глава 7. Уровень приложений)
import math, html

SCENES = {}

def esc(s):
    return html.escape(str(s), quote=False)

def track(n, keys, default):
    out, v = [], default
    for i in range(n + 1):
        if i in keys: v = keys[i]
        out.append(v)
    return out

def scene(name, n, els, waits=None, wdef=1100):
    spec = {"n": n, "w": [(waits or {}).get(i, wdef) for i in range(n + 1)], "e": {}}
    for eid, tr in els.items():
        e = {}
        if "p" in tr: e["p"] = track(n, tr["p"], (0, 0))
        if "o" in tr: e["o"] = track(n, tr["o"], 1)
        if "c" in tr: e["c"] = track(n, tr["c"], "")
        if "t" in tr: e["t"] = track(n, tr["t"], "")
        spec["e"][eid] = e
    SCENES[name] = spec
    return f'data-scene="{name}"'

# ---------------------------------------------------------------- иконки (сетка 24×24, контур)
IC = {
    "pc": "M3 4h18v12H3z M8 20h8 M12 16v4",
    "laptop": "M5 5h14v10H5z M2 19h20l-2-4H4z",
    "server": "M5 3h14v6H5z M5 9h14v6H5z M5 15h14v6H5z M8 6h.01 M8 12h.01 M8 18h.01 M12 6h4 M12 12h4 M12 18h4",
    "router": "M3 13h18v7H3z M7 16.5h.01 M10.5 16.5h.01 M8.5 9.5a5 5 0 0 1 7 0 M6 7a8.5 8.5 0 0 1 12 0 M12 13v-1",
    "switch": "M2 8h20v8H2z M5 12h2 M9 12h2 M13 12h2 M17 12h2",
    "cloud": "M7 18h10a4 4 0 0 0 .5-7.97A6 6 0 0 0 6 10.5 3.75 3.75 0 0 0 7 18z",
    "globe": "M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18z M3 12h18 M12 3c3.2 3 3.2 15 0 18 M12 3c-3.2 3-3.2 15 0 18",
    "dns": "M4 4h16v7H4z M4 13h16v7H4z M7 7.5h.01 M7 16.5h.01 M11 7.5h6 M11 16.5h6",
    "mail": "M3 6h18v12H3z M3 6l9 7 9-7",
    "clock": "M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18z M12 7v5l3.5 2",
    "atom": "M12 11v2 M12 3c-2 0-3.2 4-3.2 9s1.2 9 3.2 9 3.2-4 3.2-9-1.2-9-3.2-9z M4.2 7.5c-1 1.8 1.8 5.2 6.2 7.7s8.4 3.3 9.4 1.5-1.8-5.2-6.2-7.7-8.4-3.3-9.4-1.5z",
    "sat": "M9 9l6 6 M8.5 12.5l4-4 3 3-4 4z M3 8l3-3 4 4-3 3z M14 19l3-3 4 4-3 3z M17 3a4 4 0 0 1 4 4",
    "lock": "M6 11h12v9H6z M9 11V8a3 3 0 0 1 6 0v3 M12 15v2",
    "folder": "M3 6h6l2 2h10v11H3z",
    "printer": "M7 9V3h10v6 M4 9h16v8H4z M7 14h10v7H7z",
    "term": "M3 4h18v16H3z M7 9l3 3-3 3 M12 15h5",
    "file": "M6 3h9l4 4v14H6z M15 3v4h4 M9 12h6 M9 16h6",
    "shield": "M12 3l8 3v6c0 5-3.6 8-8 9-4.4-1-8-4-8-9V6z M9 12l2 2 4-4",
    "fw": "M3 5h18v14H3z M3 10h18 M3 15h18 M9 5v5 M15 10v5 M9 15v4",
    "video": "M3 6h13v12H3z M16 10l5-3v10l-5-3z",
    "gear": "M12 9a3 3 0 1 0 0 6a3 3 0 1 0 0-6z M12 2v3 M12 19v3 M2 12h3 M19 12h3 M4.9 4.9l2.1 2.1 M17 17l2.1 2.1 M4.9 19.1L7 17 M17 7l2.1-2.1",
    "key": "M7.5 11a3.5 3.5 0 1 0 0 7a3.5 3.5 0 1 0 0-7z M10 12.5L20 3 M16 7l2.5 2.5 M13.5 9.5l2 2",
    "desk": "M3 4h18v12H3z M8 20h8 M12 16v4 M7 8h6 M7 11h10",
    "user": "M12 4a4 4 0 1 0 0 8a4 4 0 1 0 0-8z M4 21a8 8 0 0 1 16 0",
    "hacker": "M12 3a5 5 0 0 0-5 5v3h10V8a5 5 0 0 0-5-5z M4 21a8 8 0 0 1 16 0 M9 8h6",
    "book": "M4 4h7a2 2 0 0 1 2 2v14a2 2 0 0 0-2-2H4z M20 4h-7 M20 4v14h-7",
    "db": "M12 3c4.4 0 8 1.3 8 3s-3.6 3-8 3-8-1.3-8-3 3.6-3 8-3z M4 6v12c0 1.7 3.6 3 8 3s8-1.3 8-3V6 M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3",
    "radio": "M12 12v9 M8 21h8 M8.5 8.5a5 5 0 0 1 7 0 M5.6 5.6a9 9 0 0 1 12.8 0 M12 12h.01",
    "check": "M5 12l4 4 10-10",
    "cross": "M6 6l12 12 M18 6L6 18",
    "info": "M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18z M12 11v6 M12 7.5h.01",
    "warn": "M12 3l10 18H2z M12 10v5 M12 18h.01",
    "target": "M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18z M12 8a4 4 0 1 0 0 8a4 4 0 1 0 0-8z",
    "layers": "M12 3l9 5-9 5-9-5z M3 13l9 5 9-5 M3 17.5l9 5 9-5",
    "link": "M10 14a4 4 0 0 0 5.66 0l3-3a4 4 0 0 0-5.66-5.66l-1 1 M14 10a4 4 0 0 0-5.66 0l-3 3a4 4 0 0 0 5.66 5.66l1-1",
    "hand": "M7 11V5a2 2 0 0 1 4 0v5 M11 9a2 2 0 0 1 4 0v2 M15 10a2 2 0 0 1 4 0v4a7 7 0 0 1-7 7h-1a6 6 0 0 1-5-3l-2.5-4a1.8 1.8 0 0 1 3-2L7 14",
    "img": "M3 5h18v14H3z M3 16l5-5 4 4 3-3 6 6 M15 9h.01",
    "zip": "M6 3h12v18H6z M11 3v2h2 M11 7h2 M11 9v2h2 M11 13h2v3h-2z",
    "hourglass": "M6 3h12 M6 21h12 M7 3c0 5 10 5 10 9s-10 4-10 9 M17 3c0 5-10 5-10 9s10 4 10 9",
}

def icon(name, size=24, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" width="{size}" height="{size}" aria-hidden="true"><path d="{IC[name]}"/></svg>'

def hexicon(name, cls="hx"):
    return (f'<span class="{cls}"><svg viewBox="0 0 48 48" aria-hidden="true"><path class="hxf" d="M14 3h20l11 21-11 21H14L3 24z"/>'
            f'<g transform="translate(12 12)"><path class="hxi" d="{IC[name]}"/></g></svg></span>')

def svgicon(name, x, y, s=1.6, cls="sic"):
    return f'<path class="{cls}" transform="translate({x - 12 * s:.1f} {y - 12 * s:.1f}) scale({s})" d="{IC[name]}"/>'

HEXP = "M{0} {1}h{2}l{3} {4}-{3} {4}h-{2}l-{3}-{4}z"

def hexnode(x, y, r=40):
    w = r * 0.5
    return f'<path class="nhx" d="M{x - w:.1f} {y - r * 0.87:.1f}h{r:.1f}l{w:.1f} {r * 0.87:.1f}-{w:.1f} {r * 0.87:.1f}h-{r:.1f}l-{w:.1f}-{r * 0.87:.1f}z"/>'

# ---------------------------------------------------------------- топология с пакетами
COLS = {"blue": "wb", "amber": "wa", "violet": "wv", "teal": "wt", "red": "wr", "green": "wg", "ice": "wi"}

DEVK = {"laptop", "server", "dns", "pc", "router", "switch", "cloud", "globe", "fw", "hacker", "term", "phone", "ap", "monitor"}

def _node(nid, n):
    from _g7a_ui import dev
    x, y = n["x"], n["y"]
    r = n.get("r", 40)
    lines = n["label"].split("\n")
    if n["ic"] in DEVK:
        shape = f'<g transform="translate({x} {y}) scale({r / 44:.3f})">{dev(n["ic"], n.get("scr", ""), n.get("cls", ""))}</g>'
    else:
        shape = hexnode(x, y, r) + svgicon(n["ic"], x, y, r / 25)
    w = max(len(t) for t in lines) * 9.2 + 26
    ly = y + r + 14
    box = f'<path class="nlb" d="M{x - w / 2 + 6:.1f} {ly:.1f}H{x + w / 2:.1f}V{ly + 22 * len(lines) + 4 - 6:.1f}L{x + w / 2 - 6:.1f} {ly + 22 * len(lines) + 4:.1f}H{x - w / 2:.1f}V{ly + 6:.1f}Z"/>'
    lab = "".join(f'<tspan x="{x}" dy="{0 if i == 0 else 22}">{esc(t)}</tspan>' for i, t in enumerate(lines))
    sub = n.get("sub", "")
    s = f'<text class="nsub" x="{x}" y="{ly + 22 * len(lines) + 22}" text-anchor="middle">{esc(sub)}</text>' if sub else ""
    return (f'<g class="nd" data-id="n_{nid}">{shape}{box}'
            f'<text class="nlab" x="{x}" y="{ly + 18}" text-anchor="middle">{lab}</text>{s}</g>'
            f'<g class="tagg" data-id="gb_{nid}"><text class="tag" data-id="g_{nid}" x="{x}" y="{y - r - 14}" text-anchor="middle"></text></g>')

def _pt(nodes, a, b, off):
    ax, ay, bx, by = nodes[a]["x"], nodes[a]["y"], nodes[b]["x"], nodes[b]["y"]
    L = math.hypot(bx - ax, by - ay) or 1
    ux, uy = (bx - ax) / L, (by - ay) / L
    ra, rb = nodes[a].get("r", 40) + 8, nodes[b].get("r", 40) + 12
    nx, ny = -uy * off, ux * off
    return (ax + ux * ra + nx, ay + uy * ra + ny, bx - ux * rb + nx, by - uy * rb + ny)

def ahead(x, y, ang, cls, eid=None):
    a = math.radians(ang)
    p = [(x + 6 * math.cos(a), y + 6 * math.sin(a)),
         (x - 10 * math.cos(a) + 7 * math.sin(a), y - 10 * math.sin(a) - 7 * math.cos(a)),
         (x - 10 * math.cos(a) - 7 * math.sin(a), y - 10 * math.sin(a) + 7 * math.cos(a))]
    return f'<polygon class="ah {cls}" points="{" ".join(f"{u:.1f},{v:.1f}" for u, v in p)}"/>'

def arrow(eid, x1, y1, x2, y2, col, dash=False, curve=0):
    cls = COLS.get(col, col)
    if curve:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - curve
        d = f"M{x1:.1f} {y1:.1f}Q{mx:.1f} {my:.1f} {x2:.1f} {y2:.1f}"
        ang = math.degrees(math.atan2(y2 - my, x2 - mx))
    else:
        d = f"M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}"
        ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    dc = " dsh" if dash else ""
    return f'<g class="arw" data-id="{eid}"><path class="dr {cls}{dc}" pathLength="1" d="{d}"/>{ahead(x2, y2, ang, cls)}</g>'

def fields_panel(prefix, fields, title="Заголовок пакета"):
    rows = "".join(f'<div class="fr"><span class="fk">{esc(k)}</span><span class="fv mono" data-id="{prefix}f{i}"></span></div>' for i, k in enumerate(fields))
    return f'<div class="fpan"><div class="fpt">{esc(title)}</div>{rows}</div>'

def flow(name, vb, nodes, steps, links=(), fields=(), ftitle="Заголовок пакета", extra="", wdef=2300, curve=None, pre=""):
    """Топология: узлы-шестиугольники, пакеты летят по шагам, справа панель полей заголовка, снизу подпись."""
    n = len(steps)
    els, body, pk = {}, [], []
    body.append("".join(f'<line class="lk" x1="{nodes[a]["x"]}" y1="{nodes[a]["y"]}" x2="{nodes[b]["x"]}" y2="{nodes[b]["y"]}"/>' for a, b in links))
    body.append(extra)
    body.append("".join(_node(k, v) for k, v in nodes.items()))
    hot = {k: {0: ""} for k in nodes}
    tags = {k: {0: ""} for k in nodes}
    fl = {f"{name}f{i}": {0: ""} for i in range(len(fields))}
    cap = {0: ""}
    sn = {0: ""}
    pairs = {}
    for k, st in enumerate(steps, start=1):
        cap[k] = st.get("cap", "")
        sn[k] = f"{k:02d} / {n:02d}"
        for nid in nodes:
            hot[nid][k] = ""
            tags[nid][k] = ""
        for h in st.get("hl", []):
            hot[h][k] = "hot"
        for t_n, t_v in st.get("tag", {}).items():
            tags[t_n][k] = t_v
        if "f" in st:
            for i, fk in enumerate(fields):
                fl[f"{name}f{i}"][k] = st["f"].get(fk, "—")
        if "a" in st:
            a = st["a"]
            bs = st["b"] if isinstance(st["b"], list) else [st["b"]]
            for j, b in enumerate(bs):
                key = (a, b)
                cnt = pairs.get(key, 0) + pairs.get((b, a), 0)
                pairs[key] = pairs.get(key, 0) + 1
                off = (7 if a < b else -7) if st.get("off") is None else st["off"]
                x1, y1, x2, y2 = _pt(nodes, a, b, off)
                eid = f"{name}a{k}_{j}"
                cv = st.get("curve", 0)
                body.append(arrow(eid, x1, y1, x2, y2, st.get("col", "teal"), st.get("dash", False), cv))
                els[eid] = {"c": {0: "", k: "on", k + 1: "on old"}}
                if st.get("keep"):
                    els[eid] = {"c": {0: "", k: "on"}}
                if st.get("fail"):
                    els[eid]["c"][k] = "on fail"
                    els[eid]["c"][k + 1] = "on old fail"
                hot[b][k] = "hot" if not st.get("fail") else "bad"
                # пакет
                lbl = st.get("pk", "")
                if lbl:
                    pid = f"{name}p{k}_{j}"
                    w = max(64, 11 * len(lbl) + 22)
                    mx, my = (x1 + (x2 - x1) * .7, y1 + (y2 - y1) * .7)
                    sx, sy = (x1, y1)
                    ocy = -24
                    pk.append(f'<g class="an pk {COLS.get(st.get("col", "teal"))}" data-id="{pid}" style="--md:{st.get("md", 1100)}ms">'
                              f'<path d="M{-w / 2 + 6} {ocy - 13}H{w / 2}V{ocy + 7}L{w / 2 - 6} {ocy + 13}H{-w / 2}V{ocy - 7}Z"/>'
                              f'<text x="0" y="{ocy + 5}" text-anchor="middle">{esc(lbl)}</text></g>')
                    els[pid] = {"p": {0: (round(sx, 1), round(sy, 1)), k: (round(mx, 1), round(my, 1))}, "o": {0: 0, k: 1, k + 1: 0}}
    for nid in nodes:
        els[f"n_{nid}"] = {"c": hot[nid]}
        els[f"g_{nid}"] = {"t": tags[nid]}
    for kf, v in fl.items():
        els[kf] = {"t": v}
    els[f"{name}cp"] = {"t": cap}
    els[f"{name}sn"] = {"t": sn}
    sc = scene(name, n, els, {i: steps[i - 1].get("w", wdef) for i in range(1, n + 1)}, wdef)
    svgc = f'<svg class="dg flw" viewBox="{vb}" role="img">{"".join(body)}{"".join(pk)}</svg>'
    fp = fields_panel(name, fields, ftitle) if fields else ""
    grid = "flg" if fields else "flg one"
    return (f'<div class="card dgc flow" {sc}>{pre}<div class="{grid}"><div class="flv">{svgc}</div>{fp}</div>'
            f'<div class="fcap"><span class="fsn mono" data-id="{name}sn"></span><span class="fct" data-id="{name}cp"></span></div></div>')

# ---------------------------------------------------------------- диаграмма обмена (линии жизни)
def seq(name, cols, msgs, width=900, gap=58, fields=(), ftitle="Заголовок пакета", wdef=1900, top=124, pre="", hint=""):
    ncol = len(cols)
    xs = [80 + i * (width - 160) / (ncol - 1) for i in range(ncol)]
    rows, r = [], 0
    for m in msgs:
        if m.get("clear"):
            r = 0; rows.append(None); continue
        if "a" not in m:
            rows.append(None); continue
        rows.append(r); r += 1
    maxr = max([x for x in rows if x is not None] + [0]) + 1
    H = top + maxr * gap + 40
    body = []
    for i, c in enumerate(cols):
        x = xs[i]
        body.append(f'<line class="ll" x1="{x}" y1="{top - 18}" x2="{x}" y2="{H - 10}"/>')
        from _g7a_ui import dev
        shp = f'<g transform="translate({x} 44) scale(.6)">{dev(c[2])}</g>' if c[2] in DEVK else hexnode(x, 44, 30) + svgicon(c[2], x, 44, 1.15)
        body.append(f'<g class="nd" data-id="{name}c{i}">{shp}</g>')
        body.append(f'<text class="nlab" x="{x}" y="{top - 26 + 4}" text-anchor="middle">{esc(c[0])}</text>')
        if c[1]:
            body.append(f'<text class="nsub" x="{x}" y="{top - 6 + 4}" text-anchor="middle">{esc(c[1])}</text>')
    n = len(msgs)
    els = {}
    cap, sn = {0: ""}, {0: ""}
    fl = {f"{name}f{i}": {0: ""} for i in range(len(fields))}
    groups = [[]]
    for k, m in enumerate(msgs, start=1):
        cap[k] = m.get("cap", "")
        sn[k] = f"{k:02d} / {n:02d}"
        if "f" in m:
            for i, fk in enumerate(fields):
                fl[f"{name}f{i}"][k] = m["f"].get(fk, "—")
        if m.get("clear"):
            for eid in groups[-1]:
                els[eid].setdefault("o", {0: 1})
                els[eid]["o"][k] = 0
            groups.append([])
            continue
        if "a" not in m:
            continue
        y = top + 24 + rows[k - 1] * gap
        a, b = m["a"], m["b"]
        x1, x2 = xs[a], xs[b]
        dx = 10 if x2 > x1 else -10
        eid = f"{name}m{k}"
        body.append(arrow(eid, x1 + dx, y, x2 - dx * 1.4, y, m.get("col", "teal"), m.get("dash", False)))
        els[eid] = {"c": {0: "", k: "on", k + 1: "on old"}}
        if m.get("fail"):
            els[eid]["c"][k] = "on fail"; els[eid]["c"][k + 1] = "on old fail"
        lx = (x1 + x2) / 2
        tid = f"{name}l{k}"
        sub = f'<text class="msub" x="{lx}" y="{y + 20}" text-anchor="middle">{esc(m.get("sub", ""))}</text>' if m.get("sub") else ""
        body.append(f'<g class="an ml {COLS.get(m.get("col", "teal"))}" data-id="{tid}"><text class="mlab" x="{lx}" y="{y - 9}" text-anchor="middle">{esc(m["t"])}</text>{sub}</g>')
        els[tid] = {"o": {0: 0, k: 1}}
        groups[-1] += [eid, tid]
        if m.get("x"):
            xid = f"{name}x{k}"
            body.append(f'<g class="an xmark" data-id="{xid}"><path d="M{x2 - dx * 3 - 11} {y - 11}l22 22 M{x2 - dx * 3 + 11} {y - 11}l-22 22"/></g>')
            els[xid] = {"o": {0: 0, k: 1}}
            groups[-1].append(xid)
    els[f"{name}cp"] = {"t": cap}
    els[f"{name}sn"] = {"t": sn}
    for kf, v in fl.items():
        els[kf] = {"t": v}
    sc = scene(name, n, els, {i: msgs[i - 1].get("w", wdef) for i in range(1, n + 1)}, wdef)
    svgc = f'<svg class="dg seqd" viewBox="0 0 {width} {H}" role="img">{"".join(body)}</svg>'
    fp = fields_panel(name, fields, ftitle) if fields else ""
    grid = "flg" if fields else "flg one"
    return (f'<div class="card dgc flow" {sc}>{pre}<div class="{grid}"><div class="flv">{svgc}</div>{fp}</div>'
            f'<div class="fcap"><span class="fsn mono" data-id="{name}sn"></span><span class="fct" data-id="{name}cp"></span></div>{hint}</div>')
