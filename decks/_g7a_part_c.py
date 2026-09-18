
# 38 ---------------------------------------------------------------- типы DNS-запросов (s29)
def dnsmode(name, rec):
    b = [f'<g transform="translate(90 190) scale(1.1)">{dev("pc")}</g><text x="90" y="270" text-anchor="middle" style="font-family:var(--hf)">Клиент DNS</text>',
         f'<g transform="translate(400 70) scale(.9)">{dev("server")}</g><text x="400" y="140" text-anchor="middle" style="font-family:var(--hf)">DNS-сервер 1</text>',
         f'<g transform="translate(400 250) scale(.9)">{dev("server")}</g><text x="400" y="322" text-anchor="middle" style="font-family:var(--hf)">DNS-сервер 2</text>']
    if rec:
        A = [(150, 160, 340, 80, "blue", "1"), (400, 130, 400, 195, "blue", "2"), (425, 195, 425, 130, "red", "3"), (340, 100, 150, 180, "red", "4")]
    else:
        A = [(150, 160, 340, 80, "blue", "1"), (340, 100, 150, 180, "red", "2"), (150, 200, 340, 250, "blue", "3"), (340, 270, 150, 222, "red", "4")]
    els = {}
    for i, (x1, y1, x2, y2, c, n) in enumerate(A):
        off = 12 if x1 != x2 else 0
        b.append(arrow(f"{name}{i}", x1, y1, x2, y2, c))
        mx, my = (x1 + x2) / 2 + (0 if x1 != x2 else -26 if c == "blue" else 26), (y1 + y2) / 2 - (14 if x1 != x2 else 0)
        col = "#4aa8ff" if c == "blue" else "#ff5c6e"
        b.append(f'<g class="an" data-id="{name}n{i}"><circle cx="{mx}" cy="{my}" r="13" fill="{col}"/><text x="{mx}" y="{my + 5}" text-anchor="middle" style="font-family:var(--hf);fill:#03120f">{n}</text></g>')
        els[f"{name}{i}"] = {"c": {0: "", i + 1: "on"}}
        els[f"{name}n{i}"] = {"o": {0: 0, i + 1: 1}}
    sc = scene(name, 4, els, {i: 1300 for i in range(5)})
    return f'<div {sc}><svg class="mini" viewBox="0 0 520 330" aria-hidden="true">{"".join(b)}</svg></div>'
def order(items):
    return '<div class="G" style="--gc:1fr 1fr">' + "".join(f'<div class="lrow plain2"><span class="hn" style="background:{"var(--blue)" if c == "b" else "var(--red)"}">{i+1}</span><span>{t}</span></div>' for i, (t, c) in enumerate(items)) + '</div>'
slide("Типы DNS-запросов", "", "", G("minmax(0,1.3fr) minmax(0,1fr)",
    ih("Типы", "DNS-запросов", "", "Когда DNS-сервер не имеет записи запрашиваемого доменного имени, клиент может выполнить запрос в одном из двух режимов.", inline=True, big=True),
    info("<b>DNS — это распределённая система.</b> База данных большинства DNS-серверов не содержит всех записей доменных имён.", "info", 0), cls="ac") +
    G("minmax(0,1fr) minmax(0,1fr)",
      pnl("Рекурсивный запрос", '<p class="p sm">DNS-сервер запрашивает другие DNS-серверы и возвращает результат запроса DNS-клиенту.</p>' + dnsmode("rq", True) +
          '<h3 class="uh">Порядок действий</h3>' + order([("Клиент отправляет запрос DNS-серверу.", "b"), ("DNS-сервер запрашивает другие DNS-серверы.", "b"), ("Другие DNS-серверы возвращают ответ DNS-серверу.", "r"), ("DNS-сервер возвращает результат клиенту.", "r")]), "big", 0),
      pnl("Итеративный запрос", '<p class="p sm">DNS-сервер сообщает клиенту IP-адрес другого DNS-сервера, с которого клиент запрашивает доменное имя.</p>' + dnsmode("iq", False) +
          '<h3 class="uh">Порядок действий</h3>' + order([("Клиент отправляет запрос DNS-серверу.", "b"), ("DNS-сервер сообщает IP-адрес другого DNS-сервера.", "r"), ("Клиент запрашивает имя у указанного DNS-сервера.", "b"), ("DNS-сервер возвращает результат клиенту.", "r")]), "big", 0)))
slide("Рекурсия по цепочке", "", "", G("minmax(0,.7fr) minmax(0,1.7fr)",
    ih("Рекурсивный и итеративный", "по всей цепочке", "клиент · локальный · корень · TLD · авторитетный",
       "Переключите режим: в рекурсивном вся работа на локальном DNS-сервере, клиент получает один ответ. В итеративном клиент сам обходит серверы по ссылкам."),
    '<div><div class="seg" data-sw="1"><button class="btn on" type="button" data-to="dnsr" aria-pressed="true">Рекурсивный</button><button class="btn" type="button" data-to="dnsi" aria-pressed="false">Итеративный</button></div>' +
    DNSR + DNSI.replace('class="card dgc flow"', 'hidden class="card dgc flow"', 1) + '</div>', cls="as"))

# 40 ---------------------------------------------------------------- доверенные и недоверенные (s30)
TRUST = flow("trust", "0 0 900 560", {
    "c": {"x": 80, "y": 90, "ic": "laptop", "label": "Клиент (браузер)"},
    "l": {"x": 330, "y": 90, "ic": "server", "label": "Недоверенный", "sub": "локальный, кэширующий"},
    "o": {"x": 740, "y": 90, "ic": "server", "label": "Корневой «.»"},
    "t": {"x": 740, "y": 290, "ic": "server", "label": "Зона .ru"},
    "a": {"x": 740, "y": 470, "ic": "server", "label": "Авторитетный", "sub": "зона example.ru"}}, [
    {"a": "c", "b": "l", "pk": "1 www.shop.example.ru ?", "col": "blue", "cap": "1 DNS-запрос: клиент обращается к недоверенному (локальному, кэширующему) DNS-серверу."},
    {"a": "l", "b": "o", "pk": "2 запрос", "col": "teal", "cap": "2 Запрос к корневому серверу."},
    {"a": "o", "b": "l", "pk": "3 адрес .ru", "col": "green", "cap": "3 Ответ: адрес сервера зоны .ru."},
    {"a": "l", "b": "t", "pk": "4 запрос", "col": "teal", "cap": "4 Запрос к серверу зоны .ru."},
    {"a": "t", "b": "l", "pk": "5 адрес example.ru", "col": "green", "cap": "5 Ответ: адрес сервера example.ru."},
    {"a": "l", "b": "a", "pk": "6 запрос", "col": "teal", "cap": "6 Запрос к авторитетному серверу зоны example.ru."},
    {"a": "a", "b": "l", "pk": "7 IP, AA=1", "col": "amber", "tag": {"l": "в кэш на время TTL"}, "cap": "7 Авторитетный ответ (AA=1). Недоверенный сервер сохраняет его в памяти на время действия TTL."},
    {"a": "l", "b": "c", "pk": "8 IP, AA=0", "col": "amber", "cap": "8 DNS-ответ клиенту. Повторный запрос (если запись в кэше) будет обслужен сразу, не обращаясь к доверенным серверам."},
], links=[("c", "l"), ("l", "o"), ("l", "t"), ("l", "a")], wdef=1900)
slide("Доверенные и недоверенные", "", "", G("minmax(0,.75fr) minmax(0,1.6fr) minmax(0,.85fr)",
    '<div>' + ih("Доверенные и недоверенные", "DNS-серверы", "как это работает?", "DNS — иерархическая система, в которой недоверенные серверы обращаются к доверенным за информацией о доменах и кэшируют ответы для ускорения последующих запросов.") +
    '<div class="lst">' + pnl("Доверенный DNS-сервер", '<p class="p sm">Хранит оригинальные записи о соответствии доменных имён и IP-адресов в рамках своей зоны ответственности и имеет право выдавать авторитетные ответы: информация актуальна и достоверна.</p>', "", 1, ic="server") +
    pnl("Недоверенный DNS-сервер", '<p class="p sm">Не имеет оригинальных записей в зоне ответственности. Перенаправляет запросы к вышестоящим серверам и запоминает ответы; при повторном запросе выдаёт их из памяти, не загружая корневые серверы.</p>', "", 1, ic="db") + '</div></div>',
    pnl("Пример работы DNS", TRUST + info("<b>Кэш DNS.</b> Недоверенный сервер сохраняет ответ в памяти на время действия TTL и при повторном запросе выдаёт его из кэша.", "db", 0), "", 0),
    '<div class="lst">' + pnl("Авторитетные и неавторитетные данные", '<div class="lst">' + lrow("shield", "Авторитетные данные", "Хранятся в базе данных в рамках своей зоны; за выдачу и достоверность отвечает доверенный сервер.", 2) +
                              lrow("db", "Неавторитетные данные", "Получены перенаправлением запроса к доверенному серверу и записаны в память локального DNS-сервера.", 2) + '</div>', "", 2) +
    pnl("Флаг AA (Authoritative Answer)", '<p class="p sm">Флаг AA в DNS-ответе показывает, являются ли данные авторитетными:</p>' +
        '<div class="lst"><div class="lrow"><span class="nb">1</span><div><span>Данные получены от сервера, который отвечает за эту область данных.</span></div></div>'
        '<div class="lrow"><span class="nb">0</span><div><span>Выданы из памяти локального DNS-сервера, записавшего их при получении от доверенного сервера.</span></div></div></div>', "", 3) + '</div>', cls="as") +
    '<div class="mt">' + qt("Кэш на недоверенных серверах снижает нагрузку на доверенные серверы и ускоряет доступ; актуальность данных обеспечивается периодической очисткой памяти с последующим обновлением у доверенных серверов.", 4) + '</div>')

# 41 ---------------------------------------------------------------- проблемы ручной настройки (s32)
slide("Ручная настройка: проблемы", "", "", G("minmax(0,1fr) minmax(0,1fr)",
    '<div class="card pn half" data-s="0">' + ih("Проблемы", "при ручной настройке параметров сети") +
    G("minmax(0,1.1fr) minmax(0,.9fr)",
      '<div class="card pn" data-s="1"><div class="pns">Конфигурация IPv4-адреса</div><div class="form"><span>IP-адрес</span><b>192 . 168 . 1 . 10</b><span>Маска</span><b>255 . 255 . 255 . 0</b>'
      '<span>Шлюз</span><b>192 . 168 . 1 . 1</b><span>DNS</span><b>8 . 8 . 8 . 8</b></div></div>',
      '<div class="qcloud" data-s="2"><span class="qtag">Адрес?</span><span class="qtag">Маска?</span>' + hexicon("warn", "hx lg red") + '<span class="qtag">Шлюз?</span><span class="qtag">DNS?</span></div>', cls="ac") +
    '<div class="G ac" style="--gc:1fr auto;margin:.6rem 0"><div class="alert" data-s="3">' + hexicon("cross", "hx sm") + 'Нет подключения к сети</div>' + devsvg("laptop", ">_", "8rem") + '</div>' +
    '<div class="lst">' + lrow("user", "Пользователи", "Обычные пользователи не знакомы с сетевыми параметрами — частые неправильные конфигурации приводят к сбою подключения к сети.", 4) +
    lrow("warn", "Конфликты", "Случайная конфигурация IP-адресов может вызвать конфликты IP-адресов.", 4) + '</div></div>',
    '<div class="card pn half" data-s="0">' + ih("Большая", "рабочая нагрузка") +
    G("minmax(0,1.3fr) minmax(0,.8fr)", '<div class="mon">' + "".join(f'<div data-s="5" style="--dl:{i*30}ms">{devsvg("monitor", "", "100%")}</div>' for i in range(20)) + '</div>',
      '<div class="lst"><div class="card pn" data-s="6"><h3>План работы на неделю</h3>' + bul(["Распределение IP-адресов", "Настройка параметров", "Проверка доступности", "Решение обращений", "Обновление конфигураций", "…"]) + '</div>' +
      devbox("user", "Администратор сети", "", "", "4rem", 6) + '</div>', cls="ac") +
    '<div class="lst mt">' + lrow("gear", "Централизованно и вручную", "Администраторы настраивают сетевые параметры централизованно, с большими нагрузками и повторяющимися задачами.", 7) +
    lrow("file", "Заранее", "Администраторы должны заранее спланировать и выделить IP-адреса пользователям.", 7) + '</div></div>', cls="as"))

# 42 ---------------------------------------------------------------- низкий коэффициент / WLAN (s33)
IPS = ["192.168.1.10", "192.168.1.11", "192.168.1.12", None, "192.168.1.14", None, "192.168.1.16", "192.168.1.17", "192.168.1.18", "192.168.1.19", None, "192.168.1.21", None, "192.168.1.23", "192.168.1.24", "192.168.1.25"]
ipgrid = '<div class="G" style="--gc:repeat(4,minmax(0,1fr));gap:.45rem">' + "".join(
    f'<div class="ipc{" off" if a is None else ""}" data-s="{2 if a is None else 1}" style="--dl:{i*40}ms">{devsvg("monitor", "", "3rem", "red" if a is None else "")}{a or "Не используется"}</div>' for i, a in enumerate(IPS)) + '</div>'
WLAN = ('<svg class="mini" viewBox="0 0 620 300" aria-hidden="true"><circle class="zone" cx="170" cy="160" r="140"/><circle class="zone" cx="450" cy="160" r="140"/>'
        '<text x="170" y="40" text-anchor="middle" style="font-family:var(--hf);fill:#2ee6c8;font-size:18px">Офис A</text><text x="450" y="40" text-anchor="middle" style="font-family:var(--hf);fill:#2ee6c8;font-size:18px">Офис B</text>'
        f'<g transform="translate(170 100)">{dev("ap")}</g><g transform="translate(450 100)">{dev("ap")}</g>'
        '<text x="170" y="140" text-anchor="middle">Точка доступа (AP-1)</text><text x="450" y="140" text-anchor="middle">Точка доступа (AP-2)</text>'
        f'<g transform="translate(120 230) scale(.55)">{dev("laptop")}</g><g transform="translate(190 230) scale(.5)">{dev("phone")}</g><g transform="translate(430 230) scale(.55)">{dev("laptop")}</g><g transform="translate(500 230) scale(.5)">{dev("phone")}</g>'
        f'<g class="an" data-id="sta" style="--md:2000ms"><g transform="scale(.6)">{dev("laptop")}</g></g>'
        '<text x="310" y="150" text-anchor="middle" style="font-family:var(--hf)">Перемещение между офисами</text>'
        '<g class="an" data-id="stq"><text x="450" y="290" text-anchor="middle" style="fill:#f5b83d;font-weight:700">нужна повторная настройка IP-адреса?</text></g></svg>')
WLAN_SC = scene("wlan", 2, {"sta": {"p": {0: (230, 190), 1: (400, 190)}}, "stq": {"o": {0: 0, 2: 1}}}, {1: 2300, 2: 1200})
slide("Низкая эффективность", "", "", G("minmax(0,1fr) minmax(0,1fr)",
    '<div class="card pn half" data-s="0">' + ih("Низкий коэффициент", "использования IP-адресов", "", "В корпоративной сети каждый пользователь использует фиксированный IP-адрес.") + ipgrid +
    '<div class="G ac mt" style="--gc:auto 1fr" data-s="3"><div class="pie"></div><div><b class="hl" style="font-size:1.6rem;font-family:var(--hf)">62%</b> используется · <b style="color:var(--red);font-size:1.6rem;font-family:var(--hf)">38%</b> не используется'
    '<p class="p sm">Коэффициент использования IP-адресов очень низкий, а некоторые адреса остаются неиспользованными длительное время.</p></div></div></div>',
    '<div class="card pn half" data-s="0">' + ih("Низкая гибкость", "в беспроводных сетях (WLAN)", "", "Беспроводные локальные сети обеспечивают гибкое расположение станций (STA), но при перемещении из одной зоны покрытия в другую может потребоваться повторная настройка IP-адреса.") +
    f'<div {WLAN_SC}>{WLAN}</div>' + '<div class="lst">' + lrow("radio", "Перемещение STA", "При перемещении STA между зонами покрытия может потребоваться повторная настройка IP-адреса.", 3) +
    lrow("gear", "Неудобство", "Это усложняет использование сети и снижает удобство для пользователей.", 3) + '</div></div>', cls="as"))

# 43 ---------------------------------------------------------------- DHCP (s34)
DHCPF = flow("dhcpf", "0 0 900 330", {
    "c1": {"x": 70, "y": 80, "ic": "laptop", "label": "Ноутбук", "r": 30}, "c2": {"x": 200, "y": 70, "ic": "monitor", "label": "ПК", "r": 30},
    "c3": {"x": 70, "y": 230, "ic": "phone", "label": "Смартфон", "r": 30}, "c4": {"x": 200, "y": 240, "ic": "printer", "label": "Принтер", "r": 26},
    "sw": {"x": 470, "y": 170, "ic": "switch", "label": "Сетевое оборудование", "r": 34}, "s": {"x": 790, "y": 170, "ic": "server", "label": "Сервер DHCP", "sub": "пул адресов"}}, [
    {"a": "c1", "b": "sw", "pk": "DHCP Discover", "col": "teal", "cap": "Устройства в сети — клиенты DHCP — получают сетевые параметры автоматически: запрос IP-адреса."},
    {"a": "sw", "b": "s", "pk": "DHCP Discover", "col": "teal", "cap": "Запрос достигает сервера DHCP."},
    {"hl": ["s"], "tag": {"s": "свободный адрес из пула"}, "cap": "Сервер выдаёт свободный IP-адрес из выделенного диапазона — пула адресов."},
    {"a": "s", "b": "sw", "pk": "DHCP Offer / ACK", "col": "green", "cap": "Назначение IP-адреса: IP, маска, шлюз, DNS."},
    {"a": "sw", "b": "c1", "pk": "DHCP Offer / ACK", "col": "green", "tag": {"c1": "192.168.1.10"}, "cap": "Клиент получил параметры. Так же настраиваются остальные устройства."},
], links=[("c1", "sw"), ("c2", "sw"), ("c3", "sw"), ("c4", "sw"), ("sw", "s")], extra='<rect class="zone" x="14" y="14" width="260" height="300"/><text class="zl" x="28" y="36">Клиенты DHCP</text>', wdef=1900)
slide("DHCPv4", "", "", G("minmax(0,.8fr) minmax(0,1.8fr) minmax(0,.8fr)",
    '<div>' + ih("Работа протокола", "DHCP", "автоматическая настройка сетевых параметров",
                 "DHCP необходим для автоматического назначения сетевых параметров узла. Без них работа устройства в сети невозможна, поэтому этот сервис используется первым.") +
    pnl("", '<div class="lst">' + lrow("globe", "IP-адрес", "Уникальный адрес устройства в сети", 1) + lrow("layers", "Маска подсети", "Определяет границы сети", 1) +
        lrow("router", "Шлюз по умолчанию", "Доступ в другие сети (например, в Интернет)", 1) + lrow("dns", "Адрес DNS-сервера", "Преобразование доменных имён в IP-адреса", 1) + '</div>', "", 1) + '</div>',
    '<div>' + DHCPF + G("minmax(0,1fr) minmax(0,1fr)",
                        pnl("В домашних сетях", '<div class="G ac" style="--gc:1fr auto"><p class="p sm" style="margin:0">В качестве DHCP-сервера выступает домашний маршрутизатор.</p>' + devsvg("router", "", "5rem") + '</div>', "", 2, ic="desk"),
                        pnl("В средних и крупных сетях", '<div class="G ac" style="--gc:1fr auto"><p class="p sm" style="margin:0">В качестве DHCP-сервера выделяется отдельный компьютер.</p>' + devsvg("server", "", "3rem") + '</div>', "", 2, ic="server")) +
    '<div class="mt">' + qt("Получение IP-адреса автоматически обычно настроено на сетевом интерфейсе по умолчанию после установки операционной системы.", 3) + '</div></div>',
    pnl("Типы адресации", '<div class="lst">' + pnl("Динамическая адресация", '<p class="p sm">В больших сетях, где количество устройств постоянно меняется: автоматически предоставляет параметры для доступа к сети.</p>', "", 1, ic="link") +
        pnl("Статическая адресация", '<p class="p sm">Параметры назначаются вручную — для серверов и принтеров, которым нужен постоянный IP-адрес.</p>', "", 1, ic="gear") + '</div>', "", 1), cls="as"))

# 44 ---------------------------------------------------------------- преимущества DHCP (s35)
POOLF = flow("poolf", "0 0 620 300", {
    "a": {"x": 60, "y": 60, "ic": "laptop", "label": "Клиент DHCP", "r": 30}, "b": {"x": 60, "y": 160, "ic": "pc", "label": "Клиент DHCP", "r": 30}, "p": {"x": 60, "y": 255, "ic": "phone", "label": "Клиент DHCP", "r": 26},
    "sw": {"x": 300, "y": 160, "ic": "switch", "label": "Коммутатор", "r": 34}, "s": {"x": 540, "y": 150, "ic": "server", "label": "Сервер DHCP"}}, [
    {"a": "a", "b": "sw", "pk": "1 запрос", "col": "blue"}, {"a": "b", "b": "sw", "pk": "1 запрос", "col": "blue"}, {"a": "sw", "b": "s", "pk": "запросы", "col": "blue", "cap": "IP-адреса получают из единого пула на сервере DHCP."},
], links=[("a", "sw"), ("b", "sw"), ("p", "sw"), ("sw", "s")], wdef=1100)
LEASEF = flow("leasef", "0 0 620 260", {"c": {"x": 90, "y": 120, "ic": "laptop", "label": "Клиент DHCP"}, "s": {"x": 530, "y": 110, "ic": "server", "label": "Сервер DHCP"}}, [
    {"a": "c", "b": "s", "pk": "1 Запрос адреса", "col": "blue"}, {"a": "s", "b": "c", "pk": "2 Ответ с адресом", "col": "red", "tag": {"c": "аренда 8 часов"}}], links=[("c", "s")], wdef=1300)
slide("Преимущества DHCP", "", "", G("minmax(0,1fr) minmax(0,1fr)",
    '<div class="card pn half" data-s="0">' + ih("Унифицированное", "управление", "", "IP-адреса получают из единого пула на сервере DHCP.") + POOLF +
    G("minmax(0,1.2fr) minmax(0,1fr)", pnl("Пул IP-адресов (Pool-No 1)", '<table class="tbl2">' + "".join(f"<tr><td>{a}</td><td>{b_}</td></tr>" for a, b_ in (("DNS-сервер", "10.1.1.2"), ("Сеть", "10.1.2.0"), ("Маска", "255.255.255.0"), ("Шлюз", "10.1.2.1"), ("Всего адресов", "252"), ("Используется", "2"))) + '</table>', "", 1),
      '<div class="G ac" style="--gc:auto 1fr" data-s="1">' + hexicon("db", "hx lg") + '<p class="p sm">Сервер DHCP записывает и поддерживает статус использования IP-адресов для унифицированного назначения.</p></div>', cls="ac") + '</div>',
    '<div class="card pn half" data-s="0">' + ih("Аренда", "IP-адресов", "", "DHCP определяет время аренды (lease) для эффективного использования IP-адресов.", inline=True) + LEASEF +
    G("minmax(0,1.3fr) minmax(0,.8fr)", pnl("", '<div class="G ac" style="--gc:auto 1fr">' + hexicon("file", "hx lg") + kv([("IP-адрес:", "192.168.1.10"), ("Маска подсети:", "255.255.255.0 (/24)"), ("Шлюз:", "192.168.1.1"), ("DNS-сервер:", "114.114.114.114"), ("Время аренды:", "<span class='hl'>8 часов</span>")]) + '</div>', "", 1),
      '<div class="G ac" style="--gc:auto 1fr" data-s="1">' + hexicon("clock", "hx lg") + '<p class="p sm">По истечении времени аренды IP-адрес может быть автоматически обновлён.</p></div>', cls="ac") + '</div>', cls="as") +
    G("repeat(3,minmax(0,1fr))", lrow("user", "Эффективное использование адресного пространства", "Динамическая адресация позволяет повторно использовать IP-адреса — важно в больших сетях с меняющимся количеством устройств.", 2),
      lrow("gear", "Простое управление", "Централизованное назначение и контроль IP-адресов упрощает администрирование и снижает вероятность ошибок.", 2),
      lrow("clock", "Гибкость", "Время аренды позволяет эффективно использовать IP-адреса и автоматически обновлять конфигурацию устройств.", 2), style="margin-top:.8rem") +
    '<div class="mt">' + qt("DHCP обеспечивает автоматическое назначение сетевых параметров, упрощая работу в сети и повышая её эффективность.", 3) + '</div>')

# 45 ---------------------------------------------------------------- DORA (s36)
CMc, SMc = "e4:5a:d4:1f:f4:80", "a0:a3:f0:d1:26:5a"
slide("DHCP: четыре этапа", "", "", G("minmax(0,1.5fr) minmax(0,1fr)",
    ih("Процесс предоставления", "IP-адреса клиенту от DHCP-сервера"),
    info("DHCP (Dynamic Host Configuration Protocol) — автоматически назначает сетевые параметры устройствам в сети. Адреса — из захвата Wireshark лекции.", "info", 0), cls="ac") +
    G("minmax(0,.55fr) minmax(0,.5fr) minmax(0,2.2fr) minmax(0,.5fr)",
      '<div class="lst">' + "".join(f'<div class="lrow" data-s="{i*1+1}"><span class="hn" style="width:2.4rem;height:2.2rem;font-size:1.3rem">{i+1}</span><span style="font-size:.88rem;color:#d3f0ea">{t}</span></div>'
                                    for i, t in enumerate(["Клиент ищет DHCP-сервер в сети", "Сервер предлагает сетевые параметры клиенту", "Клиент подтверждает выбор предложения от конкретного сервера", "Сервер подтверждает выдачу IP-адреса"])) + '</div>',
      '<div class="col-dev" style="height:100%">' + devsvg("laptop", "", "7rem") + '<span class="dvbl">DHCP-клиент</span><span class="dvbs">' + CMc + '</span></div>',
      '<div class="lst">' +
      msgrow("DHCPDISCOVER", "target", "r", "red", "Широковещательная рассылка", [("IP источника", "0.0.0.0"), ("MAC источника", CMc)], [("IP назначения", "255.255.255.255"), ("MAC назначения", "ff:ff:ff:ff:ff:ff")], 1, 2600) +
      msgrow("DHCPOFFER", "file", "l", "blue", "Предложенный IP-адрес 10.10.1.13 и срок аренды", [("IP назначения", "255.255.255.255"), ("MAC назначения", "ff:ff:ff:ff:ff:ff")], [("IP источника", "10.10.1.1"), ("MAC источника", SMc)], 2, 2600) +
      msgrow("DHCPREQUEST", "check", "r", "red", "Широковещательная рассылка", [("IP источника", "0.0.0.0"), ("MAC источника", CMc)], [("IP назначения", "255.255.255.255"), ("MAC назначения", "ff:ff:ff:ff:ff:ff")], 3, 2600) +
      msgrow("DHCPACK", "check", "l", "blue", "Подтверждает выдачу IP-адреса", [("IP назначения", "255.255.255.255"), ("MAC назначения", "ff:ff:ff:ff:ff:ff")], [("IP источника", "10.10.1.1"), ("MAC источника", SMc)], 4, 2600) + '</div>',
      '<div class="col-dev" style="height:100%">' + devsvg("server", "", "5rem") + '<span class="dvbl">DHCP-сервер</span><span class="dvbs">10.10.1.1</span></div>', cls="as") +
    G("minmax(0,1fr) minmax(0,1fr)", info("Если запрашиваемый адрес недоступен, сервер отправляет сообщение с отказом (DHCPNAK), и процесс получения адреса начинается заново.", "info", 5),
      info("Перед отправкой DHCPACK сервер проверяет доступность адреса (например, с помощью ICMP-запроса).", "gear", 5), style="margin-top:.8rem"))

# 46 ---------------------------------------------------------------- Wireshark DHCP
def wsd(title, lines, s):
    return pnl(title, '<div class="ws" style="font-size:.72rem">' + "\n".join(lines) + '</div>', "", s)
slide("Wireshark: DHCP", "", "", ih("Анализ DHCP", "с помощью Wireshark", "по четырём захватам лекции", inline=True) +
      table(["Сообщение", "MAC назначения", "IP источника", "IP назначения", "Порты UDP"], [
          ["DHCPDISCOVER", "ff:ff:ff:ff:ff:ff", "0.0.0.0", "255.255.255.255", "68 ▸ 67"], ["DHCPOFFER", "ff:ff:ff:ff:ff:ff", "10.10.1.1", "255.255.255.255", "67 ▸ 68"],
          ["DHCPREQUEST", "ff:ff:ff:ff:ff:ff", "0.0.0.0", "255.255.255.255", "68 ▸ 67"], ["DHCPACK", "ff:ff:ff:ff:ff:ff", "10.10.1.1", "255.255.255.255", "67 ▸ 68"]], "mono") +
      G("repeat(4,minmax(0,1fr))",
        wsd("DHCPDISCOVER", ['<span class="rd">Info: DHCP Discover</span>', "Ethernet II, Src: EltexEnt_1f:f4:80", '<span class="rd">Destination: Broadcast (ff:ff:ff:ff:ff:ff)</span>', '<span class="rd">IPv4, Src: 0.0.0.0, Dst: 255.255.255.255</span>', "UDP, Src Port: 68, Dst Port: 67"], 2),
        wsd("DHCPOFFER", ['<span class="rd">Info: DHCP Offer</span>', '<span class="rd">Destination: Broadcast (ff:ff:ff:ff:ff:ff)</span>', "Source: D-LinkIn_d1:26:5a", '<span class="rd">IPv4, Src: 10.10.1.1, Dst: 255.255.255.255</span>', '<span class="rd">Your (client) IP address: 10.10.1.13</span>', "Option: (51) IP Address Lease Time"], 2),
        wsd("DHCPREQUEST", ['<span class="rd">Info: DHCP Request</span>', "Destination: Broadcast", '<span class="rd">IPv4, Src: 0.0.0.0, Dst: 255.255.255.255</span>', "UDP, Src Port: 68, Dst Port: 67", "Option: (54) DHCP Server Identifier (10.10.1.1)", '<span class="rd">Option: (50) Requested IP Address (10.10.1.13)</span>'], 3),
        wsd("DHCPACK", ['<span class="rd">Info: DHCP ACK</span>', '<span class="rd">Destination: Broadcast (ff:ff:ff:ff:ff:ff)</span>', '<span class="rd">IPv4, Src: 10.10.1.1, Dst: 255.255.255.255</span>', "Your (client) IP address: 10.10.1.13", "Subnet Mask (255.255.255.0)", "IP Address Lease Time: (600s) 10 minutes"], 3), style="margin-top:.8rem"))

# 47 ---------------------------------------------------------------- конфликт (s37)
slide("Конфликт IP-адресов", "", "", G("minmax(0,1.3fr) minmax(0,1fr)",
    ih("Проверка IP-адреса", "на конфликт", "", "Действия DHCP-клиента после получения адреса от сервера."),
    info("Наличие двух узлов с одинаковым IP-адресом в сети маловероятно, но возможно. Чтобы избежать таких ситуаций, клиент проверяет полученный адрес.", "info", 0), cls="ac") +
    G("minmax(0,2fr) minmax(0,.9fr)",
      '<div>' + G("minmax(0,.4fr) minmax(0,2fr) minmax(0,.4fr)",
                  '<div class="col-dev" style="height:100%">' + devsvg("monitor", "", "6rem") + '<span class="dvbl">DHCP-клиент</span><span class="dvbs">MAC: ' + CMc + '<br>IP: 10.10.1.13</span></div>',
                  '<div class="lst">' +
                  msgrow("1 DHCPACK", "check", "l", "blue", "Подтверждаю принятие IPv4-адреса", [("IP назначения", "255.255.255.255"), ("MAC назначения", "ff:ff:ff:ff:ff:ff")], [("IP источника", "10.10.1.1"), ("MAC источника", SMc)], 1, 1800) +
                  msgrow("2 ARP-request", "info", "r", "red", "У кого-нибудь есть такой же адрес?", [("IP источника", "10.10.1.13"), ("MAC источника", CMc)], [("IP назначения", "10.10.1.13"), ("MAC назначения", "ff:ff:ff:ff:ff:ff")], 2, 1800) +
                  msgrow("3 ARP-reply", "warn", "l", "blue", "У меня", [("IP назначения", "10.10.1.13"), ("MAC назначения", CMc)], [("IP источника", "10.10.1.13"), ("MAC источника", "xx:xx:xx:xx:xx:xx (другое)")], 3, 1800) +
                  msgrow("4 DHCPDECLINE", "cross", "r", "red", "Нет, спасибо", [("IP источника", "0.0.0.0"), ("MAC источника", CMc)], [("IP назначения", "255.255.255.255"), ("MAC назначения", "ff:ff:ff:ff:ff:ff")], 4, 1800) + '</div>',
                  '<div class="col-dev" style="height:100%">' + devsvg("server", "", "4.5rem") + '<span class="dvbl">DHCP-сервер</span><span class="dvbs">MAC: ' + SMc + '<br>IP: 10.10.1.1</span></div>', cls="as") +
      G("minmax(0,1fr) minmax(0,1fr)", pnl("ARP-ответа нет", '<p class="p sm">Такой IP-адрес в сети не используется: DHCP-сервер не обманул клиента, адрес уникален для сегмента. Клиент начинает его применять.</p>', "grn", 5, ic="check"),
        pnl("Получен ARP-ответ", '<p class="p sm">Этот IP-адрес уже используется. Клиент отправляет <b>DHCPDECLINE</b>, чтобы сервер назначил другой адрес.</p>', "red", 5, ic="cross"), style="margin-top:.6rem") + '</div>',
      '<div class="lst">' + pnl("Что такое конфликт IP-адресов?", '<p class="p sm">Два устройства с одинаковым IP-адресом не могут корректно получать информацию от других узлов. Бывает при ручном назначении адресов разными администраторами без координации или без документации по инвентаризации адресов.</p>', "", 1, ic="warn") +
      pnl("Зачем нужна проверка?", '<p class="p sm">После DHCPACK клиент отправляет ARP-запрос на назначенный IP-адрес, чтобы убедиться, что он уникален в данном сегменте сети.</p>', "", 2, ic="shield") +
      pnl("Что делать дальше?", '<p class="p sm">Нет ARP-ответа — адрес свободен. Есть ответ — клиент уведомляет DHCP-сервер сообщением DHCPDECLINE и получает другой IP-адрес.</p>', "", 5, ic="gear") + '</div>', cls="as"))

# 48 ---------------------------------------------------------------- продление аренды (s38)
def lease_panel(n, t, sub, body, s, cls=""):
    return f'<div class="card pn {cls}" data-s="{s}" data-w="1800"><div class="pnh"><span class="nb" style="width:3.2rem;height:2.8rem;font-size:1.5rem">{n}</span><div><h3 style="margin:0;text-transform:uppercase">{t}</h3><div class="pns" style="margin:0">{sub}</div></div></div>{body}</div>'
def fan(col, lab, sub):
    return f'<div class="ar c-{col}" style="text-align:center;font-family:var(--hf)">{lab}<br><small>{sub}</small>{mline("r", col)}{mline("r", col, "fan1")}{mline("r", col, "fan2")}</div>'
LT = ('<div class="tl" data-s="1"><div class="ln"></div>'
      '<div class="pt" style="left:0;color:var(--cyan)"><i></i>Получение<br>IP-адреса</div><div class="pt" style="left:50%;color:var(--green)"><i></i>T0<br>(50% аренды)</div>'
      '<div class="pt" style="left:87.5%;color:var(--amber)"><i></i>T1<br>(87,5% аренды)</div><div class="pt" style="left:100%;color:var(--red)"><i></i>Истечение<br>аренды</div></div>')
slide("Продление аренды", "", "", G("minmax(0,1.3fr) minmax(0,1fr)", ih("Продление аренды", "IP-адреса в DHCP"),
    info("После получения IP-адреса и времени аренды DHCP-клиент устанавливает два таймера: <b style='color:var(--amber)'>T0 = 50%</b> от времени аренды, <b>T1 = 87,5%</b> от времени аренды.", "clock", 0), cls="ac") +
    G("minmax(0,1fr) minmax(0,1fr)",
      lease_panel(1, "Наступление T0", "Продление аренды у того же сервера",
                  '<div class="G ac" style="--gc:auto 1fr auto">' + devbox("laptop", "DHCP-клиент", "IP: 10.10.1.10<br>MAC: " + CMc, "", "7rem", 1) +
                  '<div><div class="ar c-blue" style="text-align:center;font-family:var(--hf)">DHCPREQUEST<br><small>(одноадресная рассылка) продление аренды</small>' + mline("r", "blue") + '</div>'
                  '<div class="ar c-grn" style="text-align:center;font-family:var(--hf);margin-top:1rem">' + mline("l", "grn") + 'DHCPACK<br><small>(подтверждение)</small></div></div>' +
                  devbox("server", "DHCP-сервер", "IP: 10.10.1.1<br>MAC: " + SMc, "", "5rem", 1) + '</div>' +
                  info("Сервер продлевает аренду, сбрасывает таймеры, а клиент обновляет T0 и T1, продолжая использовать свой IP-адрес.", "check", 1), 1),
      '<div class="lst">' +
      lease_panel(2, "Нет ответа. Наступление T1", "Попытка продления широковещательной рассылкой",
                  '<div class="G ac" style="--gc:auto 1fr auto">' + devsvg("laptop", "", "5rem") + fan("red", "DHCPREQUEST", "(широковещательная рассылка)") +
                  '<div class="lst" style="gap:.2rem">' + "".join(devsvg("server", "", "2rem") for _ in range(3)) + '</div></div>' +
                  '<div class="alert">' + hexicon("warn", "hx sm") + 'Если ответа нет, клиент продолжает использовать IP-адрес до окончания аренды — вдруг у сервера просто сменился адрес.</div>', 2, "red") +
      lease_panel(3, "Нет ответа. Истечение аренды", "Начало нового цикла получения IP-адреса",
                  '<div class="G ac" style="--gc:auto 1fr auto 1fr">' + devsvg("laptop", "", "5rem") + fan("red", "DHCPDISCOVER", "(широковещательная рассылка)") +
                  '<div class="lst" style="gap:.2rem">' + "".join(devsvg("server", "", "2rem") for _ in range(2)) + '</div>' +
                  '<div class="alert" style="font-size:.8rem">Если сервер отказывает в продлении (DHCPNACK) или не отвечает — новый цикл с DHCPDISCOVER.</div></div>', 3, "red") + '</div>', cls="as") +
    '<div class="mt">' + LEASE + '</div>')

# 49 ---------------------------------------------------------------- DHCP relay (s43)
RM = "a0:a3:f0:d1:26:5a"
def rmsg(n, name, note, col, d, a, b_, extra, s):
    return (f'<div class="msg" data-s="{s}" data-w="1500"><div class="mh"><span class="chip {"red" if col == "red" else "blue"}">{n:02d}</span>{name}<small>{note}</small></div>{mline(d, col)}'
            f'<div class="addr" style="grid-template-columns:1fr">{adr(a + b_)}</div>{extra}</div>')
def ex(t):
    return f'<div class="dimp" style="font-size:.8rem;margin-top:.2rem">{t}</div>'
slide("DHCP relay", "", "", G("minmax(0,1.3fr) minmax(0,1fr)",
    ih("DHCP", "relay", "передача DHCP-сообщений между сетями · связь клиента с удалённым DHCP-сервером", inline=True, big=True),
    info("DHCP-ретранслятор (DHCP relay) передаёт запросы и ответы DHCP между разными сетями, так как широковещательные сообщения не проходят через маршрутизаторы.", "info", 0), cls="ac") +
    G("minmax(0,2fr) minmax(0,.8fr)",
      '<div class="card pn" data-s="0">' +
      G("auto 1fr auto 1fr auto", devbox("monitor", "PC-A", "DHCP-клиент", "", "5rem", 0), '<div class="netl"><span>192.168.10.0/24</span></div>', devbox("router", "DHCP-relay", ".1 | .1", "", "6rem", 0),
        '<div class="netl"><span>192.168.30.0/24</span></div>', devbox("server", "DHCP-сервер", ".10", "", "3.5rem", 0), cls="ac") +
      G("minmax(0,1fr) minmax(0,1fr)",
        '<div class="lst">' + rmsg(1, "DHCPDISCOVER", "широковещательно", "red", "r", [("IP src", "0.0.0.0"), ("MAC src", CMc)], [("IP dst", "255.255.255.255"), ("MAC dst", "ff:ff:ff:ff:ff:ff")], "", 1) +
        rmsg(4, "DHCPOFFER", "одноадресно, для PC-A", "blue", "l", [("IP src", "192.168.10.1"), ("MAC src", RM)], [("IP dst", "192.168.10.15"), ("MAC dst", CMc)], ex("Предлагаемый адрес: <b class='hl'>192.168.10.15</b>"), 4) +
        rmsg(5, "DHCPREQUEST", "широковещательно", "red", "r", [("IP src", "0.0.0.0"), ("MAC src", CMc)], [("IP dst", "255.255.255.255"), ("MAC dst", "ff:ff:ff:ff:ff:ff")], ex("Запрашиваемый адрес: <b class='hl'>192.168.10.15</b>"), 5) +
        rmsg(8, "DHCPACK", "одноадресно, для PC-A", "blue", "l", [("IP src", "192.168.10.1"), ("MAC src", RM)], [("IP dst", "192.168.10.15"), ("MAC dst", CMc)], ex("Назначенный адрес: <b class='hl'>192.168.10.15</b>"), 8) + '</div>',
        '<div class="lst">' + rmsg(2, "DHCPDISCOVER", "от PC-A, одноадресно", "red", "r", [("IP src", "192.168.10.1"), ("MAC src", RM)], [("IP dst", "192.168.30.10"), ("MAC dst", "server-mac")], ex("В поле <b class='hl'>GIADDR</b> указан адрес 192.168.10.1"), 2) +
        rmsg(3, "DHCPOFFER", "одноадресно, для PC-A", "blue", "l", [("IP src", "192.168.30.10"), ("MAC src", "server-mac")], [("IP dst", "192.168.10.1"), ("MAC dst", RM)], ex("Предлагаемый адрес: 192.168.10.15"), 3) +
        rmsg(6, "DHCPREQUEST", "от PC-A, одноадресно", "red", "r", [("IP src", "192.168.10.1"), ("MAC src", RM)], [("IP dst", "192.168.30.10"), ("MAC dst", "server-mac")], ex("Запрашиваемый адрес: 192.168.10.15"), 6) +
        rmsg(7, "DHCPACK", "одноадресно, для PC-A", "blue", "l", [("IP src", "192.168.30.10"), ("MAC src", "server-mac")], [("IP dst", "192.168.10.1"), ("MAC dst", RM)], ex("Назначенный адрес: 192.168.10.15"), 7) + '</div>', cls="as", style="margin-top:.6rem") + '</div>',
      '<div class="lst">' + pnl("Как работает DHCP relay?", steps(["Перехватывает широковещательные запросы от клиента (DHCPDISCOVER).", "Заменяет адрес источника на адрес своего интерфейса и добавляет его в поле GIADDR.",
                                                                  "Передаёт запрос DHCP-серверу одноадресно.", "Получает ответ от сервера (DHCPOFFER, DHCPACK).", "Отправляет ответ клиенту одноадресно, используя MAC-адрес клиента из сообщения."]), "", 1) +
      pnl("Важно знать", '<div class="lst">' + lrow("globe", "", "Широковещательные сообщения DHCP не проходят через маршрутизаторы.") + lrow("link", "", "Клиент и сервер должны быть в одном широковещательном домене или использовать DHCP relay.") +
          lrow("gear", "", "По полю GIADDR сервер определяет, какой пул адресов использовать для конкретной сети.") + '</div>', "", 1) + '</div>', cls="as") +
    G("minmax(0,1fr) minmax(0,1fr)", pnl("", '<div class="G ac" style="--gc:auto 1fr">' + hexicon("check", "hx lg") + '<div><h3>Результат</h3><p class="p sm" style="margin:0">PC-A получает IP-адрес 192.168.10.15 от удалённого DHCP-сервера через DHCP-ретранслятор.</p></div></div>', "", 9),
      qt("DHCP relay объединяет сети и делает автоматическую настройку доступной в любой инфраструктуре.", 9), style="margin-top:.8rem"))

# 50 ---------------------------------------------------------------- SMB (s44)
SMBV = ('<svg class="mini" viewBox="0 0 700 220" aria-hidden="true">' f'<g transform="translate(110 110) scale(1.3)">{dev("monitor", "", "blue")}</g><g transform="translate(590 110) scale(1.3)">{dev("monitor", "", "blue")}</g>'
        + arrow("sm1", 190, 110, 510, 110, "teal") + arrow("sm2", 510, 110, 190, 110, "teal") +
        "".join(f'<g class="an" data-id="sf{i}" style="--md:1600ms"><path class="fpg" d="M-12 -16h16l8 8v24h-24z"/></g>' for i in range(4)) + '</svg>')
SMBV_SC = scene("smbv", 3, {"sm1": {"c": {0: "", 1: "on"}}, "sm2": {"c": {0: "", 2: "on"}},
                            "sf0": {"p": {0: (200, 80), 1: (480, 80)}, "o": {0: 0, 1: 1}}, "sf1": {"p": {0: (200, 145), 1: (480, 145)}, "o": {0: 0, 1: 1}},
                            "sf2": {"p": {0: (500, 80), 2: (230, 80)}, "o": {0: 0, 2: 1}}, "sf3": {"p": {0: (500, 145), 3: (260, 145)}, "o": {0: 0, 3: 1}}}, {i: 1400 for i in range(4)})
slide("SMB", "", "", G("minmax(0,1fr) minmax(0,1fr)",
    ih("SMB", "обмен данными между узлами", "", "Протокол SMB обеспечивает совместный доступ к файлам, директориям, принтерам и другим сетевым ресурсам.", big=True),
    info("<b>SMB (Server Message Block)</b> — протокол для передачи данных между клиентом и сервером. Определяет организацию совместных ресурсов в сети.", "info", 0), cls="ac") +
    G("minmax(0,1.6fr) minmax(0,1fr)", f'<div class="card pn" data-s="0"><div {SMBV_SC}>{SMBV}</div><div class="G" style="--gc:1fr 1fr;text-align:center"><span class="dvbl">Узел 1 (SMB-клиент)</span><span class="dvbl">Узел 2 (SMB-сервер)</span></div></div>',
      pnl("Что можно делать с помощью SMB?", '<div class="lst">' + lrow("user", "Запускать, аутентифицировать и завершать сеансы") + lrow("folder", "Управлять доступом к файлам, каталогам и т.д.") +
          lrow("printer", "Использовать общие принтеры и другие ресурсы") + lrow("gear", "Разрешать приложению отправлять данные на другое устройство") + '</div>', "", 1), cls="as") +
    G("minmax(0,1fr) minmax(0,.8fr) minmax(0,1fr)",
      pnl("Как работает SMB?", SMB, "", 2),
      pnl("Совместные ресурсы", '<div class="lst">' + lrow("folder", "Файлы и каталоги", "", 2) + lrow("printer", "Принтеры", "", 2) + lrow("gear", "Приложения", "", 2) + lrow("user", "Другие сетевые ресурсы", "", 2) + '</div>', "", 2),
      pnl("Особенности SMB", '<div class="lst">' + lrow("link", "Долговременное подключение", "В отличие от FTP — постоянный сеанс: с удалёнными файлами работают как с локальными.", 3) +
          lrow("shield", "Безопасность", "Аутентификация пользователей и управление правами доступа.", 3) + lrow("layers", "Широкое применение", "Корпоративные и домашние сети.", 3) + '</div>', "", 3), style="margin-top:.8rem") +
    '<div class="mt">' + qt("SMB делает совместную работу в сети такой же удобной, как работу с локальными файлами.", 4) + '</div>')

# 51 ---------------------------------------------------------------- почтовые протоколы (s45)
MAIL0 = flow("mail0", "0 0 820 330", {
    "s": {"x": 90, "y": 80, "ic": "monitor", "label": "Отправитель", "sub": "почтовый клиент"},
    "r": {"x": 90, "y": 260, "ic": "monitor", "label": "Получатель", "sub": "почтовый клиент"},
    "i": {"x": 400, "y": 170, "ic": "cloud", "label": "Интернет", "r": 60},
    "m1": {"x": 720, "y": 70, "ic": "server", "label": "Сервер (отправляющий)"},
    "m2": {"x": 720, "y": 250, "ic": "server", "label": "Сервер (получающий)"}}, [
    {"a": "s", "b": "i", "pk": "SMTP", "col": "teal", "cap": "1 Клиент отправляет письмо на свой почтовый сервер (протокол SMTP)."},
    {"a": "i", "b": "m1", "pk": "SMTP", "col": "teal", "cap": "Письмо на отправляющем сервере."},
    {"a": "m1", "b": "m2", "pk": "SMTP", "col": "teal", "cap": "2 Почтовый сервер отправляет письмо через Интернет на сервер получателя (SMTP)."},
    {"a": "m2", "b": "i", "pk": "POP/IMAP", "col": "blue", "cap": "3 Получатель забирает письмо с почтового сервера по IMAP или POP…"},
    {"a": "i", "b": "r", "pk": "POP/IMAP", "col": "blue", "tag": {"r": "письмо получено"}, "cap": "…и читает его в почтовом клиенте."},
], links=[("s", "i"), ("r", "i"), ("i", "m1"), ("i", "m2"), ("m1", "m2")], wdef=1700)
slide("Почтовые протоколы", "", "", G("minmax(0,.8fr) minmax(0,1.8fr) minmax(0,.8fr)",
    '<div>' + ih("Почтовые", "протоколы", "отправка, хранение и получение электронных сообщений", inline=True) +
    '<div class="lst">' + lrow("mail", "Электронная почта", "Система для отправки, хранения и получения сообщений по сети. Письма хранятся на почтовых серверах в базах данных.", 1) +
    lrow("user", "Пользователи и серверы", "Пользователи обращаются к почтовым серверам; серверы взаимодействуют друг с другом для обмена письмами между доменами.", 1) + '</div></div>',
    MAIL0,
    pnl("Как это работает?", steps(["Клиент отправляет письмо на свой почтовый сервер (SMTP).", "Почтовый сервер отправляет письмо через Интернет на сервер получателя (SMTP).", "Получатель забирает письмо с помощью IMAP или POP."]), "", 1), cls="as") +
    G("repeat(3,minmax(0,1fr))",
      pnl("SMTP", '<div class="pns">Simple Mail Transfer Protocol</div>' + bul(["Отправка электронных сообщений.", "От почтового клиента к серверу и между почтовыми серверами.", "Передача писем между разными доменами."]), "", 2, ic="mail"),
      pnl("IMAP", '<div class="pns">Internet Message Access Protocol</div>' + bul(["Получение писем.", "Письма хранятся на сервере, клиент получает к ним доступ.", "Работа с письмами с нескольких устройств."]), "", 2, ic="db"),
      pnl("POP", '<div class="pns">Post Office Protocol</div>' + bul(["Получение писем.", "Письма загружаются с сервера на устройство (обычно с удалением с сервера).", "Подходит для работы с почтой с одного устройства."]), "", 2, ic="mail"), style="margin-top:.8rem") +
    '<div class="mt">' + qt("SMTP, IMAP и POP — основные протоколы, которые обеспечивают работу электронной почты.", 3, "gear") + '</div>')

# 52 ---------------------------------------------------------------- SMTP (s46)
slide("SMTP", "", "", G("minmax(0,.8fr) minmax(0,1.9fr)",
    '<div>' + ih("Работа протокола", "SMTP", "передача сообщений между почтовыми серверами", inline=True) +
    pnl("SMTP", '<div class="pns">Simple Mail Transfer Protocol</div><p class="p sm">Протокол для отправки электронных сообщений от клиента на почтовый сервер и между почтовыми серверами.</p>', "", 1, ic="mail") +
    pnl("Структура SMTP-сообщения", '<div class="lst">' + lrow("file", "Заголовок", "Строго определённый формат (RFC 2822)") + lrow("file", "Тело сообщения", "Текст произвольной длины") + '</div>', "", 1, ic="file") + '</div>',
    MAIL, cls="as") +
    G("repeat(4,minmax(0,1fr))",
      pnl("<span class='bn'>1</span> Установление соединения", '<div class="stgd">' + devsvg("laptop", "", "4rem") + '<div class="stga c-teal">' + mline("r", "teal") + '</div>' + devsvg("server", "", "2.6rem") + '</div>' +
          bul(["При отправке почтовый клиент устанавливает соединение с почтовым сервером по SMTP."]), "", 2),
      pnl("<span class='bn'>2</span> Передача сообщения", bul(["Клиент отправляет сообщение на почтовый сервер.", "Сервер проверяет, есть ли получатель в его списке: если да — доставляет; если нет — пересылает другому серверу (SMTP)."]), "", 2),
      pnl("<span class='bn'>3</span> Временное хранение", bul(["Сервер назначения недоступен — сообщение хранится на сервере и периодически отправляется повторно.", "Не доставлено за определённое время — возвращается отправителю с уведомлением."]), "amb", 2),
      pnl("<span class='bn'>4</span> Получение сообщения", bul(["Получатель забирает сообщение с сервера по IMAP или POP.", "IMAP оставляет письма на сервере, POP загружает на устройство (обычно с удалением)."]), "", 2), style="margin-top:.8rem") +
    '<div class="mt">' + qt("Поиск нужных почтовых серверов для пересылки происходит с помощью DNS — по записям MX.", 3, "dns") + '</div>')

# 53 ---------------------------------------------------------------- POP (s47)
POPX = ('<div class="pcmd" data-s="3">' + "".join(
    f'<div class="pl" style="--dl:{i*180}ms"><span class="sv">{a}</span><span class="dir {d}"></span><span class="cl">{b_}</span></div>' for i, (a, d, b_) in enumerate([
        ("+OK POP3 server ready", "l", ""), ("+OK User accepted", "l", "USER user@company.ru"), ("+OK Password accepted", "l", "PASS ********"), ("+OK 2 messages (3200 octets)", "l", "LIST"),
        ("+OK Message follows…", "l", "RETR 1"), ("+OK Message deleted", "l", "DELE 1"), ("", "r", "QUIT")])) + '</div>')
slide("POP", "", "", G("minmax(0,1.4fr) minmax(0,1fr)",
    ih("POP", "получение электронной почты", "", "Протокол POP (Post Office Protocol) используется для получения электронных сообщений с почтового сервера на устройство пользователя.", inline=True, big=True),
    info("POP позволяет загружать письма с почтового сервера на локальное устройство, обычно с использованием TCP (порт 110) или защищённого POP3S (порт 995).", "info", 0), cls="ac") +
    G("minmax(0,1.9fr) minmax(0,.8fr)", POPF,
      pnl("Этапы работы POP", steps(["Отправитель отправляет письмо на адрес получателя (SMTP).", "Письмо доставляется на почтовый сервер и хранится там.", "Клиент устанавливает соединение с сервером (POP).",
                                     "Сервер отправляет приветствие и ожидает команд.", "Клиент проходит аутентификацию и запрашивает список писем.", "Клиент загружает сообщения на своё устройство.",
                                     "После получения сообщение удаляется с почтового сервера."]), "", 1), cls="as") +
    G("minmax(0,1fr) minmax(0,1.2fr) minmax(0,1fr)",
      pnl("Основные особенности", '<div class="lst">' + lrow("file", "Загрузка писем на локальное устройство", "", 2) + lrow("cross", "Удаление писем с сервера после получения", "", 2) +
          lrow("lock", "Простой протокол, минимальный набор команд", "", 2) + lrow("gear", "TCP 110 или POP3S 995", "", 2) + '</div>', "", 2),
      pnl("Пример обмена командами", '<div class="G" style="--gc:1fr 1fr"><b class="dimp">Сервер</b><b class="dimp" style="text-align:right">Клиент</b></div>' + POPX, "", 3),
      pnl("Важно знать", '<div class="lst">' + lrow("warn", "Письма удаляются с сервера", "Это может быть критично для компаний малого бизнеса.", 4, cls="bad") +
          lrow("user", "Для индивидуального использования", "Когда письма нужны только на одном устройстве.", 4) + lrow("server", "Хранить письма на сервере", "Используйте IMAP.", 4) + '</div>', "", 4), style="margin-top:.8rem") +
    '<div class="mt">' + qt("POP — простой и надёжный способ получить почту, но после загрузки письма остаются только у вас.", 5) + '</div>')

# 54 ---------------------------------------------------------------- IMAP (s48)
slide("IMAP", "", "", G("minmax(0,1.4fr) minmax(0,1fr)",
    ih("Работа протокола", "IMAP", "получение и управление электронными сообщениями на сервере", inline=True),
    info("IMAP (Internet Message Access Protocol) позволяет получать сообщения с почтового сервера, оставляя их копии на сервере.", "info", 0), cls="ac") +
    IMAPF +
    G("repeat(4,minmax(0,1fr))",
      pnl("Что такое IMAP?", '<p class="p sm">Протокол прикладного уровня для получения и управления электронными сообщениями на почтовом сервере.</p>' + lrow("server", "TCP 143", "IMAP использует порт TCP 143."), "", 1),
      pnl("Как это работает?", steps(["Отправитель отправляет письмо на почтовый сервер (SMTP).", "Письмо сохраняется на сервере получателя.", "Получатель подключается по IMAP и получает копию сообщения.", "Исходное сообщение остаётся на сервере, пока пользователь не удалит его вручную."]), "", 1),
      pnl("Особенности IMAP", '<div class="lst">' + lrow("cloud", "", "Пользователь получает копию, оригинал остаётся на сервере.") + lrow("server", "", "Работа с письмами с нескольких устройств.") +
          lrow("desk", "", "Изменения (прочитано, удалено) синхронизируются.") + lrow("gear", "", "Удаление сообщения — и на устройстве, и на сервере.") + '</div>', "", 1),
      pnl("Преимущества", bul(["Доступ к почте с любого устройства.", "Синхронизация писем и папок.", "Удобное управление сообщениями на сервере.", "Для пользователей, работающих с почтой на нескольких устройствах."]), "grn", 1), style="margin-top:.8rem") +
    '<div class="mt">' + qt("IMAP — удобное решение для тех, кто хочет иметь доступ к своей почте с разных устройств, сохраняя письма на сервере.", 2, "info") + '</div>')

# 55 ---------------------------------------------------------------- синхронизация времени (s49)
CLOCK = ('<svg class="clockbig" viewBox="-110 -110 220 220" aria-hidden="true" data-s="1" data-w="2600"><circle r="100" class="glb"/><circle r="84" class="gll"/>' +
         "".join(f'<line x1="0" y1="-92" x2="0" y2="-80" class="sln" transform="rotate({i*30})"/>' for i in range(12)) +
         '<line class="hand h1" x1="0" y1="0" x2="0" y2="-48" style="stroke-width:6"/><line class="hand h2" x1="0" y1="0" x2="0" y2="-72" style="stroke-width:4"/><circle r="6" fill="#7ef5e2"/></svg>')
slide("Синхронизация времени", "", "", G("minmax(0,1.6fr) minmax(0,1fr)",
    ih("Требования к синхронизации", "времени", "единое время — основа стабильной и эффективной работы сети", inline=True),
    qt("Во многих сценариях в корпоративных кампусных сетях требуется последовательная синхронизация всех устройств.", 0), cls="ac") +
    G("minmax(0,1fr) minmax(0,.8fr) minmax(0,1fr)",
      '<div class="lst">' + pnl("Управление сетью", '<p class="p sm">Анализ журналов или сообщений отладки, собранных от различных маршрутизаторов, требует времени для обработки: единое время позволяет выстроить последовательность событий.</p>' +
                                code(['<span class="k">LOG</span> 10:24:03', '<span class="k">LOG</span> 10:24:07', '<span class="k">LOG</span> 10:24:11'], 2), "", 2, ic="desk") +
      pnl("Совместная работа систем", '<p class="p sm">Несколько систем, работающих вместе над одним сложным событием, используют один синхронизирующий сигнал, чтобы обеспечить правильную последовательность реализации.</p>', "", 2, ic="gear") + '</div>',
      '<div>' + CLOCK + '<div class="card pn" data-s="1" style="text-align:center"><h3 style="font-size:1.6rem;color:#fff">Синхронизация времени</h3><p class="p sm" style="margin:0">Единое время для надёжной работы</p></div></div>',
      '<div class="lst">' + pnl("Система тарификации", '<p class="p sm">Часы всех устройств должны быть согласованными: точное время нужно для учёта ресурсов и выставления счетов.</p>', "", 3, ic="db") +
      pnl("Инкрементное резервное копирование", '<p class="p sm">Часы на сервере резервного копирования и клиентах должны быть синхронизированы — чтобы правильно определить изменённые файлы.</p>', "", 3, ic="db") + '</div>', cls="ac") +
    G("minmax(0,1fr) minmax(0,1.2fr)",
      pnl("Системное время", '<p class="p sm">Некоторым приложениям необходимо знать время входа пользователей в систему и время изменения файлов.</p>', "", 4, ic="user"),
      '<div class="G" style="--gc:1fr 1fr" data-s="4">' + pnl("Вход в систему", '<table class="tbl2"><tr><td>user1</td><td>09:15:22</td></tr><tr><td>user2</td><td>10:03:47</td></tr><tr><td>user3</td><td>11:28:19</td></tr></table>', "", 0) +
      pnl("Изменение файлов", '<table class="tbl2"><tr><td>config.txt</td><td>09:42:11</td></tr><tr><td>data.db</td><td>10:17:36</td></tr><tr><td>report.pdf</td><td>11:05:03</td></tr></table>', "", 0) + '</div>', style="margin-top:.8rem") +
    '<div class="mt">' + qt("Точное и единое время — необходимое условие для безопасности, отказоустойчивости и эффективного управления сетью.", 5, "gear") + '</div>')

# 56 ---------------------------------------------------------------- NTP (s50)
slide("NTP", "", "", G("minmax(0,1.2fr) minmax(0,1fr)",
    ih("NTP", "иерархическая структура серверов времени", "", "Синхронизация времени в сети для обеспечения безопасности, диагностики и управляемости.", inline=True, big=True),
    info("Устройства используют программные часы, запускаемые при загрузке. Время можно ввести вручную командой или получить по <b>NTP</b>: все устройства получают одинаковые настройки от NTP-сервера.", "info", 0), cls="ac") +
    G("minmax(0,2fr) minmax(0,.9fr)", NTP,
      '<div class="lst">' + pnl("Ключевые особенности NTP", '<div class="lst">' + lrow("clock", "Синхронизация времени", "Одинаковое время важно для безопасности и диагностики.") +
                                lrow("layers", "Иерархическая структура", "Каждая ступень — часовой слой (stratum); чем меньше номер, тем ближе к точному источнику.") +
                                lrow("shield", "Надёжность", "Серверы одного уровня равноправны: резервирование и проверка точности.") + lrow("gear", "Простая настройка", "Вручную или с помощью NTP.") + '</div>', "", 1) +
      pnl("Номера часовых слоёв (stratum)", '<div class="lst">' + '<div class="lrow"><span class="nb">0</span><span>Точные источники времени (атомные часы, GPS)</span></div>'
          '<div class="lrow"><span class="nb">1</span><span>Серверы, подключённые к stratum 0</span></div><div class="lrow"><span class="nb" style="width:3.2rem">2–15</span><span>Серверы и клиенты, получающие время от вышестоящих слоёв</span></div>'
          '<div class="lrow bad"><span class="nb" style="background:var(--red)">16</span><span>Недоверенный слой (время не синхронизировано)</span></div></div>', "", 2) + '</div>', cls="as") +
    G("minmax(0,1fr) minmax(0,1.4fr)", pnl("", '<div class="G ac" style="--gc:auto 1fr">' + hexicon("check", "hx lg") + '<div><h3>Результат</h3><p class="p sm" style="margin:0">Все устройства сети имеют одинаковое время: это упрощает управление, повышает безопасность и облегчает поиск причин событий.</p></div></div>', "", 3),
      qt("Точное время в сети — фундамент надёжной и безопасной инфраструктуры.", 3), style="margin-top:.8rem"))

# 57 ---------------------------------------------------------------- атомные часы (s51) — реальное фото платы с выносками
slide("Атомные часы", "", "", G("minmax(0,1.3fr) minmax(0,1fr)", ih("Современные", "атомные часы", "высокая точность · стабильность · надёжность", inline=True),
      info("Атомные часы — устройства, использующие стабильные колебания атомов для высокоточного измерения времени. Это источник слоя 0 в иерархии NTP.", "atom", 0), cls="ac") +
      G("minmax(0,.8fr) minmax(0,2fr) minmax(0,.8fr)",
        '<div class="lst">' + pnl("Модуль атомных часов", '<div class="pns">Orolia Spectratime mRO-50</div><p class="p sm">Высокоточный модуль, использующий стабильные колебания атомов рубидия для точного и стабильного времени.</p>' +
                                  '<div class="lst">' + lrow("target", "Высокая точность", "до нс") + lrow("shield", "Долговременная стабильность") + lrow("gear", "Надёжная работа", "в различных условиях") + '</div>', "", 1, ic="atom") + '</div>',
        '<figure class="card ph" data-s="0" style="margin:0"><img src="img7app/s51_board.jpg" alt="Плата модуля атомных часов Orolia mRO-50" style="max-height:56vh"></figure>',
        '<div class="lst">' + pnl("Процессор / ПЛИС", '<div class="pns">Intel Cyclone 10</div><p class="p sm">Обработка сигналов, синхронизация и управление модулем атомных часов.</p>', "", 2, ic="gear") +
        pnl("Интерфейсы", '<div class="pns">SMA-разъёмы</div><p class="p sm">Подключение внешних антенн и интерфейсов синхронизации (например, 1PPS, 10 MHz).</p>', "", 2, ic="radio") +
        pnl("Дополнительный модуль", '<div class="pns">Приёмник GNSS (например, u-blox)</div><p class="p sm">Резервная синхронизация и повышение надёжности системы.</p>', "", 2, ic="sat") + '</div>', cls="ac") +
      '<div class="mt">' + irow([("clock", "Точное время"), ("link", "Стабильная работа"), ("shield", "Проверенные технологии")], 3) + '</div>')

# 58–62 ---------------------------------------------------------------- тренажёры, проверь себя, вопросы, до свидания
slide("Тренажёр: протоколы", "", "", ih("Тренажёр", "какой протокол и какой порт", inline=True) + '<div class="two even">' + trn("t1", "Задача — протокол", "Новая задача") + trn("t2", "Порт — протокол", "Другой порт") + '</div>')
slide("Тренажёр: DHCP и DNS", "", "", ih("Тренажёр", "адреса DHCP и части доменного имени", inline=True) + '<div class="two even">' + trn("t3", "Адреса в сообщениях DHCP", "Следующий вопрос") + trn("t4", "Части доменного имени", "Следующая часть") + '</div>')
slide("Проверь себя", "", "", ih("Проверь", "себя", "12 вопросов с разбором", inline=True, big=True) + '<div class="two mid"><div class="card quiz">'
      '<div class="qtop mono"><span id="qz-n">1 / 12</span><span id="qz-sc">верно: 0</span></div><div class="tq" id="qz-q"></div>'
      '<div class="opts col" id="qz-o"></div><div class="tres" id="qz-e" aria-live="polite"></div>'
      '<div class="trow"><button class="btn" id="qz-pv" type="button">Предыдущий</button><button class="btn pri" id="qz-nx" type="button">Следующий вопрос</button></div></div>'
      '<div class="side">' + info("Выберите ответ — сразу появится разбор. Вопросы охватывают FTP, TFTP, DNS, DHCP, почту и NTP.", "info", 0) + '<div class="relbox" style="min-height:16rem">' + globe_deco("gdeco g-c") + '</div></div></div>')
slide("Вопросы", "", "", ih("Вопросы", "для обсуждения", inline=True, big=True) + G("repeat(3,minmax(0,1fr))", *[pnl(f"<span class='bn'>{i+1:02d}</span>", p(q, cls="p"), "", 1, ic=ic) for i, (q, ic) in enumerate([
    ("Почему DNS-сервер провайдера отвечает роутеру с флагом AA=0, хотя данные верные?", "dns"), ("Что изменится в пути DNS-запроса, если запись уже есть в кэше роутера?", "router"),
    ("Какой режим FTP выбрать, если клиент за NAT, и почему?", "folder"), ("Зачем клиенту ARP-запрос после DHCPACK, если сервер уже проверял адрес ICMP-запросом?", "warn"),
    ("Почему DHCP-сообщения не проходят через маршрутизатор без DHCP relay?", "link"), ("Когда удобнее POP, а когда IMAP?", "mail")])]))
slide("До свидания", "", "", f"""
<div class="title bye">{TITLE_ART}
  <div class="kick"><span class="nb">07</span>Глава 7 · уровень приложений</div>
  <h1>Спасибо<br><span class="o2">за внимание!</span></h1>
  <p class="lead">До свидания! Повторите путь DNS-запроса и этапы DHCP — они понадобятся в лабораторной работе.</p>
  <p class="authors">Ананко Софья Михайловна<br>Качур Анна Юрьевна</p>
</div>""", "tslide")
