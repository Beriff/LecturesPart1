
# ================================================================ SLIDES — повторяют инфографики 7.pptx
from _g7a_ui import (dev, devsvg, devbox, ih, info, qt, pnl, pcd, tile, lrow, steps, bul, irow, G, code, kv, chip, ftile, globe_deco, CSS2)

def art(ic, tag="", cls=""):
    t = f'<span class="tag">{tag}</span>' if tag else ""
    return f'<div class="art {cls}"><svg class="bigic" viewBox="0 0 24 24" aria-hidden="true"><path d="{IC[ic]}"/></svg>{t}</div>'

def mline(d, col, cls=""):
    return f'<div class="mline {d} c-{col} {cls}"></div>'

def srow(i, title, text, label, d, col, s, w=1300):
    return (f'<div class="srow" data-s="{s}" data-w="{w}"><span class="hn">{i}</span><div class="st"><b>{title}</b><span>{text}</span></div>'
            f'<div class="ar c-{col}">{label}{mline(d, col)}</div></div>')

def adr(pairs):
    return "<div>" + "".join(f"<span>{k}</span><b>{v}</b>" for k, v in pairs) + "</div>"

def msgrow(name, ic, d, col, note, left, right, s, w=1500):
    return (f'<div class="msg" data-s="{s}" data-w="{w}"><div class="mh">{hexicon(ic, "hx sm")}{name}<small>{note}</small></div>{mline(d, col)}'
            f'<div class="addr">{adr(left)}{adr(right)}</div></div>')

S.clear()

# 1 ---------------------------------------------------------------- титул
TITLE_ART = ('<div class="tart" aria-hidden="true">' + globe_deco("tglobe") +
             "".join(f'<div class="tic t{i}">{hexicon(ic, "hx lg")}</div>' for i, ic in enumerate(["mail", "folder", "globe", "dns", "lock", "clock"])) +
             f'<div class="tlap">{devsvg("laptop", "globe", "16rem")}</div></div>')
slide("Титул", "", "", f"""
<div class="title">{TITLE_ART}
  <div class="kick"><span class="nb">07</span>Глава 7</div>
  <h1>Уровень<br><span class="o2">приложений</span></h1>
  <p class="ihs">HTTP · DNS · DHCP · FTP · почта · NTP</p>
  <p class="lead">Как работают сервисы, которыми мы пользуемся каждый день: от ввода адреса в браузере до получения письма и синхронизации часов</p>
  <p class="authors">Ананко Софья Михайловна<br>Качур Анна Юрьевна</p>
</div>""", "tslide")

# 2 ---------------------------------------------------------------- цель
slide("Цель лекции", "", "", ih("Цель", "лекции", "что разберём в главе 7", inline=True, big=True) +
      G("repeat(3,minmax(0,1fr))", *[pnl("", f'<div class="goal">{hexicon(ic, "hx lg")}<span class="nb">{i+1:02d}</span></div><h3 class="uh">{t}</h3><p class="p sm">{d}</p>', "", 1)
                                     for i, (ic, t, d) in enumerate([("layers", "Функции", "Функции уровня приложений"),
                                                                     ("globe", "Протоколы", "Протоколы уровня приложений"),
                                                                     ("link", "Взаимодействие", "Взаимодействие с нижестоящими протоколами модели OSI")])]) +
      '<div class="mt">' + qt("Уровень приложений — самый верхний уровень модели OSI: здесь работают сервисы, с которыми сталкивается пользователь.") + '</div>')

# 3 ---------------------------------------------------------------- OSI и TCP/IP + популярные протоколы (s03)
POP7 = [("globe", "HTTP", "Hyper Text Transfer Protocol", "Протокол передачи гипертекста"), ("dns", "DNS", "Domain Name Service", "Служба доменных имен"),
        ("gear", "DHCP", "Dynamic Host Configuration Protocol", "Протокол динамической конфигурации узла"), ("folder", "FTP", "File Transfer Protocol", "Протокол передачи файлов"),
        ("mail", "SMTP", "Simple Mail Transfer Protocol", "Простой протокол электронной почты"), ("mail", "POP", "Post Office Protocol", "Протокол получения электронной почты"),
        ("mail", "IMAP", "Internet Message Access Protocol", "Протокол доступа к сообщениям Интернет")]
poprows = "".join(f'<div class="prow" data-s="{6}" style="--dl:{i*80}ms">{hexicon(ic, "hx")}<div><b>{n}</b><span>{f}</span></div><em>{d}</em></div>' for i, (ic, n, f, d) in enumerate(POP7))
poprows += f'<div class="prow" data-s="6" style="--dl:600ms">{hexicon("more" if False else "layers", "hx")}<div><b>И многие другие…</b></div><em></em></div>'
slide("OSI и TCP/IP", "", "", G("minmax(0,1.25fr) minmax(0,1fr)",
    '<div>' + ih("Уровень", "приложений", "модели OSI и TCP/IP",
                 "Уровень приложений, уровень представления и сеансовый уровень модели OSI соответствуют одному уровню приложений модели TCP/IP.", inline=True) +
    OSI_SC + '<div class="mt">' + qt("Протоколы уровня приложений нужны для обмена данными между приложениями конечных пользователей. <span class='hl'>Это самый верхний уровень в модели OSI.</span>", 1, "layers") + '</div></div>',
    '<div class="relbox">' + globe_deco("gdeco g-tr") + pnl("Популярные протоколы", '<div class="pns sp">уровня приложений</div><div class="lst">' + poprows + '</div>', "", 0) +
    '<p class="p sm mt">Более подробно каждый из протоколов будет рассмотрен в данной главе.</p></div>', cls="as"))

# 4 ---------------------------------------------------------------- протоколы 01–06 (s04)
REQRESP = ('<svg class="mini" viewBox="0 0 520 220" aria-hidden="true">'
           f'<g transform="translate(80 120) scale(1.05)">{dev("laptop", "page")}</g><g transform="translate(440 120) scale(1.05)">{dev("laptop", "page")}</g>'
           f'<g transform="translate(260 46) scale(1.25)">{dev("cloud")}</g><text x="260" y="44" text-anchor="middle" style="font-family:var(--hf);font-size:13px">ПРОТОКОЛЫ</text><text x="260" y="60" text-anchor="middle" style="font-family:var(--hf);font-size:13px">УРОВНЯ ПРИЛОЖЕНИЙ</text>'
           '<text x="80" y="42" text-anchor="middle" style="font-family:var(--hf)">КЛИЕНТ</text><text x="80" y="200" text-anchor="middle" class="ml2" fill="#8fb8b0">(отправитель)</text>'
           '<text x="440" y="42" text-anchor="middle" style="font-family:var(--hf)">СЕРВЕР</text><text x="440" y="200" text-anchor="middle" class="ml2" fill="#8fb8b0">(получатель)</text>'
           + arrow("rr1", 150, 118, 368, 118, "teal") + arrow("rr2", 368, 150, 150, 150, "teal") +
           '<text x="260" y="108" text-anchor="middle" style="font-family:var(--hf)">ЗАПРОС</text><text x="260" y="172" text-anchor="middle" style="font-family:var(--hf)">ОТВЕТ</text></svg>')
REQRESP_SC = scene("rr", 2, {"rr1": {"c": {0: "", 1: "on"}}, "rr2": {"c": {0: "", 2: "on"}}}, {1: 1100, 2: 1100})
ARTS = {0: art("globe", "WWW"), 1: art("lock", "https://"), 2: '<div class="art col"><span class="chip">eltex-co.ru</span><span class="arrd"></span><span class="chip">62.109.1.166</span></div>',
        3: '<div class="art">' + devsvg("router", "", "6.5rem") + '<div class="mini-list">IP-адрес<br>Маска подсети<br>Шлюз<br>DNS-сервер</div></div>',
        4: '<div class="art">' + devsvg("server", "", "3rem") + art("file") + devsvg("server", "", "3rem") + '</div>', 5: art("shield", "SFTP")}
slide("Протоколы 01–06", "", "", G("minmax(0,1fr) minmax(0,1fr)",
    ih("Протоколы", "уровня приложений", "обмен данными между приложениями",
       "Во время сеанса связи протоколами уровня приложений пользуется как отправляющая, так и принимающая сторона. Для успешного обмена информацией между двумя приложениями необходима совместимость протоколов."),
    f'<div class="card dgc flow" {REQRESP_SC}>{REQRESP}<p class="p sm" style="text-align:center;margin:0">Оба устройства используют одинаковые протоколы для обмена данными.</p></div>', cls="ac") +
    G("repeat(3,minmax(0,1fr))", *[pcd(i + 1, P16[i][0], P16[i][1], P16[i][2], ARTS[i], 1, i * 90) for i in range(6)]) +
    '<div class="mt">' + qt("Протоколы уровня приложений обеспечивают обмен данными между приложениями конечных пользователей.") + '</div>')

# 5 ---------------------------------------------------------------- протоколы 07–16 (s05)
ARTS2 = {6: art("mail"), 7: art("mail"), 8: art("mail", "3"), 9: art("mail"), 10: art("folder"), 11: art("video"), 12: art("gear"), 13: art("term"), 14: art("lock", ">_"), 15: art("desk")}
slide("Протоколы 07–16", "", "", G("minmax(0,1.1fr) minmax(0,1fr)",
    ih("Протоколы", "уровня приложений", "связь людей и данных"),
    info("Протоколы уровня приложений позволяют приложениям конечных пользователей обмениваться данными по сети. Во время сеанса связи ими пользуются как отправляющая, так и принимающая сторона.", "globe"), cls="ac") +
    G("repeat(4,minmax(0,1fr))", *[pcd(i + 1, P16[i][0], P16[i][1], P16[i][2], ARTS2[i], 1, (i - 6) * 70, "sm") for i in range(6, 16)],
      '<div style="grid-column:span 2;display:flex;flex-direction:column;gap:.7rem">' + qt("Совместимость протоколов — необходимое условие успешного обмена данными между приложениями.") +
      irow([("mail", "Почта"), ("folder", "Файлы"), ("video", "Мультимедиа"), ("gear", "Управление"), ("term", "Удалённый доступ")]) + '</div>'))

# 6 ---------------------------------------------------------------- уровень представления (s06)
def osi_stack(hi, s=1):
    return '<div class="stack3d">' + "".join(f'<div class="slab{" hi" if 7 - i == hi else " dim"}" data-s="{s}" style="--dl:{i*70}ms"><span class="sn">{7 - i}</span>{t} уровень</div>'
                                            for i, t in enumerate(["Прикладной", "Представления", "Сеансовый", "Транспортный", "Сетевой", "Канальный", "Физический"])) + '</div>'
FMT = [("JPEG", "Стандарт цифрового сжатия неподвижных изображений.", "img", "JPG"), ("PNG", "Формат файлов для растровых графических приложений.", "img", "PNG"),
       ("GIF", "Формат обмена графическими данными.", "img", "GIF"), ("MPEG", "Стандарт сжатия движущихся видеоизображений.", "video", "MPEG"),
       ("ASCII", "Таблица кодировки, в которой распространенным печатным и непечатным символам сопоставлены числовые коды.", "file", "ASCII"),
       ("TLS/SSL", "Криптографические протоколы, обеспечивающие безопасную связь.", "shield", "TLS/SSL")]
slide("Уровень представления", "", "", G("minmax(0,.9fr) minmax(0,.8fr) minmax(0,1.3fr)",
    ih("Уровень", "представления", "модель OSI", "Преобразование. Защита. Сжатие. Данные в понятном виде."),
    osi_stack(6),
    pnl("Основные функции", G("1fr 1fr", lrow("file", "Форматирование данных", "Данные с уровня приложений — в удобный для сети формат и обратно."),
                              lrow("file", "Кодирование", "Перевод из кодировки ASCII в понятный для человека текст."),
                              lrow("layers", "Сжатие данных", "Сокращение объема передаваемой информации."),
                              lrow("lock", "Шифрование и дешифрование", "Защита передаваемых по сети данных.")), "", 1), cls="ac") +
    '<h3 class="uh mt">Популярные стандарты и форматы <span class="dimp">уровня представления</span></h3>' +
    G("repeat(3,minmax(0,1fr))", *[pcd(i + 1, n, "", d, art(ic, t), 2, i * 80, "sm") for i, (n, d, ic, t) in enumerate(FMT)]) +
    G("minmax(0,1fr) minmax(0,1fr)", irow([("img", "Изображения"), ("video", "Видео"), ("file", "Текст"), ("lock", "Безопасность")], 3),
      qt("Удобные данные — надёжные соединения для цифрового мира. Уровень представления делает данные доступными, эффективными и безопасными.", 3), style="margin-top:.8rem"))

# 7 ---------------------------------------------------------------- сеансовый уровень (s07)
SESS_ART = ('<svg class="mini" viewBox="0 0 520 230" aria-hidden="true">'
            f'<g transform="translate(90 140) scale(1.3)">{dev("laptop", "page")}</g><g transform="translate(440 130) scale(1.3)">{dev("monitor", "page")}</g>'
            + arrow("se1", 170, 118, 360, 118, "teal", curve=40) + arrow("se2", 360, 160, 170, 160, "teal", curve=-40) +
            '<text x="265" y="146" text-anchor="middle" style="font-family:var(--hf);font-size:24px;fill:#7ef5e2">СЕАНС</text></svg>')
SESS_SC = scene("sesl", 2, {"se1": {"c": {0: "", 1: "on"}}, "se2": {"c": {0: "", 2: "on"}}}, {1: 900, 2: 900})
slide("Сеансовый уровень", "", "", ih("Сеансовый", "уровень", "установление и поддержание сеанса связи", inline=True, big=True) +
      G("minmax(0,.7fr) minmax(0,1.6fr)", osi_stack(5),
        '<div>' + G("minmax(0,1fr) minmax(0,1fr)",
                    '<div><h3 class="uh">Что делает?</h3><p class="p">Сеансовый уровень служит для установления, поддержания, завершения сеанса связи, а также обмена информацией между двумя приложениями конечных пользователей.</p></div>',
                    f'<div {SESS_SC}>{SESS_ART}</div>', cls="ac") +
        '<h3 class="uh">Основные протоколы</h3>' +
        G("repeat(4,minmax(0,1fr))", tile("hand", "H.245", "Протокол согласования параметров соединения", "", 2), tile("shield", "L2TP", "Туннельный протокол для поддержания виртуальных частных сетей", "", 2, 90),
          tile("user", "PAP", "Протокол простой проверки подлинности", "", 2, 180), tile("link", "PPTP", "Туннельный протокол типа «точка-точка»", "", 2, 270)) +
        '<div class="mt">' + qt("Сеансовый уровень обеспечивает диалог между приложениями — от начала сеанса до его завершения.", 3) + '</div></div>', cls="ac"))

# 8 ---------------------------------------------------------------- этапы сеанса (s16)
STG = [("1", "Инициация сеанса", "blue", "Запрос на соединение (SYN)", "r", "Один из участников отправляет запрос на установление соединения другому участнику."),
       ("2", "Согласование", "grn", "Обмен параметрами", "b", "Между участниками происходит обмен данными для согласования условий сеанса."),
       ("3", "Установление соединения", "vio", "Соединение установлено", "c", "После согласования условий соединение считается установленным. Обе стороны готовы к передаче данных."),
       ("4", "Передача данных", "amb", "Данные / подтверждения (ACK)", "b", "В течение сеанса происходит обмен информацией. Каждая часть данных подтверждается на приёмной стороне."),
       ("5", "Завершение сеанса", "red", "Запрос на завершение (FIN / ACK)", "b", "Один из участников инициирует завершение сеанса, и после получения подтверждения соединение разрывается.")]
def stgcard(n, t, col, lab, mode, d, i):
    ar = mline("r", col) if mode == "r" else (mline("r", col) + mline("l", col) if mode == "b" else f'<div class="okc c-{col}">{hexicon("check", "hx sm")}</div>')
    return (f'<div class="card pn stg" data-s="{i+1}" data-w="1300"><div class="pnh"><span class="nb nb-{col}">{n}</span><h3>{t}</h3></div>'
            f'<div class="stgd">{devsvg("laptop", "", "3.6rem")}<div class="stga c-{col}"><small>{lab}</small>{ar}</div>{devsvg("server", "", "2.8rem")}</div>'
            f'<div class="stgl"><span>Клиент</span><span>Сервер</span></div><p class="p sm">{d}</p></div>')
slide("Сеанс связи", "", "", G("minmax(0,1.5fr) minmax(0,1fr)",
    ih("Этапы установки", "сеанса связи", "", "<b class='hl'>Сеанс связи</b> — установленное взаимодействие между устройствами, позволяющее передавать и принимать информацию. Информация пересылается по частям, приём каждой части и всего сообщения подтверждается."),
    qt("Сеанс связи обеспечивает надёжную доставку данных — полностью и в правильном порядке.", 0), cls="ac") +
    G("repeat(5,minmax(0,1fr))", *[stgcard(*x, i) for i, x in enumerate(STG)]) +
    G("minmax(0,1fr) minmax(0,1.1fr) minmax(0,.9fr)",
      pnl("Гарантии сеанса связи", G("repeat(3,minmax(0,1fr))", tile("shield", "Полная доставка", "Все части сообщения будут доставлены", "plain", 6),
                                     tile("book", "Правильный порядок", "Данные поступают в нужной последовательности", "plain", 6), tile("check", "Подтверждение", "Каждая часть подтверждается приёмной стороной", "plain", 6)), "", 6),
      pnl("Пример: этапы на диаграмме обмена", SESS, "", 6),
      '<div style="display:flex;flex-direction:column;gap:.8rem">' + pnl("Где используется?", G("1fr 1fr", tile("globe", "Веб-сайты", "HTTP/HTTPS", "plain", 6), tile("mail", "Почта", "SMTP", "plain", 6),
                                                                                                    tile("folder", "Файлы", "FTP", "plain", 6), tile("video", "Видео", "потоковое", "plain", 6)), "", 6) +
      qt("Установка сеанса связи — основа надёжного обмена данными в сетях.", 6) + '</div>', style="margin-top:.8rem"))

# 9 ---------------------------------------------------------------- FTP два соединения (s08)
slide("FTP: два соединения", "", "", G("minmax(0,.7fr) minmax(0,1.8fr)",
    '<div>' + ih("FTP", "протокол передачи файлов", big=True) + info("<b>FTP (File Transfer Protocol)</b> — протокол для передачи файлов между клиентом и сервером по модели клиент/сервер.") + '</div>',
    FTP2, cls="ac") +
    G("repeat(3,minmax(0,1fr))",
      pnl("FTP-клиент", bul(["Запущенное на узле приложение для получения данных с сервера и отправки данных на сервер.", "Устанавливает TCP-соединения с FTP-сервером."]), "", 1, ic="user"),
      pnl("Особенности", bul(["Для работы FTP необходимо два соединения: для команд и ответов — TCP-соединение, для передачи файлов — TCP-соединение.",
                              "Соединение для данных создаётся для каждого сеанса передачи и автоматически закрывается после её завершения."]), "", 1, ic="gear"),
      pnl("FTP-сервер", bul(["На сервере должна быть запущена FTP-служба в виде приложения.", "Обрабатывает команды клиента и обеспечивает передачу файлов."]), "", 1, ic="server")))

# 10 ---------------------------------------------------------------- ASCII / бинарный (s09)
FILES_UP = "".join(f'<div class="fly up" data-s="2" style="--dl:{i*250}ms">{ftile(t)}</div>' for i, t in enumerate(["TXT", "LOG", "CFG"]))
FILES_DN = "".join(f'<div class="fly dn" data-s="3" style="--dl:{i*250}ms">{ftile(t, "blue")}</div>' for i, t in enumerate(["EXE", "BIN", "PNG"]))
slide("FTP: ASCII и бинарный", "", "", G("minmax(0,.8fr) minmax(0,1fr) minmax(0,1fr)",
    ih("FTP", "передача файлов по модели клиент/сервер", big=True),
    pnl("Режим <span class='hl'>ASCII</span>", '<div class="frow">' + ftile("TXT") + ftile("LOG") + ftile("CFG") + '</div><p class="p sm" style="text-align:center;margin:.4rem 0 0">Текстовые файлы</p>', "", 1),
    pnl("<span class='hl'>Бинарный</span> режим", '<div class="frow">' + ftile("EXE", "blue") + ftile("BIN", "blue") + ftile("PNG", "blue") + '</div><p class="p sm" style="text-align:center;margin:.4rem 0 0">Нетекстовые файлы</p>', "", 1), cls="ac") +
    G("minmax(0,.7fr) minmax(0,2fr) minmax(0,.7fr)", devbox("laptop", "FTP-клиент", "", "folder", "12rem"),
      f'<div class="lane"><small>Загрузка файлов на сервер</small><div class="lanebar c-teal">{FILES_UP}{mline("r", "teal")}</div>'
      f'<div class="lanebar c-blue">{FILES_DN}{mline("l", "blue")}</div><small>Выгрузка файлов с сервера</small></div>',
      devbox("server", "FTP-сервер", "", "", "8rem"), cls="ac", style="margin:.8rem 0") +
    G("minmax(0,1fr) minmax(0,1fr)",
      pnl("", '<div class="pnh">' + hexicon("file", "hx") + '<p class="p sm" style="margin:0"><b class="hl">ASCII</b> — отправитель преобразовывает символы в код ASCII перед отправкой, получатель — обратно в символы. Подходит для TXT, LOG, CFG: файлов конфигурации и лог-файлов сетевых устройств.</p></div>', "", 4),
      pnl("", '<div class="pnh">' + hexicon("zip", "hx") + '<p class="p sm" style="margin:0"><b class="hl">Бинарный режим</b> — передаёт файлы без преобразования формата. Подходит для BIN, EXE, PNG: изображений, программ и файлов версий сетевых устройств.</p></div>', "", 4)))

# 11/12 ---------------------------------------------------------------- FTP активный / пассивный (s10, s11)
def ftp_mode(mode):
    act = mode == "a"
    rows = ([("Клиент инициирует соединение", "FTP-клиент устанавливает TCP-соединение с TCP-портом 21 на FTP-сервере.", "TCP SYN, порт 21", "r", "teal"),
             ("Аутентификация", "Обмен данными для входа пользователя.", "USER / PASS", "b", "teal"),
             ("Команда PORT", "Клиент сообщает открытый порт P (случайный порт; P > 1024).", "PORT P (P > 1024)", "r", "teal"),
             ("Установка соединения для данных", "FTP-сервер (порт 20) инициирует TCP-соединение на порт P FTP-клиента.", "TCP SYN с порта 20 на порт P", "l", "blue"),
             ("Передача файлов", "После установления соединения начинается передача данных.", "Передача данных", "b", "blue")] if act else
            [("Установка управляющего соединения", "Клиент устанавливает TCP-соединение с портом 21 на FTP-сервере.", "TCP SYN, порт 21", "r", "teal"),
             ("Аутентификация", "Обмен данными для входа пользователя (USER / PASS).", "USER / PASS", "b", "teal"),
             ("Команда PASV", "Клиент отправляет команду PASV для запроса открытого порта на сервере.", "PASV", "r", "teal"),
             ("Ответ Enter PASV", "Сервер открывает случайный порт N (> 1024) и сообщает его клиенту.", "Enter PASV (порт N)", "l", "teal"),
             ("Установка соединения для данных", "Клиент инициирует TCP-соединение с порта P на порт N сервера.", "TCP SYN с порта P на порт N", "r", "blue"),
             ("Передача файлов", "После установки соединения начинается передача данных.", "Передача данных", "b", "blue")])
    def ar(d, col):
        return mline("r", col) + mline("l", col) if d == "b" else mline(d, col)
    rws = "".join(f'<div class="srow" data-s="{i+1}" data-w="1500"><span class="hn">{i+1}</span><div class="st"><b>{t}</b><span>{x}</span></div>'
                  f'<div class="ar c-{c}">{l}{ar(d, c)}</div></div>' for i, (t, x, l, d, c) in enumerate(rows))
    n = len(rows)
    srvports = ('<div class="plist"><span class="chip">Порт 21<br><small>управление</small></span><span class="chip blue">' +
                ("Порт 20<br><small>данные</small>" if act else "Порт N (&gt; 1024)<br><small>данные</small>") + '</span></div>')
    head = ih("FTP", "активный режим" if act else "пассивный режим", "", "Установка соединения и передача файлов", big=True)
    inf = info("В активном режиме FTP-клиент использует случайные порты и указывает серверу порт, на который нужно подключиться для передачи данных." if act else
               "В пассивном режиме FTP-сервер открывает порт для передачи данных, а клиент устанавливает с ним соединение.", "info", 0)
    ports = pnl("Ключевые порты", '<div class="ports">' + (
        '<div><span class="pb">21</span>Управляющее соединение (от клиента к серверу)</div><div><span class="pb blue">20</span>Соединение для передачи данных (от сервера к клиенту)</div>' if act else
        '<div><span class="pb">21</span>Управляющее соединение (от клиента к серверу)</div><div><span class="pb blue">N</span>Порт для передачи данных (открывает сервер, &gt; 1024)</div>') +
        '<div><span class="pb blue">P</span>Случайный порт клиента (&gt; 1024)</div></div>', "", n + 1, ic="gear")
    mid = (pnl("Порядок работы", steps(["Клиент подключается к порту 21 сервера.", "Выполняется аутентификация.", "Клиент сообщает серверу порт P с помощью команды PORT.",
                                       "Сервер подключается с порта 20 на порт P клиента.", "Передаются данные."], n + 1), "", n + 1, ic="check") if act else
           pnl("Преимущества", bul(["Работает, если клиент находится за NAT (клиент инициирует соединение).", "Не требует открытия входящих соединений на клиенте.",
                                    "Упрощает прохождение через межсетевые экраны на стороне клиента."]), "", n + 1, ic="check"))
    lim = (pnl("Особенности", bul(["Для передачи данных сервер инициирует соединение.", "Клиент должен быть доступен извне (открыт порт P).",
                                   "Используются разные порты для управления и передачи данных.", "Подходит для простых сетей, может быть ограничен межсетевыми экранами."]), "", n + 1, ic="file") if act else
           pnl("Возможные ограничения", bul(["Если FTP-сервер во внутренней сети за межсетевым экраном и недоступен для входящих соединений от клиента, соединение не устанавливается.",
                                             "Требуется, чтобы клиент мог устанавливать соединения к открытым портам сервера."]), "amb", n + 1, ic="warn"))
    return (G("minmax(0,1fr) minmax(0,1.3fr)", head, inf, cls="ac") +
            G("minmax(0,.55fr) minmax(0,2fr) minmax(0,.55fr)",
              '<div class="col-dev">' + devsvg("laptop", "folder", "11rem") + '<span class="chip">Порт P (&gt; 1024)</span><span class="dvbl">FTP-клиент</span></div>',
              f'<div class="lst">{rws}</div>',
              '<div class="col-dev">' + devsvg("server", "", "7rem") + srvports + '<span class="dvbl">FTP-сервер</span></div>', cls="ac") +
            G("repeat(3,minmax(0,1fr))", ports, mid, lim, style="margin-top:.8rem"))
slide("FTP: активный режим", "", "", ftp_mode("a"))
slide("FTP: активный — диаграмма", "", "", G("minmax(0,.6fr) minmax(0,1.8fr)",
    '<div>' + ih("Активный режим", "по портам", "кто кому открывает соединение",
       "Каждая вертикальная линия — отдельный порт. Смотрите на направление пятой стрелки: соединение для данных открывает <b class='hl'>сервер</b> с порта 20.") +
    pnl("Лекция", p("В активном режиме клиент FTP использует случайный порт (больше 1024) для запроса на соединение на порт 21 FTP-сервера. FTP-клиент прослушивает порт Р и командой PORT уведомляет сервер. Когда необходимо передать данные, FTP-сервер отправляет запрос на соединение с порта 20 на порт P FTP-клиента.", cls="p sm"), "", 0) + '</div>',
    FTPA, cls="ac"))
slide("FTP: пассивный режим", "", "", ftp_mode("p"))
slide("FTP: пассивный — диаграмма", "", "", G("minmax(0,.6fr) minmax(0,1.8fr)",
    '<div>' + ih("Пассивный режим", "по портам", "кто кому открывает соединение",
       "Сравните с активным режимом: теперь соединение для данных открывает <b class='hl'>клиент</b> — с порта P на порт N сервера.") +
    pnl("Лекция", p("После получения команды PASV FTP-сервер включает порт N (случайный порт больше 1024) и с помощью команды Enter PASV уведомляет FTP-клиент об открытом номере порта. Когда необходимо передать данные, FTP-клиент отправляет запрос на соединение с порта Р на порт N на FTP-сервере.", cls="p sm"), "", 0) + '</div>',
    FTPP, cls="ac"))

slide("FTP: NAT и межсетевой экран", "", "", ih("Проблемы", "активного и пассивного режимов", "", "Активный режим и пассивный режим различаются способами передачи данных и имеют свои преимущества и недостатки.") +
      G("minmax(0,1fr) minmax(0,1fr)", pnl("Активный режим ломается на NAT", NATF, "red", 0, ic="router"), pnl("Пассивный режим и межсетевой экран", FWF, "amb", 0, ic="fw")))

# 16 ---------------------------------------------------------------- TFTP (s12)
TFTPW = seq("tftpw", [("TFTP-клиент", "", "pc"), ("TFTP-сервер", "", "server")], [
    {"a": 0, "b": 1, "t": "WRQ (запрос на запись)", "col": "blue"}, {"a": 1, "b": 0, "t": "ACK", "col": "violet"}, {"a": 0, "b": 1, "t": "DATA 1", "col": "amber"},
    {"a": 1, "b": 0, "t": "ACK", "col": "violet"}, {"a": 0, "b": 1, "t": "DATA n", "col": "amber"}, {"a": 1, "b": 0, "t": "ACK", "col": "violet"}], width=420, gap=38, wdef=700, top=118)
TFTPR = seq("tftpr", [("TFTP-клиент", "", "pc"), ("TFTP-сервер", "", "server")], [
    {"a": 0, "b": 1, "t": "RRQ (запрос на чтение)", "col": "green"}, {"a": 1, "b": 0, "t": "DATA 1", "col": "amber"}, {"a": 0, "b": 1, "t": "ACK", "col": "violet"},
    {"a": 1, "b": 0, "t": "DATA n", "col": "amber"}, {"a": 0, "b": 1, "t": "ACK", "col": "violet"}], width=420, gap=38, wdef=700, top=118)
PK5 = [("RRQ", "Запрос на чтение (чтение файла с сервера)", "file", "grn"), ("WRQ", "Запрос на запись (выгрузка файла на сервер)", "file", "blue"),
       ("DATA", "Пакет передачи данных", "file", "amb"), ("ACK", "Подтверждение получения пакета", "check", "vio"), ("ERROR", "Пакет контроля ошибок", "cross", "red")]
slide("TFTP", "", "", G("minmax(0,.8fr) minmax(0,1.3fr) minmax(0,.9fr)",
    ih("TFTP", "простая передача файлов", "", "Лёгкий. Быстрый. Надёжный.<br>По сравнению с FTP предназначен для передачи небольших файлов, и его проще реализовать.", big=True),
    '<div class="G ac" style="--gc:auto 1fr auto">' + devbox("laptop", "TFTP-клиент", "", "folder", "9rem") +
    f'<div class="ar c-teal" style="text-align:center;font-family:var(--hf)" data-s="1">Запросы (RRQ/WRQ) и передача данных{mline("r", "teal")}{mline("l", "teal")}<span class="chip">Порт 69 / UDP</span></div>' +
    devbox("server", "TFTP-сервер", "", "", "6rem") + '</div>',
    pnl("Стек протоколов TFTP", G("1fr 1fr", '<div class="pstack"><div>TFTP</div><div>UDP</div><div>IP</div></div>',
                                 '<div class="lst">' + lrow("server", "Использует UDP", "порт 69") + lrow("shield", "Аутентификация", "не требуется") + '</div>', cls="ac"), "", 1), cls="ac") +
    G("minmax(0,1.3fr) minmax(0,1fr) minmax(0,1fr)",
      pnl("Пакеты TFTP", '<div class="pns">TFTP использует пять типов пакетов</div>' + G("repeat(5,minmax(0,1fr))", *[tile(ic, n, d, c, 2, i * 90) for i, (n, d, ic, c) in enumerate(PK5)]), "", 2),
      pnl("Выгрузка файла", '<div class="pns">Передача файла с клиента на сервер (WRQ)</div>' + TFTPW, "", 3),
      pnl("Загрузка файла", '<div class="pns">Получение файла с сервера (RRQ)</div>' + TFTPR, "", 3), style="margin:.8rem 0") +
    G("minmax(0,1.3fr) minmax(0,1fr)",
      pnl("Основные особенности", G("repeat(4,minmax(0,1fr))", tile("hand", "Простая реализация", "Минимальный набор функций", "plain", 4), tile("zip", "Небольшие файлы", "Конфигурации и служебные файлы", "plain", 4),
                                    tile("lock", "Без аутентификации", "Не требует учётных данных", "plain", 4), tile("folder", "Нет просмотра каталога", "Нельзя просматривать список файлов на сервере", "plain", 4)), "", 4),
      pnl("Применение", G("repeat(3,minmax(0,1fr))", tile("gear", "Конфигурации", "файлы сетевых устройств", "plain", 4), tile("file", "Образы ПО", "например, прошивки", "plain", 4),
                                                       tile("server", "Развёртывание", "простое и быстрое", "plain", 4)) + qt("TFTP — простое решение для задач, где важны скорость и минимальные требования.", 4), "", 4)))
slide("TFTP: все сценарии", "", "", G("minmax(0,.8fr) minmax(0,1.5fr)",
    '<div>' + ih("TFTP", "запись, чтение, ошибка", "пошаговый обмен пакетами", "Цвет стрелки — тип пакета: <span style='color:var(--blue)'>RRQ/WRQ</span>, <span style='color:var(--amber)'>DATA</span>, <span style='color:var(--violet)'>ACK</span>, <span style='color:var(--red)'>ERROR</span>. Каждый блок данных подтверждается отдельно.") +
    G("1fr", *[lrow(ic, n, d, 0) for n, d, ic, c in PK5]) + '</div>', TFTP, cls="ac"))

# 18 ---------------------------------------------------------------- Telnet (s13)
slide("Telnet", "", "", G("minmax(0,.8fr) minmax(0,1fr) minmax(0,1fr)",
    ih("Telnet", "удалённое управление сетевым оборудованием", "", "Простое решение для доступа и настройки устройств.", big=True),
    pnl("Протокол <span class='hl'>Telnet</span>", '<div class="pnh">' + hexicon("term", "hx lg") + '<p class="p sm" style="margin:0">Telnet использует TCP (порт 23) для передачи команд и данных между клиентом и сервером. Позволяет удалённо управлять сетевыми устройствами с помощью командной строки.</p></div>', "", 1),
    pnl("Сценарии применения", G("repeat(3,minmax(0,1fr))", tile("gear", "Настройка", "и управление устройствами", "", 1), tile("target", "Диагностика", "и устранение неисправностей", "", 1), tile("file", "Удалённый доступ", "к сети", "", 1)), "", 1), cls="ac") +
    TEL +
    G("repeat(3,minmax(0,1fr))",
      pnl("Основные особенности", bul(["Использует TCP (порт 23).", "Позволяет управлять устройствами с помощью команд.", "Не требует выделенного кабеля (в отличие от консольного порта), если IP-адрес сервера Telnet доступен.",
                                       "Устройство, которым управляют, — сервер Telnet, подключающееся — клиент Telnet.", "Многие сетевые устройства могут работать и как сервер, и как клиент Telnet."]), "", 2, ic="check"),
      pnl("Преимущества", bul(["Простая реализация", "Удобное удалённое управление", "Быстрый доступ к устройствам", "Подходит для начальной настройки и диагностики"]), "", 2, ic="hand"),
      pnl("Ограничения", bul(["Передаёт данные в открытом виде (без шифрования)", "Ниже уровень безопасности по сравнению с SSH", "Не рекомендуется использовать в незащищённых сетях"]) +
          qt("Telnet — это удобно, но помните о безопасности вашей сети.", 2), "amb", 2, ic="warn"), style="margin-top:.8rem"))
