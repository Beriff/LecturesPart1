# -*- coding: utf-8 -*-
"""Нативная редактируемая PPTX деки «Локатор» — весь текст правится в PowerPoint."""
import os
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

SHOT = r'C:/Users/anank/Desktop/Локатор_скриншоты'
OUT  = r'D:/Преза лекций/Локатор.pptx'
PX = 6350  # EMU на 1 px при листе 1920x1080 -> 13.333"x7.5"
def px(v): return Emu(int(round(v*PX)))

# палитра
C = dict(
  board=RGBColor(0x0C,0x15,0x10), panelD=RGBColor(0x17,0x23,0x1C), panelL=RGBColor(0xFC,0xFA,0xF4),
  ink=RGBColor(0x2A,0x2A,0x28), muted=RGBColor(0x7C,0x77,0x68), cream=RGBColor(0xEF,0xE9,0xDB),
  mutedD=RGBColor(0x9A,0xA1,0x97), green=RGBColor(0x1F,0x6B,0x4A), red=RGBColor(0xC0,0x39,0x2B),
  gold=RGBColor(0xB9,0x8F,0x3E), goldS=RGBColor(0xED,0xD4,0x9D), mint=RGBColor(0x6B,0xD7,0x9A),
  surf=RGBColor(0xFF,0xFF,0xFF), surf2=RGBColor(0xEC,0xE7,0xDC), line=RGBColor(0xE2,0xDA,0xCA),
  dcard=RGBColor(0x1A,0x24,0x1C), glass=RGBColor(0x20,0x2B,0x23), navy=RGBColor(0x1B,0x2C,0x3F),
  goldSoftBg=RGBColor(0xED,0xD4,0x9D), redBg=RGBColor(0xFB,0xF0,0xEE), greenBg=RGBColor(0xE6,0xF2,0xEA),
)
DISP='Manrope'; TEXT='Inter'
SCALE=0.8  # коррекция px->pt (размеры задавал в px-логике)

prs = Presentation()
prs.slide_width  = px(1920); prs.slide_height = px(1080)
BLANK = prs.slide_layouts[6]

def no_shadow(sp):
    sp.shadow.inherit=False

def solid(sp, color):
    sp.fill.solid(); sp.fill.fore_color.rgb=color
def nofill(sp): sp.fill.background()
def setline(sp,color=None,w=1,dash=None):
    if color is None: sp.line.fill.background(); return
    sp.line.color.rgb=color; sp.line.width=px(w)
    if dash:
        ln=sp.line._get_or_add_ln(); d=ln.makeelement(qn('a:prstDash'),{'val':dash}); ln.append(d)

def rrect(slide,x,y,w,h,fill=None,line=None,radius=22,lw=1.5,dash=None):
    sp=slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,px(x),px(y),px(w),px(h))
    sp.adjustments[0]=min(0.5,radius/min(w,h))
    if fill is None: nofill(sp)
    else: solid(sp,fill)
    setline(sp,line,lw,dash); no_shadow(sp)
    return sp

def oval(slide,x,y,d,fill,line=None,lw=1.5):
    sp=slide.shapes.add_shape(MSO_SHAPE.OVAL,px(x),px(y),px(d),px(d))
    solid(sp,fill); setline(sp,line,lw); no_shadow(sp); return sp

def _fmt(run,size,color,bold,font,italic=False):
    run.font.size=Pt(size*SCALE); run.font.bold=bold; run.font.name=font
    run.font.color.rgb=color; run.font.italic=italic

def tb(slide,x,y,w,h,anchor=MSO_ANCHOR.TOP,align=PP_ALIGN.LEFT):
    b=slide.shapes.add_textbox(px(x),px(y),px(w),px(h)); tf=b.text_frame
    tf.word_wrap=True
    for m in ('margin_left','margin_right','margin_top','margin_bottom'): setattr(tf,m,0)
    tf.vertical_anchor=anchor
    tf.paragraphs[0].alignment=align
    return tf

def para(tf,runs,size,color,bold=False,font=TEXT,align=PP_ALIGN.LEFT,first=False,spacing=1.0,space_after=0):
    """runs: str или список (text,color|None,bold|None)."""
    p=tf.paragraphs[0] if first and not tf.paragraphs[0].runs else tf.add_paragraph()
    p.alignment=align; p.line_spacing=spacing
    p.space_before=Pt(0); p.space_after=Pt(space_after)
    if isinstance(runs,str): runs=[(runs,None,None)]
    runs=[(e,None,None) if isinstance(e,str) else e for e in runs]
    for t,c,b in runs:
        r=p.add_run(); r.text=t
        _fmt(r,size,c if c is not None else color,b if b is not None else bold,font)
    return p

def text1(slide,x,y,w,h,runs,size,color,bold=False,font=TEXT,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP,spacing=1.0):
    tf=tb(slide,x,y,w,h,anchor,align); para(tf,runs,size,color,bold,font,align,first=True,spacing=spacing); return tf

def shape_text(sp,runs,size,color,bold=False,font=TEXT,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE,wrap=False):
    tf=sp.text_frame; tf.word_wrap=wrap
    for m in ('margin_left','margin_right','margin_top','margin_bottom'): setattr(tf,m,px(6))
    tf.vertical_anchor=anchor
    para(tf,runs,size,color,bold,font,align,first=True)
    return tf

# ——— базовые блоки ———
def bg_board(slide):
    slide.background.fill.solid(); slide.background.fill.fore_color.rgb=C['board']

def panel(slide,dark):
    return rrect(slide,38,38,1844,1004,fill=C['panelD'] if dark else C['panelL'],radius=34)

def chrome(slide,dark,label):
    ink = C['cream'] if dark else C['ink']
    # бренд
    tf=tb(slide,98,66,300,44,MSO_ANCHOR.MIDDLE)
    para(tf,[('ЛОКАТОР',ink,True),('.',C['red'],True)],21,ink,True,DISP,first=True)
    # светофор
    for i,col in enumerate([C['green'],C['gold'],C['red']]):
        oval(slide,250+i*17,82,11,col)
    # активная пилюля-раздел (по центру)
    w=len(label)*10.5+52
    pill=rrect(slide,960-w/2,70,w,38,fill=(C['mint'] if dark else C['green']),radius=19)
    shape_text(pill,label,13,(C['panelD'] if dark else C['surf']),True,TEXT)
    # Контакты + меню справа
    menu=rrect(slide,1770,73,38,38,fill=(C['glass'] if dark else C['surf2']),radius=12)
    shape_text(menu,'≡',18,ink,True,TEXT)
    ct=rrect(slide,1636,74,120,36,fill=None,line=(RGBColor(0x3a,0x45,0x3d) if dark else C['line']),radius=18,lw=1)
    shape_text(ct,'Контакты',13,ink,True,TEXT)

def eyebrow(slide,y,text):
    text1(slide,98,y,1000,26,text,13.5,C['gold'],True,TEXT)

def title(slide,y,lines,size=34,dark=False,w=1724):
    ink=C['cream'] if dark else C['ink']
    lh=size*1.62  # px на строку
    for i,ln in enumerate(lines):
        tf=tb(slide,98,y+i*lh,w,lh+12); tf.word_wrap=False
        para(tf,ln,size,ink,True,DISP,first=True,spacing=0.98)
    return y+len(lines)*lh

def chip(slide,x,y,text,on=False,dark=False,red=False,h=42,fs=17):
    w=len(text)*fs*0.8+48
    if red:
        sp=rrect(slide,x,y,w,h,fill=None,line=C['red'],radius=12,lw=1.5,dash='dash'); col=C['red']
    elif on:
        sp=rrect(slide,x,y,w,h,fill=(C['mint'] if dark else C['green']),radius=12); col=(C['panelD'] if dark else C['surf'])
    else:
        sp=rrect(slide,x,y,w,h,fill=(C['glass'] if dark else C['surf2']),line=(RGBColor(0x3a,0x45,0x3d) if dark else C['line']),radius=12,lw=1); col=(C['cream'] if dark else C['ink'])
    shape_text(sp,text,fs,col,True,TEXT)
    return w

def bar(slide,x,y,W,label,frac,val,red=False,dark=False):
    lblc=C['red'] if red else (C['cream'] if dark else C['ink'])
    text1(slide,x,y-4,250,30,label,20,lblc,False,TEXT,anchor=MSO_ANCHOR.MIDDLE)
    tx=x+262; tw=W-262-70
    rrect(slide,tx,y+3,tw,16,fill=(C['glass'] if dark else C['surf2']),radius=8)
    fillw=max(10,tw*frac)
    rrect(slide,tx,y+3,fillw,16,fill=(C['red'] if red else C['green']),radius=8)
    text1(slide,x+W-64,y-6,64,30,val,22,lblc,True,DISP,align=PP_ALIGN.RIGHT,anchor=MSO_ANCHOR.MIDDLE)

def pageno(slide,n,dark):
    text1(slide,1600,1000,222,26,f'{n:02d} / 19',13.5,(C['goldS'] if dark else C['gold']),False,TEXT,align=PP_ALIGN.RIGHT)

def shot(slide,path,x,y,w):
    h=w*900/1440
    r=rrect(slide,x,y,w,h,fill=C['surf'],line=C['line'],radius=20,lw=1)
    slide.shapes.add_picture(os.path.join(SHOT,path),px(x+3),px(y+3),px(w-6),px(h-6))
    return h

def new(dark,label,n):
    s=prs.slides.add_slide(BLANK); bg_board(s); panel(s,dark); chrome(s,dark,label); pageno(s,n,dark)
    return s

def pdots(slide,x,y):
    for i,col in enumerate([RGBColor(0xF4,0xEE,0xE1),C['gold'],C['navy'],C['red']]):
        oval(slide,x+i*42,y,30,col,line=RGBColor(0xDD,0xD5,0xC4),lw=1)

# =================== СЛАЙДЫ ===================

# 01 обложка
s=new(True,'Подбор',1)
eyebrow(s,210,'ПОИСК И ОЦЕНКА КОММЕРЧЕСКИХ ЛОКАЦИЙ')
by=title(s,250,[[('Находит помещение —',C['cream'],True)],
             [('и говорит,',C['cream'],True)],
             [('стоит ли его брать',C['mint'],True)]],48,dark=True,w=1000)
pdots(s,98,by+24)
text1(s,98,by+86,940,90,[('Поиск по всем площадкам сразу и аналитика локации на ',RGBColor(0xC9,0xC4,0xB7),False),('предобученном ИИ',C['mint'],True)],20,RGBColor(0xC9,0xC4,0xB7),False,TEXT,spacing=1.25)
text1(s,98,by+196,980,40,'Циан · Авито · Яндекс · N1 · ДомКлик',18,RGBColor(0xA7,0xA2,0x94),False,TEXT)
shot(s,'03_results.png',1120,300,740)
oval(s,1090,720,60,C['red']); text1(s,1090,720,60,60,'↗',24,C['surf'],True,TEXT,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)

# 02 как ищут
s=new(False,'Проблема',2)
eyebrow(s,150,'01 / ПРОБЛЕМА')
title(s,182,[['Пять вкладок, один и тот же объект,'],['три разные цены']])
cards=[('Циан','45 000 ₽','дубль','red'),('Авито','36 200 ₽','дешевле','on'),('Яндекс','45 000 ₽','дубль','red'),('N1','?','фейк','red')]
cx=98
for name,price,tagt,kind in cards:
    w=200 if name!='N1' else 168
    dark=(kind=='on')
    card=rrect(s,cx,340,w,150,fill=(C['dcard'] if dark else C['surf']),line=(None if dark else C['line']),radius=20)
    text1(s,cx,356,w,34,name,24,(C['cream'] if dark else C['ink']),True,DISP,align=PP_ALIGN.CENTER)
    text1(s,cx,392,w,28,price,16,(C['mutedD'] if dark else C['muted']),False,TEXT,align=PP_ALIGN.CENTER)
    tw=len(tagt)*17*0.55+30
    if kind=='red': chip(s,cx+(w-tw)/2,430,tagt,red=True,h=36,fs=15)
    else: chip(s,cx+(w-tw)/2,430,tagt,on=True,h=36,fs=15)
    cx+=w+50
    if name!='N1':
        text1(s,cx-46,392,40,40,'→',26,C['gold'],True,TEXT,align=PP_ALIGN.CENTER)
text1(s,98,540,720,120,'Один и тот же объект висит в трёх местах с разной ценой. Агент вручную сверяет вкладки — и всё равно платит посреднику вместо собственника.',20,C['ink'],False,TEXT,spacing=1.25)
dc=rrect(s,900,530,922,130,fill=C['dcard'],radius=20); dc.line.color.rgb=C['gold']; dc.line.width=px(6)
tf=dc.text_frame; tf.word_wrap=True
for m in ('margin_left','margin_top','margin_bottom'): setattr(tf,m,px(20))
tf.margin_left=px(28); tf.vertical_anchor=MSO_ANCHOR.MIDDLE
para(tf,[('Если один менеджер тратит ',C['cream'],False),('большую часть рабочего дня',C['mint'],True),(' на ручной поиск и мониторинг сайтов — это время уходит не на сделки, а на рутину.',C['cream'],False)],19,C['cream'],False,TEXT,first=True,spacing=1.2)
x=98
for t in ['дубли между площадками','фейки в объявлениях','посредники вместо собственника']:
    x+=chip(s,x,770,t)+16

# 03 цена проблемы
s=new(True,'Цена проблемы',3)
eyebrow(s,150,'02 / ЦЕНА ПРОБЛЕМЫ')
title(s,182,[['Ручной обход площадок съедает'],['больше времени, чем работа с клиентом']],dark=True)
stats=[('5','площадок агент открывает и сверяет вручную по каждому запросу'),
       ('3×','один объект дублируется на разных сайтах — с разными ценами'),
       ('?','какие объявления актуальны и где собственник — вручную не видно')]
gx=98; gw=(1724-56)/3
for num,cap in stats:
    rrect(s,gx,360,gw,300,fill=C['glass'],line=RGBColor(0x2c,0x37,0x2f),radius=22,lw=1)
    text1(s,gx+28,378,gw-56,150,num,90,C['mint'],True,DISP)
    text1(s,gx+28,540,gw-56,110,cap,19,C['mutedD'],False,TEXT,spacing=1.2)
    gx+=gw+28
text1(s,98,700,1650,80,'Точные цифры по вашей воронке подставим на защите. Суть одна: время уходит не на сделку, а на рутину сверки площадок.',20,RGBColor(0xB7,0xB2,0xA5),False,TEXT,spacing=1.2)

# 04 механизм
s=new(False,'Как устроен',4)
eyebrow(s,150,'03 / КАК УСТРОЕН ЛОКАТОР')
title(s,182,[['Собираем → чистим → оцениваем']])
steps=[('🔎','Собираем','Все площадки в одном запросе: Циан, Авито, Яндекс, N1, ДомКлик.',False),
       ('🧹','Чистим','Склеиваем дубли по фото, отсеиваем фейки и посредников.',True),
       ('📊','Оцениваем','Балл объекта и индекс локации 0–100 по пяти факторам.',False)]
gx=98; gw=(1724-2*72)/3
for emo,h,body,dark in steps:
    rrect(s,gx,320,gw,300,fill=(C['dcard'] if dark else C['surf']),line=(None if dark else C['line']),radius=22)
    text1(s,gx+30,344,gw-60,50,emo,30,(C['mint'] if dark else C['green']),True,TEXT)
    text1(s,gx+30,400,gw-60,44,h,28,(C['cream'] if dark else C['ink']),True,DISP)
    text1(s,gx+30,452,gw-60,150,body,19,(C['cream'] if dark else C['ink']),False,TEXT,spacing=1.25)
    gx+=gw+72
    if h!='Оцениваем': text1(s,gx-64,440,52,44,'→',30,C['gold'],True,TEXT,align=PP_ALIGN.CENTER)
text1(s,98,670,1650,60,'Дальше по порядку: где ищем, как отбираем и почему анализу можно верить.',20,C['muted'],False,TEXT)

# 05 площадки
s=new(False,'Источники',5)
eyebrow(s,150,'04 / ИСТОЧНИКИ ОБЪЯВЛЕНИЙ')
title(s,182,[['Один запрос — пять баз']])
names=[('Циан',False),('Авито',True),('Яндекс',False),('N1',True),('ДомКлик',False)]
gw=(1724-2*22)/3; gh=140
pos=[(0,0),(1,0),(2,0),(0,1),(1,1)]
for (col,row),(name,dark) in zip(pos,names):
    x=98+col*(gw+22); y=320+row*(gh+22)
    rrect(s,x,y,gw,gh,fill=(C['dcard'] if dark else C['surf']),line=(None if dark else C['line']),radius=22)
    text1(s,x,y,gw,gh,name,30,(C['cream'] if dark else C['ink']),True,DISP,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
x=98+2*(gw+22); y=320+1*(gh+22)
add=rrect(s,x,y,gw,gh,fill=None,line=C['green'],radius=22,lw=2,dash='dash')
tf=add.text_frame; tf.vertical_anchor=MSO_ANCHOR.MIDDLE
para(tf,'+ ваша база',28,C['green'],True,DISP,PP_ALIGN.CENTER,first=True)
para(tf,'нужна ещё одна площадка — добавим под вас',15,C['muted'],False,TEXT,PP_ALIGN.CENTER)
text1(s,98,650,1650,60,'Шестая карточка важнее пяти первых: продукт подстраивается под ваш рынок, а не наоборот.',20,C['ink'],False,TEXT)

# 06 поиск словами
s=new(False,'Ввод запроса',6)
eyebrow(s,150,'05 / ВВОД ЗАПРОСА')
title(s,182,[['Опишите словами — критерии соберёт ИИ']])
shot(s,'01_main.png',98,300,820)
qx=970
dc=rrect(s,qx,300,852,90,fill=C['dcard'],radius=20)
shape_text(dc,'«кофейня, первый этаж, Новосибирск, до 150 тыс/месяц»',22,C['cream'],False,TEXT,PP_ALIGN.LEFT)
text1(s,qx,398,852,40,'↓',30,C['gold'],True,TEXT,align=PP_ALIGN.CENTER)
chips6=['тип: кофейня','этаж: первый','город: Новосибирск','бюджет: ≤ 150 тыс','ниша: общепит']
cx=qx; cy=450
for t in chips6:
    w=len(t)*17*0.55+36
    if cx+w>qx+852: cx=qx; cy+=54
    chip(s,cx,cy,t,on=True); cx+=w+12
text1(s,qx,cy+70,852,80,'Можно приложить документ с ТЗ — разберём его сами и превратим в фильтры.',20,C['muted'],False,TEXT,spacing=1.2)

# 07 фильтры
s=new(False,'Фильтры',7)
eyebrow(s,150,'06 / ФИЛЬТРЫ')
title(s,182,[['Фильтры, которых нет на площадках']])
feat=[('Без дублей по фото','склеиваем объект с разных сайтов',False),
      ('Скрыть фейки','объявления-приманки не показываем',True),
      ('ИИ-разбор описания','вытаскиваем смысл из текста',False),
      ('Пешая доступность','метро и остановки в шаговой зоне',False),
      ('Сначала из базы','проверенные объекты в приоритете',True),
      ('Только собственники','без комиссии посредника',False)]
gw=(1060-18)/2; gh=132
for i,(h,b,dark) in enumerate(feat):
    col=i%2; row=i//2
    x=98+col*(gw+18); y=300+row*(gh+18)
    rrect(s,x,y,gw,gh,fill=(C['dcard'] if dark else C['surf']),line=(None if dark else C['line']),radius=20)
    text1(s,x+24,y+22,gw-48,36,h,21,(C['cream'] if dark else C['ink']),True,TEXT)
    text1(s,x+24,y+66,gw-48,50,b,16,(C['mutedD'] if dark else C['muted']),False,TEXT)
shot(s,'02_filters.png',1200,300,622)

# 08 индекс
s=new(False,'Индекс локации',8)
eyebrow(s,150,'07 / ИНДЕКС ЛОКАЦИИ')
title(s,182,[['Балл 84 — и пять причин, почему именно 84']])
dc=rrect(s,98,300,470,340,fill=C['dcard'],radius=22)
text1(s,98,320,470,200,'84',110,C['mint'],True,DISP,align=PP_ALIGN.CENTER)
text1(s,98,500,470,30,'из 100',20,C['mutedD'],False,TEXT,align=PP_ALIGN.CENTER)
badge=rrect(s,98+105,548,260,44,fill=C['mint'],radius=22)
shape_text(badge,'ПЕРСПЕКТИВНАЯ',15,C['panelD'],True,TEXT)
bx=620; bw=1200
data=[('Аудитория',1.0,'10',False),('Доход',0.84,'8.4',False),('Трафик',1.0,'10',False),('Конкуренция',0.38,'3.8',True),('Инфраструктура',1.0,'10',False)]
for i,(l,f,v,r) in enumerate(data):
    bar(s,bx,330+i*58,bw,l,f,v,red=r)
text1(s,98,700,1700,80,[('Оценка разложена на факторы: видно не только ',C['ink'],False),('сколько',C['ink'],True),(', но и ',C['ink'],False),('за счёт чего',C['ink'],True),('. Слабую конкуренцию — 3.8 — показываем честно, а не прячем за средним баллом.',C['ink'],False)],20,C['ink'],False,TEXT,spacing=1.2)

# 09 источники данных
s=new(True,'Источники данных',9)
eyebrow(s,150,'08 / ИСТОЧНИКИ ДАННЫХ')
title(s,182,[['Считаем по фактам, а не по ощущениям']],dark=True)
src=[('🏢','Организации рядом',[('Сколько и каких заведений в радиусе, перенасыщена ли ниша. Источник — ',None,False),('2ГИС / Яндекс.Карты',None,True),('.',None,False)]),
     ('💰','Доход населения',[('Среднемесячный доход по региону. Источник — ',None,False),('Росстат',None,True),('.',None,False)]),
     ('👥','Население и трафик',[('Плотность и проходимость точки. Источники — ',None,False),('Росстат, 2ГИС',None,True),('.',None,False)]),
     ('🚇','Инфраструктура',[('Метро, остановки, школы, садики рядом. Источники — ',None,False),('2ГИС / Яндекс',None,True),('.',None,False)])]
gw=(1724-22)/2; gh=155
for i,(emo,h,body) in enumerate(src):
    x=98+(i%2)*(gw+22); y=310+(i//2)*(gh+22)
    rrect(s,x,y,gw,gh,fill=C['glass'],line=RGBColor(0x2c,0x37,0x2f),radius=22,lw=1)
    text1(s,x+26,y+20,gw-52,40,[(emo+'  ',C['mint'],False),(h,C['cream'],True)],25,C['cream'],True,DISP)
    text1(s,x+26,y+68,gw-52,80,body,19,C['cream'],False,TEXT,spacing=1.2)
text1(s,98,660,1700,40,'Названия источников уточните перед защитой — на слайде для клиента точность даёт вес аргументу.',16,RGBColor(0x8a,0x8f,0x84),False,TEXT)

# 10 вердикт ИИ
s=new(True,'Вердикт ИИ',10)
eyebrow(s,150,'09 / ВЕРДИКТ ИИ')
title(s,182,[['ИИ, который уже знает про локации —'],['а не тот, у которого вы спрашиваете']],dark=True)
text1(s,98,330,700,30,'Что модель знает до вопроса клиента:',19,C['mutedD'],False,TEXT)
kn=['данные по локации','конкуренты и насыщенность ниши','доход населения','история и динамика цены','варианты ниши под помещение']
for i,t in enumerate(kn):
    chip(s,98,380+i*56,t,on=True,dark=True)
vc=rrect(s,900,340,922,180,fill=C['dcard'],radius=22); vc.line.color.rgb=C['red']; vc.line.width=px(6)
text1(s,940,360,850,50,[('✕ Отклонено',C['red'],True)],30,C['red'],True,DISP)
text1(s,940,420,850,90,[('проходимость ',C['cream'],False),('3/100',C['cream'],True),(' · площадь ',C['cream'],False),('82 ≫ 50 м²',C['cream'],True),(' · прогноз выручки ~221 тыс ₽/мес',C['cream'],False)],20,C['cream'],False,TEXT,spacing=1.2)
text1(s,900,550,922,120,[('Ключевое: система ',C['cream'],False),('объясняет отказ',C['mint'],True),('. Это и есть качество анализа — не «нравится / не нравится», а конкретные цифры.',C['cream'],False)],20,C['cream'],False,TEXT,spacing=1.25)

# 11 конкуренты
s=new(False,'Окружение',11)
eyebrow(s,150,'10 / ОКРУЖЕНИЕ')
title(s,182,[['603 организации в радиусе 800 м —'],['и что это значит для вас']])
shot(s,'05_object_details.png',98,320,800)
rx=960
x=rx
for t,on in [('500 м',False),('800 м',True),('1.2 км',False),('2 км',False)]:
    x+=chip(s,x,320,t,on=on)+12
text1(s,rx,388,862,120,'Радиус переключается, ниша выбирается — видно рейтинг и число отзывов каждого соседа: Дентиформ, Айс, АЙС ветклиника…',19,C['ink'],False,TEXT,spacing=1.2)
rc=rrect(s,rx,548,862,190,fill=C['redBg'],line=C['red'],radius=22,lw=1.5)
text1(s,rx+28,568,806,70,'Насыщенное окружение — риск, а не преимущество',22,C['red'],True,DISP,spacing=1.0)
text1(s,rx+28,660,806,60,[('И мы показываем это ',C['ink'],False),('до сделки',C['ink'],True),(', а не после запуска точки.',C['ink'],False)],19,C['ink'],False,TEXT)

# 12 цена и собственник
s=new(False,'Цена и собственник',12)
eyebrow(s,150,'11 / ЦЕНА И СОБСТВЕННИК')
title(s,182,[['Видим, где тот же объект дешевле']])
text1(s,98,300,820,30,'Один объект на трёх площадках:',19,C['muted'],False,TEXT)
tri=[('Циан','45 тыс',False),('Яндекс','45 тыс',False),('N1 · min','36 тыс',True)]
gw=(820-28)/3
for i,(n,p,mn) in enumerate(tri):
    x=98+i*(gw+14)
    rrect(s,x,340,gw,120,fill=(C['greenBg'] if mn else C['surf']),line=(C['green'] if mn else C['line']),radius=20)
    text1(s,x,354,gw,28,n,17,(C['green'] if mn else C['muted']),False,TEXT,align=PP_ALIGN.CENTER)
    text1(s,x,384,gw,44,p,28,(C['green'] if mn else C['ink']),True,DISP,align=PP_ALIGN.CENTER)
gc=rrect(s,98,485,820,120,fill=C['goldSoftBg'],line=RGBColor(0xE3,0xC9,0x8A),radius=20)
tf=gc.text_frame; tf.word_wrap=True; tf.vertical_anchor=MSO_ANCHOR.MIDDLE
for m in ('margin_left','margin_right'): setattr(tf,m,px(26))
para(tf,[('💰 Дешевле всего в аренду: ',RGBColor(0x5f,0x4a,0x1c),False),('36 тыс ₽',RGBColor(0x5f,0x4a,0x1c),True),(' — возможно, напрямую от собственника, без комиссии агентства.',RGBColor(0x5f,0x4a,0x1c),False)],19,RGBColor(0x5f,0x4a,0x1c),False,TEXT,first=True,spacing=1.2)
text1(s,970,300,820,30,'История места:',19,C['muted'],False,TEXT)
hc=rrect(s,970,340,852,240,fill=C['surf'],line=C['line'],radius=22)
text1(s,994,360,804,34,[('На рынке',C['ink'],False),('        3 дня',C['ink'],True)],20,C['ink'],False,TEXT)
rrect(s,994,406,804,1,fill=C['line'],radius=0)
text1(s,994,424,804,34,[('● стабильно · единичное предложение',C['ink'],False)],20,C['ink'],False,TEXT)
rrect(s,994,470,804,1,fill=C['line'],radius=0)
text1(s,994,488,804,34,[('аренда 2026-08-18 · ',C['ink'],False),('активно',C['green'],True),('        123 тыс ₽',C['green'],True)],20,C['ink'],False,TEXT)
text1(s,970,600,852,90,'Видно, сдавалось ли раньше, как долго висит и стабильна ли цена — или мечется.',20,C['muted'],False,TEXT,spacing=1.2)

# 13 каннибализация
s=new(False,'Для сетей',13)
eyebrow(s,150,'12 / ДЛЯ СЕТЕЙ И ФРАНШИЗ')
title(s,182,[['Не открываем точку рядом с вашей же точкой']])
mapc=rrect(s,98,320,820,430,fill=RGBColor(0xFC,0xFA,0xF4),line=C['line'],radius=20)
# маяки и радиусы
oval(s,98+175,320+100,230,RGBColor(0xEC,0xF3,0xEF),line=C['green']);
oval(s,98+460,320+70,230,RGBColor(0xEC,0xF3,0xEF),line=C['green'])
oval(s,98+283,320+205,16,C['green']); oval(s,98+568,320+175,16,C['green'])
for cx,cy in [(98+340,320+186),(98+250,320+270),(98+534,320+235)]:
    text1(s,cx,cy,30,30,'✕',20,C['red'],True,TEXT,align=PP_ALIGN.CENTER)
oval(s,98+726,320+330,18,None if False else RGBColor(0xFC,0xFA,0xF4),line=C['green'])
text1(s,98+722,320+325,26,26,'○',16,C['green'],True,TEXT,align=PP_ALIGN.CENTER)
text1(s,120,700,780,30,'△ ваши точки · радиус 1 км · ✕ отсеяно · ○ подходит',16,C['muted'],False,TEXT)
text1(s,960,340,862,140,[('Загрузите адреса своей сети — объекты ближе ',C['ink'],False),('1 км',C['ink'],True),(' к вашим точкам отсеются автоматически. На карте точки видны маяками.',C['ink'],False)],22,C['ink'],False,TEXT,spacing=1.25)
chip(s,960,500,'экспансия без каннибализации',on=True)
text1(s,960,570,862,40,'Настраивается в кабинете, блок «Моя сеть».',20,C['muted'],False,TEXT)

# 14 жильё
s=new(False,'Жильё',14)
eyebrow(s,150,'13 / ЖИЛАЯ НЕДВИЖИМОСТЬ')
title(s,182,[['Один объект — разный балл под тип клиента']])
text1(s,98,320,470,30,'Критерии сегмента:',22,C['ink'],False,TEXT)
for i,t in enumerate(['метро и остановки','садики и школы рядом','цена за м² к медиане района']):
    chip(s,98,362+i*54,t)
text1(s,98,560,470,60,[('Медиана района: ',C['muted'],False),('149 322 ₽/м²',C['ink'],True),(' · тренд +0.8%',C['muted'],False)],20,C['muted'],False,TEXT)
bx=640; bw=1180
seg=[('Релокант',0.95,'95',False),('Инвестор',0.83,'83',False),('Студент',0.77,'77',False),('Пара / одиночка',0.60,'60',False),('Семья',0.02,'0',True)]
for i,(l,f,v,r) in enumerate(seg):
    bar(s,bx,340+i*58,bw,l,f,v,red=r)
text1(s,98,700,1700,60,[('Агент сразу знает, ',C['ink'],False),('кому показывать',C['ink'],True),(' объект: студии — релоканту и инвестору, а не семье.',C['ink'],False)],20,C['ink'],False,TEXT)

# 15 мониторинг
s=new(False,'Мониторинг',15)
eyebrow(s,150,'14 / МОНИТОРИНГ')
title(s,182,[['Сделку не пропустите: следит система, а не вы']])
steps=[('1','Сохранили запрос',False),('2','Площадки меняются',False),('3','Приходит уведомление',True)]
gw=(1724-2*72)/3
for i,(n,h,dark) in enumerate(steps):
    x=98+i*(gw+72)
    rrect(s,x,320,gw,150,fill=(C['dcard'] if dark else C['surf']),line=(None if dark else C['line']),radius=22)
    text1(s,x,336,gw,70,n,50,(C['mint'] if dark else C['gold']),True,DISP,align=PP_ALIGN.CENTER)
    text1(s,x,410,gw,40,h,22,(C['cream'] if dark else C['ink']),True,TEXT,align=PP_ALIGN.CENTER)
    if i<2: text1(s,x+gw+8,360,56,44,'→',30,C['gold'],True,TEXT,align=PP_ALIGN.CENTER)
notif=[('Цена снизилась на 12%',' по запросу'),('Новый объект',' по вашему запросу')]
for i,(a,b) in enumerate(notif):
    x=98+i*(842+22)
    rrect(s,x,520,842,110,fill=C['surf'],line=C['green'],radius=22,lw=1.5)
    text1(s,x+28,520,782,110,[('🔔  ',C['green'],False),(a,C['green'],True),(b,C['ink'],False)],22,C['ink'],False,TEXT,anchor=MSO_ANCHOR.MIDDLE)
text1(s,98,680,1700,40,'Не нужно сидеть в поиске часами — достаточно открыть уведомление.',20,C['muted'],False,TEXT)

# 16 что уносит клиент
s=new(False,'Результат',16)
eyebrow(s,150,'15 / РЕЗУЛЬТАТ РАБОТЫ')
title(s,182,[['Отчёт, КП и выгрузка — под вашим брендом']])
gw=(1724-2*22)/3
h=shot(s,'06_report.png',98,300,gw)
text1(s,98,300+h+16,gw,30,'Отчёт локации',22,C['ink'],True,TEXT)
text1(s,98,300+h+50,gw,26,'полная аналитика точки в PDF',17,C['muted'],False,TEXT)
x2=98+gw+22
shot(s,'07_kp.png',x2,300,gw)
text1(s,x2,300+h+16,gw,30,'Коммерческое предложение',22,C['ink'],True,TEXT)
text1(s,x2,300+h+50,gw,26,'готовое КП для клиента агента',17,C['muted'],False,TEXT)
x3=98+2*(gw+22)
xc=rrect(s,x3,300,gw,h,fill=C['dcard'],radius=20)
text1(s,x3,300,gw,h,'📊  Excel',26,C['mint'],True,DISP,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
text1(s,x3,300+h+16,gw,30,'Выгрузка',22,C['ink'],True,TEXT)
text1(s,x3,300+h+50,gw,26,'объекты и баллы таблицей',17,C['muted'],False,TEXT)
text1(s,98,760,1700,60,[('Логотип агентства, имя агента и описание подставляются автоматически. Продукт делает работу агента ',C['ink'],False),('презентабельной перед его клиентом',C['ink'],True),('.',C['ink'],False)],20,C['ink'],False,TEXT,spacing=1.2)

# 17 сравнение
s=new(True,'Сравнение',17)
eyebrow(s,150,'16 / СРАВНЕНИЕ')
title(s,182,[['Площадка показывает объявления. Локатор даёт решение']],size=30,dark=True)
rows=[('Объявления с одной базы','✓','✓ все базы сразу',False),
      ('Дубли между площадками','✕','✓ склеиваем по фото',False),
      ('Фейки и посредники','✕','✓ отсеиваем',False),
      ('Оценка локации','✕','✓ индекс 0–100 по 5 факторам',True),
      ('Конкуренты и ниша','✕','✓ анализ окружения',False),
      ('Где дешевле тот же объект','✕','✓ сравниваем цены',False),
      ('Каннибализация своей сети','✕','✓ есть',False),
      ('Мониторинг и уведомления','частично','✓ по вашему запросу',False),
      ('Отчёт и КП под свой бренд','✕','✓ есть',False)]
y0=270; rh=48
# заголовки колонок
text1(s,830,y0-34,200,26,'ПЛОЩАДКИ',14,C['goldS'],True,TEXT)
text1(s,1200,y0-34,300,26,'ЛОКАТОР',14,C['goldS'],True,TEXT)
for i,(crit,a,b,acc) in enumerate(rows):
    y=y0+i*rh
    rrect(s,98,y,1724,rh-8,fill=(RGBColor(0x25,0x33,0x2a) if acc else RGBColor(0x1e,0x29,0x22)),line=(C['mint'] if acc else None),radius=12,lw=1)
    text1(s,120,y,700,rh-8,crit,19 if not acc else 21,RGBColor(0xd9,0xd3,0xc4),False,TEXT,anchor=MSO_ANCHOR.MIDDLE)
    ac=C['mint'] if a=='✓' else (C['red'] if a=='✕' else RGBColor(0x8a,0x8f,0x84))
    text1(s,830,y,200,rh-8,a,19,ac,True,TEXT,anchor=MSO_ANCHOR.MIDDLE)
    text1(s,1200,y,610,rh-8,b,19 if not acc else 21,C['mint'],False,TEXT,anchor=MSO_ANCHOR.MIDDLE)
text1(s,98,y0+9*rh+6,1700,40,'Мы не конкурируем с площадками. Мы — слой поверх них.',23,C['mint'],True,TEXT)

# 18 роли
s=new(False,'Выгода по ролям',18)
eyebrow(s,150,'17 / ВЫГОДА ПО РОЛЯМ')
title(s,182,[['Три роли — три выгоды']])
roles=[('🏗️','Франшизе','Отбор локаций по индексу и отказ на слабых точках до аренды, а не после провала.',False),
       ('🔗','Сети','Экспансия без каннибализации и единый стандарт оценки всех точек.',True),
       ('👤','Агенту','Меньше времени на поиск, больше клиентов в работе и готовое КП под рукой.',False)]
gw=(1724-2*22)/3
for i,(emo,h,body,dark) in enumerate(roles):
    x=98+i*(gw+22)
    rrect(s,x,320,gw,360,fill=(C['dcard'] if dark else C['surf']),line=(None if dark else C['line']),radius=22)
    text1(s,x+36,344,gw-72,60,emo,40,(C['mint'] if dark else C['green']),False,TEXT)
    text1(s,x+36,414,gw-72,50,h,32,(C['cream'] if dark else C['ink']),True,DISP)
    text1(s,x+36,478,gw-72,170,body,20,(C['cream'] if dark else C['ink']),False,TEXT,spacing=1.3)

# 19 финал
s=new(True,'Попробовать',19)
eyebrow(s,250,'18 / ПОПРОБОВАТЬ')
by=title(s,290,[['Бесплатный тест'],['на вашем районе']],48,dark=True,w=1100)
pdots(s,98,by+28)
text1(s,98,by+92,980,80,'Пришлите один запрос — вернём подборку с баллами и отчёт по локации.',24,RGBColor(0xC9,0xC4,0xB7),False,TEXT,spacing=1.2)
text1(s,1230,560,560,40,'VKontakte · Telegram',21,RGBColor(0xC9,0xC4,0xB7),False,TEXT)
btn=rrect(s,1230,620,340,80,fill=C['red'],radius=16)
shape_text(btn,'Отправить запрос',26,C['surf'],True,DISP)
oval(s,1590,630,60,C['red']); text1(s,1590,630,60,60,'↗',24,C['surf'],True,TEXT,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)

prs.save(OUT)
print('OK ->', OUT, 'slides:', len(prs.slides._sldIdLst))
