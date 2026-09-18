
# 19 ---------------------------------------------------------------- WWW (s15)
def _wmap():
    pts = [(120, 90), (360, 60), (560, 110), (620, 250), (420, 290), (170, 250), (300, 210)]
    b = ['<path class="wmap" d="M40 120l60-40 80 10 40-30 70 20 30-30 90 10 60 40 90-10 40 50-30 60-80 20-40 60-70 10-40-40-60 20-50 70-60-20-10-60-70-10-40-50z"/>']
    els = {}
    for i, (x, y) in enumerate(pts):
        b.append(f'<g transform="translate({x} {y}) scale(.5)">{dev("laptop", "page")}</g>')
        eid = f"wm{i}"
        b.append(f'<g class="arw" data-id="{eid}"><path class="dr wt dsh" pathLength="1" d="M380 170Q{(380 + x) / 2} {min(y, 170) - 60} {x} {y - 20}"/></g>')
        els[eid] = {"c": {0: "", 1 + i // 2: "on"}}
    b.append(f'<g transform="translate(380 175) scale(1.5)">{dev("cloud", "WWW")}</g>')
    sc = scene("wmap", 4, els, {i: 700 for i in range(5)})
    return f'<div {sc}><svg class="mini" viewBox="0 0 720 330" aria-hidden="true">{"".join(b)}</svg></div>'
slide("WWW", "", "", G("minmax(0,.8fr) minmax(0,1.7fr)",
    '<div>' + ih("WWW", "всемирная паутина", "", "<b class='hl'>Глобальный доступ к информации.</b> На начальном этапе развития Интернета для обмена документами предлагалось использовать Всемирную паутину (World Wide Web, WWW).", big=True) +
    G("repeat(3,minmax(0,1fr))", tile("globe", "Глобальный доступ", "", "plain"), tile("link", "Объединяет людей", "", "plain"), tile("shield", "Основа Интернета", "", "plain")) + '</div>',
    pnl("Мировая сеть в действии", _wmap() + '<div class="rtag">Документы доступны повсюду</div>', "", 0), cls="as") +
    G("minmax(0,1.1fr) minmax(0,.9fr) minmax(0,1fr)",
      pnl("Из чего состоит WWW?", '<div class="plus">' + tile("file", "HTML", "язык гипертекстовой разметки для отображения документа в браузере", "amb", 2) + '<span>+</span>' +
          tile("file", "HTTP", "протокол передачи документов по сети", "blue", 2, 150) + '<span>+</span>' + tile("link", "URL", "адреса для указания местоположения документов", "vio", 2, 300) + '</div>', "", 2),
      pnl("Как это работает?", steps(["Пользователь вводит URL-адрес в браузере.", "Браузер отправляет HTTP-запрос на веб-сервер.", "Веб-сервер обрабатывает запрос и отправляет ответ (HTML-страницу, изображения).", "Браузер получает данные и отображает веб-страницу."], 3), "", 3),
      pnl("Что такое WWW сейчас", '<p class="p sm">WWW на самом деле было названием клиентского приложения для просмотра HTML-документов, а теперь представляет собой набор технологий <b>(HTML + HTTP + URL-адрес)</b> и широко известен как Интернет.</p>' +
          '<div class="urlbar"><i></i><i></i><i></i>https://www.example.com/index.html</div>', "", 3), style="margin-top:.8rem") +
    '<div class="mt">' + qt("Всемирная паутина делает знания, информацию и возможности доступными для каждого — в любой точке мира.", 4) + '</div>')

# 20 ---------------------------------------------------------------- HTTP доступ к веб-страницам (s14)
HTTPW = ('<svg class="mini" viewBox="0 0 760 300" aria-hidden="true">'
         f'<g transform="translate(120 170) scale(1.6)">{dev("laptop", "page")}</g><g transform="translate(600 160) scale(1.6)">{dev("server")}</g>'
         f'<g transform="translate(360 150) scale(1.15)">{dev("cloud")}</g><text x="360" y="146" text-anchor="middle" style="font-family:var(--hf)">Интернет</text><text x="360" y="162" text-anchor="middle" class="ml2" fill="#8fb8b0">(IP-сеть)</text>'
         '<text x="120" y="40" text-anchor="middle" style="font-family:var(--hf)">Браузер (HTTP-клиент)</text><text x="600" y="40" text-anchor="middle" style="font-family:var(--hf)">Веб-сервер (HTTP-сервер)</text>'
         + arrow("hw1", 220, 92, 520, 92, "blue") + arrow("hw2", 520, 236, 220, 236, "red") +
         '<g class="an" data-id="hwt1"><text x="370" y="80" text-anchor="middle" style="font-family:var(--hf);fill:#4aa8ff">1  HTTP-запрос</text></g>'
         '<g class="an" data-id="hwt2"><text x="370" y="262" text-anchor="middle" style="font-family:var(--hf);fill:#ff5c6e">2  HTTP-ответ: HTML, изображения…</text></g></svg>')
HTTPW_SC = scene("hw", 2, {"hw1": {"c": {0: "", 1: "on"}}, "hw2": {"c": {0: "", 2: "on"}}, "hwt1": {"o": {0: 0, 1: 1}}, "hwt2": {"o": {0: 0, 2: 1}}}, {1: 1200, 2: 1200})
slide("Доступ к веб-странице", "", "", G("minmax(0,.8fr) minmax(0,1.5fr) minmax(0,.45fr)",
    '<div>' + ih("HTTP", "доступ к веб-страницам", "", "При вводе URL браузер получает данные с веб-сервера и отображает контент на странице.", big=True) +
    G("repeat(3,minmax(0,1fr))", tile("globe", "Простой доступ", "по URL-адресу", "plain"), tile("target", "Высокая скорость", "", "plain"), tile("shield", "Широкое применение", "основа веб-сервисов", "plain")) + '</div>',
    pnl("Как это работает?", f'<div {HTTPW_SC}>{HTTPW}</div>', "", 0),
    pnl("Ресурсы сервера", '<div class="lst">' + lrow("file", "HTML") + lrow("img", "Картинки") + lrow("video", "Видео") + lrow("db", "Другие файлы") + '</div>', "", 1), cls="as") +
    G("minmax(0,1fr) minmax(0,1.2fr) minmax(0,.9fr)",
      pnl("Что такое HTTP?", '<div class="pnh">' + hexicon("file", "hx lg") + '<p class="p sm" style="margin:0"><b class="hl">HTTP (HyperText Transfer Protocol)</b> — протокол прикладного уровня для связи между клиентским браузером или другой программой и веб-сервером. Основан на типовой архитектуре клиент/сервер и использует TCP для передачи.</p></div>', "", 2),
      pnl("URL-адрес", '<p class="p sm"><b class="hl">URL</b> однозначно определяет местонахождение веб-страницы или других ресурсов в Интернете. URL может содержать имя страницы гипертекста — обычно с расширением <b>.html</b> или <b>.htm</b>.</p>' + URLBAR.replace('data-id="url"', 'data-id="url0" class="url split"', 1).replace('class="url" ', ''), "", 2),
      pnl("Протоколы передачи", '<div class="lst">' + lrow("globe", "HTTP", "Передача веб-страниц") + lrow("lock", "HTTPS", "Безопасная передача данных") + lrow("link", "TCP", "Надёжная доставка данных") + lrow("globe", "IP", "Адресация и маршрутизация") + '</div>', "", 2), style="margin:.8rem 0") +
    G("minmax(0,1.5fr) minmax(0,1fr)",
      pnl("Основные этапы загрузки страницы", '<div class="chain">' + "".join(f'<div class="tile plain" data-s="3" style="--dl:{i*150}ms">{hexicon(ic, "hx")}<b>{t}</b></div>' for i, (ic, t) in enumerate([("target", "Ввод URL в браузере"), ("file", "Отправка HTTP-запроса"), ("server", "Обработка запроса на сервере"), ("file", "Получение данных (HTML)"), ("desk", "Отображение страницы")])) + '</div>', "", 3),
      qt("HTTP делает интернет доступным для всех — до сложных облачных сервисов.", 4)))

# 21 ---------------------------------------------------------------- HTTP запрос-ответ, методы, HTTPS (s17)
REQ = code(['<span class="k">GET</span> /index.html <span class="v">HTTP/1.1</span>', '<span class="d">Host:</span> www.example.com', '<span class="d">User-Agent:</span> Mozilla/5.0', '<span class="d">Accept:</span> text/html'], 5)
RSP = code(['<span class="v">HTTP/1.1</span> <span class="g">200 OK</span>', '<span class="d">Content-Type:</span> text/html', '<span class="d">Content-Length:</span> 1024', '', '&lt;html&gt; … &lt;/html&gt;'], 5)
MINI_HACK = ('<svg class="mini" viewBox="0 0 320 150" aria-hidden="true">'
             f'<g transform="translate(40 60) scale(.7)">{dev("laptop")}</g><g transform="translate(280 60) scale(.7)">{dev("server", "", "red")}</g>'
             f'<g transform="translate(160 118) scale(.55)">{dev("hacker")}</g><path class="lk2" style="stroke:var(--red)" d="M80 60H240 M160 60V92"/>'
             '<text x="160" y="146" text-anchor="middle" style="fill:#ff5c6e;font-size:12px">Перехват данных</text></svg>')
MINI_SEC = ('<svg class="mini" viewBox="0 0 320 110" aria-hidden="true">'
            f'<g transform="translate(40 55) scale(.7)">{dev("laptop")}</g><g transform="translate(280 55) scale(.7)">{dev("server")}</g>'
            '<path class="lk2" style="stroke:var(--green);stroke-dasharray:none" d="M80 55H240"/><path class="scri" style="stroke:var(--green)" d="M150 50h20v16h-20z M154 50v-6a6 6 0 0 1 12 0v6"/>'
            '<text x="160" y="100" text-anchor="middle" style="fill:#8ce36a;font-size:12px">Зашифрованное соединение</text></svg>')
def meth(n, sub, d, cl, col, ic):
    return (f'<div class="card pn {col}" data-s="2"><div class="pnh">{hexicon(ic, "hx")}<div><h3 style="margin:0">{n}</h3><div class="pns" style="margin:0">{sub}</div></div></div>'
            f'<p class="p sm">{d}</p><div class="code" style="padding:.4rem .6rem">{cl}</div></div>')
slide("HTTP: методы", "", "", G("minmax(0,.9fr) minmax(0,1.2fr) minmax(0,.8fr)",
    ih("HTTP", "протокол запрос-ответ", "", "HTTP работает по принципу «запрос-ответ»: клиент (браузер) отправляет запрос на сервер, а сервер возвращает ответ с данными (веб-страницей, изображением и т.д.).", big=True),
    HTTPM,
    pnl("Основные особенности", '<div class="lst">' + lrow("target", "Простой и понятный протокол") + lrow("file", "Работает по модели клиент/сервер") + lrow("info", "Передаёт данные в открытом виде (без шифрования)") + '</div>', "", 1), cls="ac") +
    G("minmax(0,1.6fr) minmax(0,1fr) minmax(0,1fr)",
      pnl("Методы HTTP (запросы клиента)", G("repeat(3,minmax(0,1fr))",
          meth("GET", "Получение данных", "Извлечение данных с сервера. Например, при вводе URL в браузере отправляется GET-запрос для получения страницы.", "GET /index.html HTTP/1.1", "blue", "target"),
          meth("PUT", "Отправка и обновление ресурсов", "Создание новых ресурсов или обновление существующих: профиль пользователя, изменения в документах.", "PUT /user/profile HTTP/1.1", "grn", "file"),
          meth("POST", "Отправка данных", "Передача больших объёмов данных. Повторные POST-запросы могут создать несколько одинаковых ресурсов.", "POST /upload HTTP/1.1", "vio", "file")), "", 2),
      pnl("HTTP — небезопасный протокол", '<p class="p sm">Сообщения запроса/ответа передаются открытым текстом, без шифрования: нарушители могут перехватывать данные пользователей.</p>' + MINI_HACK, "red", 3),
      pnl("HTTPS — безопасное решение", '<p class="p sm">HTTPS (HTTP Secure) обеспечивает <b class="hl">аутентификацию и шифрование</b> данных между узлами.</p>' + MINI_SEC +
          G("repeat(3,minmax(0,1fr))", tile("shield", "Аутентификация", "", "plain", 4), tile("lock", "Шифрование", "", "plain", 4), tile("shield", "Защита от перехвата", "", "plain", 4)), "grn", 4), style="margin:.8rem 0") +
    G("minmax(0,1fr) minmax(0,1fr) minmax(0,1fr)", pnl("Пример HTTP-запроса", REQ, "", 5), pnl("Пример HTTP-ответа", RSP, "", 5),
      pnl("Порты и протоколы", '<div class="ports"><div><span class="pb">80</span><b>HTTP</b> — передача данных без шифрования</div><div><span class="pb blue">443</span><b>HTTPS</b> — безопасная передача (шифрование TLS)</div></div>' +
          '<div class="mt">' + qt("HTTPS — тот же HTTP, но с защитой.", 5) + '</div>', "", 5)))
slide("HTTPS: перехват", "", "", G("minmax(0,.8fr) minmax(0,1.5fr)",
    ih("HTTP небезопасен,", "HTTPS — решение", "анимация перехвата",
       "К сожалению, протокол HTTP не обеспечивает безопасности: сообщения передаются открытым текстом без шифрования. Для защищённого обмена была придумана модификация HTTPS (HTTP Secure) — аутентификация и шифрование данных между узлами."),
    HTTPS, cls="ac"))

# 23 ---------------------------------------------------------------- пять шагов по пакетам
slide("Пять шагов: по пакетам", "", "", ih("Как открывается", "веб-страница", "каждый пакет: MAC, IP, порты",
      "При введении веб-адреса (например, https://www.eltex-co.ru/index.html) браузер устанавливает сеанс связи по протоколу HTTP с веб-сервисом на сервере. Справа — поля пакета на каждом участке.", inline=True) + WEB)

# 24 ---------------------------------------------------------------- как работает HTTP (s18)
def col5(n, t, d, vis, foot_ic, foot_t, foot_d, s):
    return (f'<div class="card pn c5" data-s="{s}" data-w="1100"><div class="pnh"><span class="nb">{n:02d}</span><h3 style="text-transform:uppercase">{t}</h3></div><p class="p sm">{d}</p>'
            f'<div class="c5v">{vis}</div><div class="lrow">{hexicon(foot_ic, "hx sm")}<div><b class="hl">{foot_t}</b><span>{foot_d}</span></div></div></div>')
V1 = ('<div class="urlbar"><i></i><i></i><i></i>https://www.eltex-co.ru/index.html</div><div class="lst" style="margin-top:.5rem">'
      '<div class="G ac" style="--gc:auto 1fr"><span class="chip">https</span><small class="dimp">Протокол</small><span class="chip">www.eltex-co.ru</span><small class="dimp">Имя сервера</small><span class="chip">index.html</span><small class="dimp">Запрашиваемый файл</small></div></div>')
V2 = '<div class="G ac" style="--gc:auto 1fr">' + devsvg("dns", "", "4.5rem") + '<div class="lst"><span class="chip">www.eltex-co.ru</span><span class="chip amb">62.109.1.166</span></div></div>'
V3 = '<div class="G ac" style="--gc:auto 1fr">' + devsvg("laptop", "", "4.5rem") + code(["GET /index.html HTTP/1.1", "Host: www.eltex-co.ru", "User-Agent: …", "Accept: …"], 0) + '</div>'
V4 = '<div class="G ac" style="--gc:auto 1fr">' + devsvg("server", "", "3.6rem") + code(['<span class="g">HTTP/1.1 200 OK</span>', "Content-Type: text/html", '<span class="k">&lt;!DOCTYPE html&gt;</span>', '<span class="k">&lt;html&gt;…&lt;/html&gt;</span>'], 0) + '</div>'
V5 = devsvg("laptop", "page", "9rem")
slide("Как работает HTTP", "", "", G("minmax(0,1fr) minmax(0,1.2fr)",
    ih("Как работает", "HTTP", "от ввода адреса до отображения веб-страницы", big=True),
    info("<b>HTML</b> — стандартизированный язык гипертекстовой разметки документов для просмотра веб-страниц в браузере. Он нужен, чтобы браузер понимал, как отобразить ту или иную веб-страницу.", "file", 0), cls="ac") +
    G("repeat(5,minmax(0,1fr))",
      col5(1, "Ввод URL и разбор адреса", "Браузер делит веб-адрес на три части: протокол, имя сервера и запрашиваемый файл.", V1, "globe", "URL", "протокол, имя, файл", 1),
      col5(2, "Имя в IP-адрес", "Браузер преобразует имя сервера в IP-адрес, с помощью которого устанавливается соединение с сервером.", V2, "globe", "DNS", "преобразует имя в IP-адрес", 2),
      col5(3, "Отправка HTTP-запроса", "Браузер отправляет запрос GET и запрашивает нужный файл (index.html — страница по умолчанию).", V3, "mail", "HTTP-запрос (GET)", "запросить файл с сервера", 3),
      col5(4, "Ответ с сервера", "Сервер отправляет запрашиваемый файл с HTML-кодом веб-сайта.", V4, "folder", "HTTP-ответ", "файл с HTML-кодом", 4),
      col5(5, "Отображение страницы", "Браузер преобразует принятый HTML-код и формирует страницу в окне браузера.", V5, "desk", "Браузер", "формирует веб-страницу", 5)) +
    G("auto 1fr auto 1fr auto", devbox("laptop", "Клиент (браузер)", "", "", "5rem", 6),
      f'<div class="ar c-teal" data-s="6" style="text-align:center;font-family:var(--hf)">HTTP: запрос{mline("r", "teal")}</div>', devsvg("globe", "", "4rem"),
      f'<div class="ar c-teal" data-s="7" style="text-align:center;font-family:var(--hf)">{mline("l", "teal")}HTTP: ответ</div>', devbox("server", "Сервер (веб-сервис)", "", "", "3.5rem", 6), cls="ac", style="margin-top:.8rem"))

# 25 ---------------------------------------------------------------- как открывается веб-страница (s31)
OPEN = flow("open", "0 0 1000 420", {
    "u": {"x": 110, "y": 250, "ic": "laptop", "label": "Пользователь", "scr": "page", "r": 52},
    "n": {"x": 440, "y": 250, "ic": "pc", "label": "Узел (клиент)", "scr": "globe", "r": 52},
    "d": {"x": 700, "y": 90, "ic": "dns", "label": "DNS-сервер"},
    "w": {"x": 890, "y": 280, "ic": "server", "label": "WEB-сервер", "sub": "www.eltex-co.ru"}}, [
    {"a": "u", "b": "n", "pk": "1 Ввод URL", "col": "blue", "cap": "Пользователь вводит в браузере адрес www.eltex-co.ru — формируется HTTP-запрос. В запросе указывается URL: протокол, доменное имя и путь к ресурсу."},
    {"hl": ["n"], "tag": {"n": "DNS-кэш: нет"}, "cap": "Компьютер проверяет DNS-кэш. Если запись есть — HTTP-запрос сразу уходит на IP-адрес из записи."},
    {"a": "n", "b": "d", "pk": "2 DNS-запрос", "col": "blue", "cap": "Записи нет — формируется и отправляется запрос на DNS-сервер с таблицей доменных имён и IP-адресов."},
    {"a": "d", "b": "n", "pk": "3 61.109.1.166", "col": "green", "cap": "DNS-сервер возвращает IP-адрес сайта. Компьютер использует его для завершения формирования HTTP-запроса."},
    {"a": "n", "b": "w", "pk": "3 GET /", "col": "blue", "cap": "Компьютер отправляет HTTP-запрос на IP-адрес веб-сервера."},
    {"a": "w", "b": "n", "pk": "4 HTML", "col": "green", "cap": "Сервер обрабатывает запрос и отправляет HTTP-ответ с HTML-страницей."},
    {"a": "n", "b": "u", "pk": "4 страница", "col": "green", "tag": {"u": "веб-страница"}, "cap": "Получив ответ от сервера, веб-браузер отображает веб-страницу."},
], links=[("u", "n"), ("n", "d"), ("n", "w")], wdef=2300)
slide("Как открывается веб-страница", "", "", G("minmax(0,1.3fr) minmax(0,1fr)",
    ih("Как открывается", "веб-страница?", "", "Рассмотрим обмен информацией между приложениями с использованием протоколов уровня приложений на примере загрузки сайта www.eltex-co.ru."),
    info("<b>URL (Uniform Resource Locator)</b> состоит из протокола, доменного имени и пути к ресурсу.<br><span class='chip amb'>https://</span> <span class='chip'>www.eltex-co.ru</span> <span class='chip vio'>/</span>", "info", 0), cls="ac") +
    OPEN + G("repeat(4,minmax(0,1fr))",
             pnl("<span class='bn'>01</span> Формирование запроса", '<p class="p sm">Пользователь вводит адрес <span class="hl">www.eltex-co.ru</span>. Формируется HTTP-запрос: URL из протокола, доменного имени и пути к ресурсу.</p>', "", 0),
             pnl("<span class='bn'>02</span> Получение IP-адреса", '<p class="p sm">Компьютер проверяет DNS-кэш. Записи нет — DNS-запрос; DNS-сервер возвращает IP-адрес сайта.</p>', "", 0),
             pnl("<span class='bn'>03</span> Запрос к web-серверу", '<p class="p sm">Компьютер отправляет HTTP-запрос на IP-адрес веб-сервера. Сервер обрабатывает запрос.</p>', "", 0),
             pnl("<span class='bn'>04</span> Получение и отображение", '<p class="p sm">Веб-сервер отправляет HTTP-ответ с HTML-страницей; браузер отображает её пользователю.</p>', "", 0), style="margin-top:.8rem"))

# 26 ---------------------------------------------------------------- HOSTS.txt (s19)
ARPA = ('<svg class="mini" viewBox="0 0 560 190" aria-hidden="true">' +
        "".join(f'<g transform="translate(50 {40 + i * 55}) scale(.5)">{dev("monitor")}</g><path class="lk2" d="M80 {40 + i * 55}L200 95"/>' for i in range(3)) +
        '<path class="fpg" d="M200 50h50l18 18v70h-68z M250 50v18h18"/><path class="sln" d="M212 80h40 M212 92h40 M212 104h40 M212 116h30"/>'
        '<text x="234" y="162" text-anchor="middle" style="font-family:var(--hf);font-size:15px">HOSTS.txt</text>'
        f'<g transform="translate(480 90) scale(.9)">{dev("server")}</g><text x="480" y="170" text-anchor="middle" style="font-family:var(--hf)">NIC</text>'
        + arrow("ah1", 300, 70, 430, 70, "teal") + arrow("ah2", 430, 120, 300, 120, "teal", dash=True) +
        '<text x="365" y="58" text-anchor="middle" style="font-size:11px">изменения по e-mail</text><text x="365" y="142" text-anchor="middle" style="font-size:11px">периодическое обновление</text></svg>')
ARPA_SC = scene("arpa", 2, {"ah1": {"c": {0: "", 1: "on"}}, "ah2": {"c": {0: "", 2: "on"}}}, {1: 1000, 2: 1000})
slide("От HOSTS.txt к DNS", "", "", G("minmax(0,.8fr) minmax(0,1.3fr) minmax(0,.8fr)",
    ih("От HOSTS.txt", "к DNS", "", "С ростом сети возникла необходимость в более масштабируемом и надёжном способе сопоставления имён и IP-адресов.", big=True),
    pnl("ARPANET: начало", f'<p class="p sm">ARPANET, предшественник Интернета, сопоставлял имена хостов с IP-адресами одним файлом HOSTS.txt. За него отвечал сетевой информационный центр (NIC).</p><div {ARPA_SC}>{ARPA}</div>', "", 0),
    pnl("Содержимое HOSTS.txt", code(['<span class="d"># IP-адрес    Имя хоста</span>', "10.0.0.1      host1", "10.0.0.2      host2", "10.0.0.3      host3", "…"], 0) +
        info("Файл HOSTS.txt содержит соответствие между именами хостов и их IP-адресами.", "info", 0), "", 1), cls="as") +
    G("minmax(0,1.1fr) minmax(0,1fr)",
      pnl("Проблемы при росте сети", '<p class="p sm">После перехода ARPANET на TCP/IP количество пользователей резко возросло. Поддерживать файл HOSTS.txt вручную стало очень сложно.</p>' +
          G("repeat(3,minmax(0,1fr))", tile("warn", "Конфликт имён", "Трудно гарантировать, что имена не совпадут с уже используемыми", "red", 2), tile("db", "Согласованность", "Имена могли измениться несколько раз до обновления файла", "blue", 2, 120),
            tile("layers", "Масштабируемость", "Ручное обновление не подходит для большой сети", "vio", 2, 240)), "", 2),
      pnl("Решение — DNS", '<p class="p sm">Поэтому была введена система доменных имён (DNS). Анимация ниже: как файл расходился по сети и где он ломался.</p>' + HOSTS, "", 3), style="margin:.8rem 0") +
    G("repeat(4,minmax(0,1fr))", lrow("gear", "Автоматизация", "Записи обновляются автоматически", 4), lrow("layers", "Иерархическая структура", "Распределённая система серверов", 4),
      lrow("shield", "Уникальность имён", "Исключает конфликты имён", 4), lrow("target", "Масштабируемость", "Миллионы доменов по всему миру", 4)) +
    '<div class="mt">' + qt("DNS — основа современного Интернета: надёжное и масштабируемое сопоставление имён хостов с IP-адресами.", 5) + '</div>')

# 27 ---------------------------------------------------------------- DNS (s20_1)
DNS3 = flow("dns3", "0 0 1000 300", {
    "u": {"x": 130, "y": 150, "ic": "laptop", "label": "Пользователь (браузер)", "scr": "globe", "r": 50},
    "d": {"x": 500, "y": 150, "ic": "dns", "label": "DNS-сервер", "r": 50},
    "w": {"x": 860, "y": 150, "ic": "server", "label": "WEB-сервер", "sub": "62.109.1.166", "r": 50}}, [
    {"a": "u", "b": "d", "pk": "Кто такой www.eltex-co.ru?", "col": "blue", "cap": "1 DNS-запрос: пользователь вводит доменное имя, браузер отправляет DNS-запрос на DNS-сервер."},
    {"a": "d", "b": "u", "pk": "62.109.1.166", "col": "violet", "cap": "2 DNS-ответ: DNS-сервер находит соответствие и отправляет пользователю IP-адрес домена."},
    {"a": "u", "b": "w", "pk": "HTTP/HTTPS к 62.109.1.166", "col": "teal", "curve": 90, "cap": "3 Доступ к веб-сайту: браузер использует полученный IP-адрес для соединения с веб-сервером."},
    {"a": "w", "b": "u", "pk": "веб-страница", "col": "green", "curve": -90, "cap": "Веб-сервер возвращает запрашиваемый ресурс."},
], links=[("u", "d")], wdef=2000)
slide("DNS: назначение", "", "", G("minmax(0,.7fr) minmax(0,1.8fr)",
    ih("DNS", "преобразование имён в IP-адреса", "", "DNS (Domain Name System) — система, которая сопоставляет доменные имена с IP-адресами, и наоборот.", big=True),
    '<div class="ibox" data-s="0">' + devsvg("globe", "", "4.5rem") + '<div>Вместо запоминания IP-адресов мы используем удобные доменные имена</div><div class="urlbar">https://www.eltex-co.ru</div><div>DNS переводит доменное имя в IP-адрес, например: <b>62.109.1.166</b></div></div>', cls="ac") +
    pnl("Как работает DNS?", '<div class="pns">Процесс получения IP-адреса по доменному имени</div>' + DNS3, "", 0) +
    G("minmax(0,1.1fr) minmax(0,.9fr) minmax(0,.8fr)",
      pnl("Зачем нужен DNS?", G("repeat(3,minmax(0,1fr))", tile("user", "Удобство", "Легко запомнить имя вместо числового адреса", "plain", 1),
                                tile("gear", "Гибкость", "Если IP-адрес изменится, пользователь этого не заметит", "plain", 1), tile("shield", "Масштабируемость", "Миллионы доменных имён", "plain", 1)), "", 1),
      pnl("DNS работает в обе стороны", G("1fr 1fr", tile("link", "Имя в IP-адрес", "www.eltex-co.ru<br>62.109.1.166", "blue", 2), tile("link", "IP-адрес в имя", "62.109.1.166<br>www.eltex-co.ru", "vio", 2)), "", 2),
      pnl("Важно", '<div class="lst">' + lrow("warn", "IP DNS-сервера", "Для работы разрешения имён на интерфейсе должен быть указан IP-адрес DNS-сервера.", 3) +
          lrow("file", "Раньше — HOSTS.txt", "С ростом сети поддерживать его вручную стало невозможно.", 3) + '</div>', "amb", 3), style="margin-top:.8rem") +
    '<div class="mt">' + qt("DNS делает Интернет удобным, надёжным и масштабируемым.", 4) + '</div>')

# 28 ---------------------------------------------------------------- как работает DNS (s20_2)
def dnsrow(n, t, d, vis, side_t, side_d, s):
    return (f'<div class="card pn drow" data-s="{s}" data-w="1500"><div class="G ac" style="--gc:auto minmax(0,.9fr) minmax(0,1.6fr) minmax(0,.9fr)">'
            f'<span class="nb" style="width:3.4rem;height:3rem;font-size:1.6rem">{n}</span><div><h3 class="uh">{t}</h3><p class="p sm">{d}</p></div>{vis}'
            f'<div class="ibox" style="display:block"><b style="font-family:var(--hf);text-transform:uppercase;color:#fff">{side_t}</b><div>{side_d}</div></div></div></div>')
def dvis(left, lab, col, d, right):
    return (f'<div class="G ac" style="--gc:auto 1fr auto">{devsvg(left[0], left[1], "7rem")}<div class="ar c-{col}" style="text-align:center">'
            f'<span class="chip {col}">{lab}</span>{mline(d, col)}</div>{devsvg(right, "", "4.6rem")}</div>')
slide("DNS: как работает", "", "", G("minmax(0,.55fr) minmax(0,2.2fr)",
    '<div>' + ih("DNS", "как работает DNS?", "", "DNS преобразует удобные для запоминания доменные имена в IP-адреса, позволяя устройствам находить нужные ресурсы в сети.", big=True) +
    pnl("", '<p class="p sm">Например: вместо запоминания IP-адреса <b>62.109.1.166</b> мы используем доменное имя <b class="hl">www.eltex-co.ru</b></p>', "", 0) +
    '<div class="mt">' + qt("DNS делает интернет удобным, надёжным и масштабируемым.", 0) + '</div></div>',
    '<div class="lst">' + dnsrow(1, "DNS-запрос", "Пользователь вводит доменное имя в браузере. Браузер формирует DNS-запрос к DNS-серверу.",
                                 dvis(("laptop", "globe"), "Кто такой www.eltex-co.ru?", "blue", "r", "dns"), "DNS-запрос", "Браузер отправляет запрос на разрешение доменного имени <b>www.eltex-co.ru</b>.", 1) +
    dnsrow(2, "DNS-ответ", "DNS-сервер сопоставляет доменное имя с его IP-адресом и отправляет пользователю DNS-ответ.",
           dvis(("laptop", "globe"), "www.eltex-co.ru = 62.109.1.166", "vio", "l", "dns"), "DNS-ответ", "DNS-сервер находит соответствие и отправляет IP-адрес домена: <b style='color:var(--violet)'>62.109.1.166</b>.", 2) +
    dnsrow(3, "Доступ к ресурсу", "Пользователь использует полученный IP-адрес для соединения с веб-сервером и доступа к ресурсу.",
           dvis(("laptop", "page"), "HTTP/HTTPS-запрос к 62.109.1.166", "teal", "r", "server"), "Веб-ресурс", "Браузер устанавливает соединение с веб-сервером по IP-адресу и получает ресурс (веб-страницу).", 3) + '</div>', cls="as"))

# 29 ---------------------------------------------------------------- путь DNS-запроса
slide("DNS: путь запроса", "", "", ih("Путь DNS-запроса", "от кэша до авторитетного сервера", "кэш ПК · роутер · провайдер · корень · TLD · авторитетный",
      "Компьютер спрашивает сначала себя, потом роутер, потом DNS-сервер провайдера, а тот — иерархию серверов. Справа — поля пакета на каждом участке.", inline=True) + DNSFULL)

# 30 ---------------------------------------------------------------- структура пакета DNS (s21)
DSEC2 = [("Header", "file", "Заголовок", "Служебная информация о пакете: идентификатор, флаги, количество записей и др. — 12 октетов.", "blue"),
         ("Question", "info", "Секция запроса", "Для какого имени и какой тип записи нужен. Сервер при ответе копирует эту информацию обратно.", "teal"),
         ("Answer", "mail", "Секция ответа", "Один или несколько ответов на запрос (например, IP-адрес).", "teal"),
         ("Authority", "server", "Секция ответа об уполномоченных серверах", "С помощью каких авторитетных серверов получена информация из секции ответа.", "blue"),
         ("Additional", "layers", "Секция ответа дополнительных записей", "Дополнительные записи, связанные с запросом, но не являющиеся строгими ответами.", "teal")]
slide("Структура пакета DNS", "", "", ih("Структура", "пакета DNS", "", "Все сообщения DNS имеют одинаковый формат: заголовок, вопрос, ответ. На DNS-серверах хранятся различные типы записей, содержащие имя, адрес и тип записи.", inline=True, big=True) +
      '<div class="relbox">' + globe_deco("gdeco g-r") + '<div class="dsec">' + "".join(
          f'<div class="dsrow" data-s="{i+1}" data-w="900"><div class="slab {"hi" if c == "blue" else ""}" style="--dl:0ms">{hexicon(ic, "hx sm")}<b>{n}</b></div><span class="dsl"></span>'
          f'<div class="ibox" style="display:block"><b style="color:var(--cyan)">{t}</b><div>{d}</div></div></div>' for i, (n, ic, t, d, c) in enumerate(DSEC2)) + '</div></div>')

# 31 ---------------------------------------------------------------- заголовок DNS (s22)
def cbox(t, d, s):
    return f'<div class="cbox" data-s="{s}"><b>{t}</b><span>{d}</span></div>'
HT = ('<div class="htab" data-s="1"><div class="hr full"><b>ID</b><small>16 бит</small></div><div class="hr bits8">' +
      "".join(f'<div style="flex:{w}"><b>{n}</b><small>{w} бит{"а" if w in (3, 4) else ""}</small></div>' for n, w in (("QR", 1), ("Opcode", 4), ("AA", 1), ("TC", 1), ("RD", 1), ("RA", 1), ("Z", 3), ("Rcode", 4))) +
      '</div>' + "".join(f'<div class="hr full"><b>{n}</b><small>16 бит</small></div>' for n in ("QDCOUNT", "ANCOUNT", "NSCOUNT", "ARCOUNT")) + '</div>')
slide("Заголовок DNS", "", "", G("minmax(0,1fr) minmax(0,1.2fr)", ih("Структура", "заголовка DNS", big=True), '<p class="p">Заголовок DNS содержит служебную информацию о запросе или ответе.</p>', cls="ac") +
      G("minmax(0,.6fr) minmax(0,2fr) minmax(0,.6fr)",
        '<div class="lst">' + cbox("ID", "Уникальный идентификатор транзакции: пакет принадлежит одной сессии «запрос-ответ».", 2) + cbox("QR", "Тип сообщения: 0 — запрос, 1 — ответ.", 2) +
        cbox("Opcode", "Код операции (тип запроса).", 2) + cbox("QDCOUNT", "Количество записей в разделе запросов.", 3) + cbox("ANCOUNT", "Количество записей в разделе ответов.", 3) + '</div>',
        '<div>' + G("repeat(6,minmax(0,1fr))", cbox("AA", "Является ли сервер авторитетным для домена.", 2), cbox("TC", "Флаг усечения (сообщение усечено).", 2), cbox("RD", "Запрашивает рекурсивное разрешение.", 2),
                    cbox("RA", "Поддерживает ли сервер рекурсию.", 2), cbox("Z", "Зарезервированные биты (равны 0).", 2), cbox("Rcode", "Код ответа (результат запроса).", 2)) +
        '<div class="mt">' + HT + '</div>' + info("Структура заголовка используется как в запросах, так и в ответах. После заголовка следуют секции с данными (вопросы, ответы, дополнительные записи).", "file", 4) + '</div>',
        '<div class="lst" style="justify-content:flex-end">' + cbox("NSCOUNT", "Количество записей, связанных с именем сервера (уполномоченные серверы).", 3) + cbox("ARCOUNT", "Количество записей в Additional Record Section.", 3) + '</div>', cls="as"))

# 32 ---------------------------------------------------------------- флаги (s24) и RFC 5395 (s25)
FL_IC = {"QR": "link", "Opcode": "file", "AA": "shield", "TC": "cross", "RD": "target", "RA": "server", "Z": "cross", "Rcode": "file", "AD": "check", "CD": "info"}
def flagbar(flags, s=1):
    cells = "".join(f'<div class="fb{" new" if n in ("AD", "CD") else ""}" style="flex:{w}" tabindex="0"><b>{n}</b><small>{w} бит{"а" if w in (3, 4) else ""}</small></div>' for n, w, d in flags)
    return f'<div class="fbar" data-s="{s}">{cells}</div>'
slide("Флаги DNS", "", "", G("minmax(0,1fr) minmax(0,1.2fr)", ih("Параметры поля", "«Флаги» DNS", big=True),
      info("Поле «Флаги» (Flags) в заголовке DNS — 2 байта. Оно содержит управляющие параметры: тип сообщения, коды операций и опции запроса или ответа.", "info", 0), cls="ac") +
      flagbar(FLAGS) + G("repeat(8,minmax(0,1fr))", *[f'<div class="card pn fc" data-s="2" style="--dl:{i*80}ms"><h3>{n}</h3><p class="p sm">{d}</p>{hexicon(FL_IC[n], "hx")}</div>' for i, (n, w, d) in enumerate(FLAGS)], style="margin-top:1rem") +
      '<div class="mt">' + info("Поле «Флаги» используется как в DNS-запросах, так и в DNS-ответах. В анимации «Путь DNS-запроса» видно, как меняются RD, AA и RA.", "file", 3) + '</div>')
slide("RFC 5395", "", "", G("minmax(0,1fr) minmax(0,1.2fr)", ih("Параметры поля «Флаги»", "стандарт RFC 5395", big=False),
      info("В стандарте RFC 5395 появились дополнительные биты <b>AD</b> и <b>CD</b>, заимствованные из поля Z, и добавились значения в поле Opcode.", "info", 0), cls="ac") +
      flagbar(FLAGS2) + G("minmax(0,1fr) minmax(0,1fr) minmax(0,1fr)",
        pnl("Opcode", table(["Код", "Значение"], [["0", "стандартный запрос"], ["1", "инверсный запрос"], ["2", "запрос статуса сервера"], ["4", "уведомление: ведущий сервер сообщает ведомым, что данные изменены"], ["5", "обновление"], ["3, 6–15", "зарезервированы"]], "sm"), "", 2),
        pnl("AD — Authentic data", '<p class="p sm">Устанавливается в ответе: включённые данные были проверены сервером, который их предоставил.</p>', "amb", 2, ic="check"),
        pnl("CD — Checking disabled", '<p class="p sm">Устанавливается в запросе: непроверенные данные приемлемы для преобразователя, отправляющего запрос.</p>', "amb", 2, ic="info"), style="margin-top:1rem") +
      '<div class="mt">' + bitrow(FLAGS2, 3) + '</div>')

# 34 ---------------------------------------------------------------- Wireshark: запрос и ответ (s23, s26)
WSQ = ('<div class="ws" data-s="1">▾ Domain Name System (query)\n    Transaction ID: 0x02bc\n  ▾ <span class="hl">Flags: 0x0100 Standard query</span>\n'
       '      0... .... .... .... = Response: Message is a query\n      .000 0... .... .... = Opcode: Standard query (0)\n      .... ..0. .... .... = Truncated: Message is not truncated\n'
       '      <span class="rd">.... ...1 .... .... = Recursion desired: Do query recursively</span>\n      .... .... .0.. .... = Z: reserved (0)\n    Questions: 1\n    Answer RRs: 0\n'
       '    Authority RRs: 0\n    Additional RRs: 0\n  ▾ Queries\n    ▾ <span class="hl">arc-emea.msn.com: type A, class IN</span>\n        Name: arc-emea.msn.com\n'
       '        <span class="rd">Type: A (Host Address) (1)</span>\n        <span class="rd">Class: IN (0x0001)</span></div>')
WSA = ('<div class="ws" data-s="1">▾ Queries\n    arc-emea.msn.com: type A, class IN\n▾ Answers\n  ▸ arc-emea.msn.com: type <span class="hl">CNAME</span>, class IN, cname arc-…\n'
       '  ▸ arc-emea.trafficmanager.net: type CNAME, class IN, …\n  ▾ iris-de-prod-azsc-v2-frc.francecentral.cloudapp.az…\n        Type: A (Host Address) (1)\n        Class: IN (0x0001)\n'
       '        <span class="rd">Time to live: 10 (10 seconds)</span>\n        Data length: 4\n        <span class="rd">Address: 20.199.58.43</span></div>')
slide("DNS-запрос в Wireshark", "", "", G("minmax(0,1fr) minmax(0,1.2fr)",
    '<div>' + ih("DNS-запрос", "в Wireshark", "рисунок 7.3.1.3") +
    pnl("Что видно в захвате", bul(["Компьютер поручает DNS-серверу найти адрес IPv4: <b>Type = A</b>.", "Имя ресурса: <b>arc-emea.msn.com</b> (поле Name).", "Класс адресов Internet: <b>Class = IN</b>.",
                                    "В поле Flags единицей отмечено <b>Recursion Desired</b>: нужно сразу предоставить конечный IP-адрес без промежуточных адресов доменов."]), "", 2) + '</div>',
    WSQ, cls="ac"))
slide("DNS-ответ и типы записей", "", "", G("minmax(0,1fr) minmax(0,1.2fr)",
    '<div>' + ih("DNS-ответ", "и типы записей", "рисунок 7.3.1.6") +
    pnl("Что видно в захвате", bul(["По запросу для arc-emea.msn.com найдено три записи.", "Одна из них — адрес IPv4 <b>20.199.58.43</b>, действительна ещё <b>10 секунд</b>.", "Тип <b>CNAME</b> — каноническое имя: псевдоним привязан к действительному доменному имени."]), "", 2) +
    pnl("Типы записей", '<div class="lst">' + lrow("pc", "A", "IPv4-адрес конечного устройства", 3) + lrow("pc", "AAAA", "IPv6-адрес конечного устройства", 3) + lrow("server", "NS", "доверенный сервер имён", 3) +
        lrow("mail", "MX", "запись обмена почтовыми сообщениями", 3) + lrow("link", "CNAME", "каноническое имя (псевдоним)", 3) + '</div>', "", 3) + '</div>',
    WSA + '<div class="mt">' + info("Локальный DNS-сервер ищет имя в своих записях. Нет совпадения — обращается к другим DNS-серверам; найденный IP-адрес передаётся локальному серверу и пользователю.", "dns", 4) + '</div>', cls="ac"))

# 36 ---------------------------------------------------------------- структура доменного имени — дерево (s27_3)
def _tree():
    N = {"r": (330, 50, "."), "com": (200, 150, ".com"), "ru": (460, 150, ".ru"), "ex": (200, 250, "example"), "ya": (460, 250, "yandex"),
         "www": (90, 350, "www"), "mail": (230, 350, "mail"), "sup": (370, 350, "support")}
    E = [("r", "com"), ("r", "ru"), ("com", "ex"), ("ru", "ya"), ("ex", "www"), ("ex", "mail"), ("ex", "sup")]
    b, els = [], {}
    for i, (a, c) in enumerate(E):
        x1, y1, _ = N[a]; x2, y2, _ = N[c]
        eid = f"te{i}"
        b.append(f'<g class="arw" data-id="{eid}"><path class="dr wt" pathLength="1" d="M{x1} {y1 + 20}V{(y1 + y2) / 2}H{x2}V{y2 - 20}"/></g>')
        els[eid] = {"c": {0: "", {0: 1, 1: 1, 2: 2, 3: 2, 4: 3, 5: 3, 6: 3}[i]: "on"}}
    for k, (x, y, t) in N.items():
        w = 44 + len(t) * 11
        lvl = {"r": 0, "com": 1, "ru": 1, "ex": 2, "ya": 2}.get(k, 3)
        b.append(f'<g class="an" data-id="tn_{k}"><path class="tnode" d="M{x - w / 2 + 10} {y - 20}H{x + w / 2 - 10}L{x + w / 2} {y}L{x + w / 2 - 10} {y + 20}H{x - w / 2 + 10}L{x - w / 2} {y}Z"/>'
                 f'<text x="{x}" y="{y + 6}" text-anchor="middle">{t}</text></g>')
        els[f"tn_{k}"] = {"o": {0: 0, lvl: 1}} if lvl else {"o": {0: 1}}
    sc = scene("tree", 3, els, {i: 1000 for i in range(4)})
    return f'<div {sc}><svg class="mini tree" viewBox="20 20 520 360" aria-hidden="true">{"".join(b)}</svg></div>'
slide("Структура доменного имени", "", "", G("minmax(0,.7fr) minmax(0,1.1fr) minmax(0,1fr)",
    '<div>' + ih("Структура", "доменного имени", "", "Доменное имя имеет иерархическую структуру, состоящую из нескольких частей, разделённых точками.") +
    '<div class="lst">' + lrow("globe", "Корневой домен", "Обозначается точкой (.) и не содержит символов.") + lrow("globe", "Домен верхнего уровня (TLD)", "Доменная зона: тип организации или география.") +
    lrow("server", "Домен второго уровня (SLD)", "Уникальное имя ресурса в зоне: в одной зоне не может быть двух одинаковых SLD.") + lrow("link", "Поддомен (домен третьего уровня)", "Необязательный уровень для организации структуры сайта.") + '</div></div>',
    '<div>' + info("<b>FQDN (Fully Qualified Domain Name)</b> — формат доменного имени:<br><span class='mono hl'>hostname.second-level domain.top-level domain.root domain.</span>", "info", 0) + _tree() +
    '<div class="ibox" data-s="0">' + hexicon("globe", "hx") + '<div>Пример полного доменного имени (FQDN): <span class="chip" style="font-size:1.2rem">www.mail.example.ru.</span></div></div></div>',
    '<div class="lst">' + pnl("TLD географического типа", '<div class="pns">принадлежность к территории, обычно две буквы</div><table class="tbl2"><tr><th>TLD</th><th>Страна</th></tr>' +
                              "".join(f"<tr><td>{a}</td><td>{b_}</td></tr>" for a, b_ in (("ru", "Россия"), ("рф", "Россия"), ("kz", "Казахстан"), ("su", "Страны СНГ"), ("uk", "Великобритания"), ("de", "Германия"))) + '</table>', "", 1, ic="globe") +
    pnl("TLD административного типа", '<div class="pns">тип организации, обычно три буквы</div><table class="tbl2"><tr><th>TLD</th><th>Тип организации</th></tr>' +
        "".join(f"<tr><td>{a}</td><td>{b_}</td></tr>" for a, b_ in (("com", "Коммерческая"), ("edu", "Образовательная"), ("net", "Коммуникационная"), ("org", "Некоммерческая"), ("int", "Международная"))) + '</table>', "", 2, ic="book") +
    info("У одного домена второго уровня может быть несколько поддоменов: <b>mail</b> и <b>support</b> в www.mail.example.ru и www.support.example.ru — поддомены домена example.ru.", "folder", 3) + '</div>', cls="as"))

# 37 ---------------------------------------------------------------- WWW.SHOP.EXAMPLE.RU (s28)
DP = [("WWW", "c-teal"), ("SHOP", "c-blue"), ("EXAMPLE", "c-grn"), ("RU", "c-amb")]
bigdom = '<div class="bigdom">' + "".join(f'<span class="bd {c}" data-s="{5 - i if i else 4}" data-w="900">{t}</span>{"<i>.</i>" if i < 3 else ""}' for i, (t, c) in enumerate(DP)) + '</div>'
def dcard(n, t, d, ic, s, col):
    return f'<div class="card pn" data-s="{s}"><div class="pnh"><span class="nb nb-{col}">{n}</span><h3>{t}</h3></div><div class="G ac" style="--gc:auto 1fr">{hexicon(ic, "hx lg")}<p class="p sm" style="margin:0">{d}</p></div></div>'
slide("Части доменного имени", "", "", G("minmax(0,.6fr) minmax(0,2fr)",
    '<div>' + ih("Структура", "доменного имени", "", "Доменное имя состоит из нескольких частей, разделённых точками. Каждая часть выполняет свою функцию и указывает на уровень в иерархии доменных имён.") +
    qt("Правильно выбранная структура доменного имени помогает сделать сайт узнаваемым, удобным и простым для пользователей.", 5) + '</div>',
    '<div>' + G("minmax(0,1fr) minmax(0,1fr)", dcard(1, "Поддомен для обозначения веб-сайта", "Три символа «WWW» часто используются как обозначение веб-сайта — аббревиатура от «World Wide Web» (Всемирная паутина).", "desk", 4, "teal"),
                dcard(4, "Домен верхнего уровня", "Общая категория или географическая принадлежность ресурса. Например, .RU — национальный домен России.", "globe", 1, "amb")) +
    bigdom + G("minmax(0,1fr) minmax(0,1fr)", dcard(2, "Поддомен", "Дополнительный уровень для организации структуры сайта или создания различных разделов, например WWW.SERVICE.EXAMPLE.RU.", "layers", 3, "blue"),
               dcard(3, "Домен второго уровня", "Основа уникального доменного имени, которая обычно указывает название сайта.", "server", 2, "grn")) + '</div>', cls="ac"))
