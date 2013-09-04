import gc
gc.set_debug(gc.DEBUG_UNCOLLECTABLE | gc.DEBUG_INSTANCES | gc.DEBUG_OBJECTS)
from tkinter import *
import win32api, win32con, win32gui
import time
import subprocess
import os
import PIL.Image
import re
import collections
import pywintypes
import shutil
import schedule


## get mouse position
## win32api.GetCursorPos()

def tempfilename(suffix = ''):
    import tempfile
    return tempfile.mktemp(suffix, 'Stronghold Kingdoms Bot' + os.sep)

path = os.path.dirname(tempfilename())
shutil.rmtree(path)
if not os.path.isdir(path):
    os.mkdir(path)

height = 1
width = 1

m1 = Tk()
m1.overrideredirect(1)
m1.geometry("{}x{}-12-12".format(height, width))
##m1.configure(background = 'black')
##m1.attributes("-alpha", 0.50)
##
##m2 = Tk()
##m2.overrideredirect(1)
##m2.geometry("{}x{}".format(width, height))
##m2.configure(background = 'black')
##m2.attributes("-alpha", 0.50)
##
####m3 = Tk()
####m3.overrideredirect(1)
####m3.geometry("1x1")
####m3.configure(background = 'white')
##
##def show_mouse_at(x, y):
##    m1.geometry('+{}+{}'.format(x - height // 2, y - width // 2))
##    m1.lift()
##    m2.geometry('+{}+{}'.format(x - width // 2, y - height // 2))
##    m2.lift()
####    m3.geometry('+{}+{}'.format(x, y))
##
##show_mouse_at(screen_width() // 2, screen_height() // 2)
##

screen_width = m1.winfo_screenwidth
screen_height = m1.winfo_screenheight
def spiel_height():
    return spiel_bbox()[3]
def spiel_width():
    return spiel_bbox()[2]
my_height = 738
my_width = 1366
breite_des_rechten_menus = 1365 - 1167
höhe_des_oberen_menus = 114
my_breite_der_karte = my_width - breite_des_rechten_menus
my_höhe_der_karte = my_height - höhe_des_oberen_menus
start_der_karte_y = höhe_des_oberen_menus

def höhe_der_karte():
    return spiel_height() - höhe_des_oberen_menus

def breite_der_karte():
    return spiel_width() - breite_des_rechten_menus

mouse_speed = 4

def move_mouse(x, y):
    posx, posy = win32api.GetCursorPos()
    while posx != x or posy != y:
        if abs(x - posx) < mouse_speed: posx = x
        if x < posx: posx -= mouse_speed
        elif x > posx: posx += mouse_speed
        if abs(y - posy) < mouse_speed: posy = y
        if y < posy: posy -= mouse_speed
        elif y > posy: posy += mouse_speed
##        win32api.SetCursorPos((posx, posy))
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE |
                             win32con.MOUSEEVENTF_ABSOLUTE,
                             int(posx / screen_width() * 65535.0),
                             int(posy / screen_height() * 65535.0))
        time.sleep(0.01)
    win32api.SetCursorPos((posx, posy))

def mouse_drag(from_x, from_y, to_x, to_y):
    move_mouse(from_x, from_y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,from_x,from_y,0,0)
    move_mouse(to_x, to_y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,to_x,to_y,0,0)

def rechts(x, y):
    return x - my_width + spiel_width(), y

def unten(x, y):
    return x, y - my_height + spiel_height()

def karte_mitte(x, y):
    # x
    my_mitte = my_breite_der_karte // 2
    mitte = breite_der_karte() // 2
    x = x - my_mitte + mitte
    # y
    my_mitte = my_höhe_der_karte // 2
    mitte = höhe_der_karte() // 2
    y = y - my_mitte + mitte
    return x, y

def click(x, y):
    move_mouse(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN|win32con.MOUSEEVENTF_LEFTUP,100,100,0,0)
    wait()

def click_again():
    x, y = win32api.GetCursorPos()
    click(x, y)

def right_click(x, y):
    move_mouse(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)
    wait()

def wait():
    time.sleep(0.5)

tkinter_to_win32api = { 
    '4' : win32con.MOUSEEVENTF_LEFTDOWN,
    '5' : win32con.MOUSEEVENTF_LEFTUP,
    '6' : win32con.MOUSEEVENTF_MOVE,
    }

class MouseCapturer:
    mouse_last_down = mouse_last_up = None
    def __init__(self):
        t = Tk()
        t.overrideredirect(1)
        t.geometry('{}x{}+0+0'.format(screen_width(), screen_height()))
        t.attributes("-alpha", 0.20)
        t.configure(background = 'blue3')
        t.bind('<Escape>', lambda e: t.quit())
        self.now = time.time()
        self.events = []
        t.bind('<Button-1>', self.event_mouse)
        t.bind('<ButtonPress-1>', self.event_mouse_down)
        t.bind('<ButtonRelease-1>', self.event_mouse_up)
        t.bind('<Motion>', self.event_mouse)
        try:
            t.mainloop()
        finally:
            t.destroy()
    
    def event_mouse(self, e):
        type = tkinter_to_win32api[e.type]
        x, y = position = (e.x_root, e.y_root)
        print(e.type, 'click({}, {})'.format(x, y))
        self.events.append((time.time(), position, lambda: click(x, y)))
        if e.type != '6':
            t.geometry('1x1-1-1'.format(screen_width(), screen_height()))
            t.update()
            time.sleep(0.01)
            click(x, y)
            time.sleep(0.01)
            t.geometry('{}x{}+0+0'.format(screen_width(), screen_height()))
            t.update()

    def event_mouse_down(self, event):
        self.mouse_last_down = event.x_root, event.y_root

    def event_mouse_up(self, event):
        self.mouse_last_up = event.x_root, event.y_root

    def get_clip_rectangle(self):
        assert not (self.mouse_last_down or self.mouse_last_up), 'mouse was not pressed'
        x1, y1 = self.mouse_last_down
        x2, y2 = self.mouse_last_up
        if x1 > x2: x1, x2 = x2, x1
        if y1 > y2: y1, y2 = y2, y1
        return x1, y1, x2, y2
        
        
def capture_mouse_events():
    return MouseCapturer().events


def capture_mouse_position():
    pos = win32api.GetCursorPos()
    t = time.time()
    printed = False
    while 1:
        pos2 = win32api.GetCursorPos()
        t2 = time.time()
        if pos != pos2:
            pos = pos2
            t = t2
            printed = False
        elif t2 > t + 0.6 and not printed:
            print('click({}, {})'.format(*pos2))
            printed = True
        time.sleep(0.001)

wo = 'spiel geöffnet'

def öffnen(f):
    assert 'öffne' in f.__name__
    l = f.__name__.split('_')
    ort = l[l.index('öffne') + 1]
    def x(*args, **kw):
        global wo
        wo = ort
        return f(*args, **kw)
    x.__name__ = f.__name__
    return x

def im_menu(ort):
    def xx(f):
        def x(*args, **kw):
            assert wo == ort, '"{}" ist im Modus "{}" und nicht im Modus "{}". "öffne_{}()" davor fehlt.'.format(f.__name__, wo, ort, ort)
            return f(*args, **kw)
        x.__name__ = f.__name__
        return x
    return xx


windowhandle = None

@öffnen
def öffne_spiel():
    global windowhandle
    # GetWindowRect(handle) # koordinaten des spieles
    name = "Stronghold Kingdoms"
    handles = []
    def append_handle(handle, handles):
        handles.append(handle)
    win32gui.EnumWindows(append_handle, handles)
    for handle in handles:
        text = win32gui.GetWindowText(handle)
        if name.lower() in text.lower():
            for i in range(30):
                try:
                    win32gui.SetForegroundWindow(handle)
                    windowhandle = handle
                    return
                except pywintypes.error: pass
    raise Exception('Spiel nicht gestartet')


def spiel_koordinaten():
    assert windowhandle is not None, 'das spiel muss vorher geöffnet werden'
    left, top, right, bottom = win32gui.GetWindowRect(windowhandle)
    return left, top ,right, bottom

def spiel_bbox():
    x, y, right, bottom = spiel_koordinaten()
    assert x < 0 # wir brauchen einen rand!
    assert y < 0
    width = right + x # eigentlich - x aber wir ziehen den rand ab
    height = bottom + y
    x = 0
    y = 0
    return x, y, width, height

@im_menu('karte')
def zoom_raus():
    for i in range(5):
        right_click(378, 367)
        time.sleep(0.5)

@im_menu('karte')
def öffne_dorf_auf_karte():
    click(*rechts(933, 61))
    time.sleep(2.5)

@öffnen
def öffne_karte():
    click(*rechts(932, 91))
@öffnen
def öffne_dorf():
    click(*rechts(977, 96))
@öffnen
def öffne_gemeinde():
    click(*rechts(1027, 92))
@öffnen
def öffne_forschung():
    click(*rechts(1084, 95))
@öffnen
def öffne_rang():
    click(*rechts(1142, 94))
@öffnen
def öffne_quests():
    click(*rechts(1194, 94))
@öffnen
def öffne_angriffe():
    click(*rechts(1252, 95))
@öffnen
def öffne_berichte():
    click(*rechts(1286, 94))
@öffnen
def öffne_fraktion():
    click(*rechts(1345, 95))

image_folder = './images'
if not os.path.isdir(image_folder):
    os.mkdir(image_folder)

_screenshot = (None, 0) # filename, time

def last_screenshot_file_name():
    return _screenshot[0]

def screenshot():
    global _screenshot
    now = time.time()
    if now - 0.05 > _screenshot[1]:
        import screenshot
        filename = screenshot.screenshot()
        _screenshot = filename, now
    else:
        filename = _screenshot[0]
    return PIL.Image.open(filename)

##def pil2tkinter_image(img, master = None):
##    x0, y0, width, height = img.getbbox()
##    print(img.getbbox())
##    pi = PhotoImage(master = master, width = width - x0, height = height - y0)
##    for x in range(x0, width):
##        for y in range(y0, height):
##            pi.put('{#%02X%02X%02X}' % img.getpixel((x, y)), (x - x0, y - y0))
##    return pi
##    
##
##def capture_button_image(name):
##    t = Tk()
##    i = None
##    def ok():
##        nonlocal i
##        i = get_image()
##        t.quit()
##    b = Button(t, command = ok, border = 0)
##    b.pack(fill = BOTH, expand = True)
##    def get_image():
##        t.attributes("-alpha", 0)
##        s = screenshot()
##        t.attributes("-alpha", 1)
##        g = b.winfo_geometry()
##        print(g, s)
##        width, height, x, y = map(int, re.match('(\\d+)x(\\d+)\\+(\\d+)\\+(\\d+)', g).groups())
##        print(g, width, height, x, y)
##        return s.crop((x , y, x + width, y + height))
##    try:
##        t.protocol("WM_DELETE_WINDOW", t.quit)
##        t.mainloop()
##    finally:
##        t.destroy()
##    if i is None:
##        return 
##    i.save(os.path.join(images_folder, name + '.png'))
##    return i
##
##def get_image(name):
##    return PIL.Image.open(os.path.join(images_folder, name + '.png'))

def funktion(kathegorie, name, bildpfad):
    def erforsche_():
        öffne_forschung()
        locals()['öffne_' + kathegorie]()
        click_bild(bildpfad)
    erforsche_.__name__ += name
    erforsche_.__doc__ = "Erforsche {name} in der Kathegorie {kathegorie}".format(**locals())
    return im_menu('Forschung')(erforsche_)

forschungsordner = os.path.join(image_folder, 'Forschung')
for kathegorie in os.listdir(forschungsordner):
    kathegorieordner = os.path.join(forschungsordner, kathegorie)
    for bild in os.listdir(kathegorieordner):
        bildpfad = os.path.join(kathegorieordner, bild)
        name = os.path.splitext(bild)[0]
        f = funktion(kathegorie, name, bildpfad)
        locals()[f.__name__] = f

del funktion

@im_menu('forschung')
def öffne_forschungsliste():
    click(*rechts(1234, 341))

@im_menu('forschung')
@öffnen
def öffne_gewerbe():
    öffne_forschungsliste()
    click(112, 347)
    
@im_menu('forschung')
@öffnen
def öffne_militär():
    öffne_forschungsliste()
    click(260, 346)
    
@im_menu('forschung')
@öffnen
def öffne_landwirtschaft():
    öffne_forschungsliste()
    click(420, 345)
    
@im_menu('forschung')
@öffnen
def öffne_bildung():
    öffne_forschungsliste()
    click(626, 336)


name_zu_pfad = {}
namen = []

for dirpath, dirnames, filenames in os.walk(image_folder):
    for filename in filenames:
        name = os.path.splitext(filename)[0]
        if name.lower() in name_zu_pfad:
            raise ValueError('name {} kommt doppelt vor'.format(name))
        path = os.path.join(dirpath, filename)
        namen.append(name.capitalize())
        kathegorie = os.path.basename(dirpath)
        if kathegorie == 'geht':
            kathegorie = os.path.basename(os.path.dirname(dirpath))
        kathegorie = 'bilder_' + kathegorie.lower()
        name_zu_pfad[name] = name_zu_pfad[name.capitalize()] = \
                             name_zu_pfad[name.lower()] = \
                             name_zu_pfad[name.upper()] = path
        locals().setdefault(kathegorie, [])
        locals()[kathegorie].append(name.capitalize())
        locals()[kathegorie].sort()

def open_image(image):
    if not os.path.isfile(image):
        image = name_zu_pfad[image]
    return PIL.Image.open(image)

def ressourcen_positionen(*bilder):
    if not bilder: bilder = bilder_ressourcen
    return karten_positionen(*bilder)

def _karten_koordinaten():
    # wenn 1 und 2 gelten, gilt auch 3
    miny = start_der_karte_y # 3
    minx = 0 # 3
    maxx = minx + breite_der_karte() # 3
    maxy = miny + höhe_der_karte() # 3
    mittex = (minx + maxx) // 2
    mittey = (miny + maxy) // 2
    return minx, miny, maxx, maxy, mittex, mittey

def karten_positionen(*bilder):
    minx, miny, maxx, maxy, *x = _karten_koordinaten()
    return bild_positionen(minx, miny, maxx, maxy, bilder)

Ressource = collections.namedtuple('Ressource', ['name', 'x', 'y', 'pos'])

def bild_positionen(minx, miny, maxx, maxy, bilder):
    if not bilder: bilder = namen
    images = [open_image(name) for name in bilder]
    s = screenshot()
    s_getpixel = s.getpixel
    x0, y0, maxx, maxy = s.getbbox()
    assert x0 == 0, x0
    assert y0 == 0, y0
    assert maxx == screen_width() #1
    assert maxy == screen_height() #2
    ps1 = [(image.getpixel((0,0))[:3], image, image.getbbox()) for image in images]
    maxx -= min([img[2][2] for img in ps1])
    maxy -= min([img[2][3] for img in ps1])
    positions = []
    matches = {img : 0 for img in ps1}
##    print(minx, '-->',maxx, '|', miny, '-->', maxy)
    for x in range(minx, maxx):
        for y in range(miny, maxy):
            match = True
            px = s_getpixel((x, y))[:3]
            for img in ps1:
                if img[0] != px: continue
                matches[img] += 1
                bbox = img[2]
                matches[img]
                if maxx - x < bbox[2] or maxy - y < bbox[3]:
                    continue
                image_getpixel = img[1].getpixel
                for dx in range(bbox[2]):
                    for dy in range(bbox[3]):
                        if s_getpixel((x + dx, y + dy))[:3] != \
                           image_getpixel((dx, dy))[:3]:
                            match = False
                            break
                    if not match: break
                if match:
                    positions.append(Ressource(bilder[ps1.index(img)],
                                      x + width // 2,
                                      y + height // 2,
                                      pos[:]))
    for img, _matches in matches.items():
        if _matches > 20:
            print('many matches', _matches, 'for', bilder[ps1.index(img)])
    return positions

ressource_erkunden_click = lambda: click(*rechts(1270, 200))
ressource_erkunden_ausführen = lambda: click(*karte_mitte(824, 569))
ressource_erkunden_abbrechen = lambda: click(*karte_mitte(910, 210))

def ein_kundschafter():
    """=> ob ein kundschafter ausgewaehlt ist."""
    x, y = karte_mitte(309, 582)
    return bild_positionen(x - 50, y - 50, x + 50, y + 50, ('ein_kundschafter',))

@im_menu('karte')
def ressource_erkunden(x, y):
    """erkunde eine ressource => ob geklappt"""
    zerstöre_positionsbestimmung()
    click(x, y)
    ressource_erkunden_click()
    for i in range(10):
        if not ein_kundschafter():
            click(*karte_mitte(309, 582))
        else:
            break
    if i > 1:
        print(i, 'mal gebraucht, um den kundschafter auf 1 zu setzen', last_screenshot_file_name())
    ressource_erkunden_ausführen()
    if karten_positionen('ein_kundschafter'):
        # ausführen is fehlgeschlagen
        ressource_erkunden_abbrechen()
        return False
    return True

def sign(i):
    if i == 0: return 0
    return i // abs(i)

def zerstöre_positionsbestimmung():
    global pos
    pos = []

#################### funktionen, die die positionsbestimmung intakt halten

zerstöre_positionsbestimmung()
dorf = None

##def dorf_positionen_in_mitte():
##    if dorf:
##        x, y = dorf.x, dorf.y
##        ret = bild_positionen(x - 50, y - 50, x + 50, y + 50, ('dorf',))
##        if ret:
##            return ret
##    return karten_positionen('Dorf')

def starte_kartenpositionsbestimmung():
    global pos, dorf
    öffne_karte()
    öffne_dorf_auf_karte()
    x = breite_der_karte() // 2
    y = höhe_der_karte() // 2
    dorf = Ressource('Dorf', x, y, [x, y])
    pos = [dorf.x, dorf.y]
##    for i in range(3):
##        öffne_dorf_auf_karte()
##        dp = dorf_positionen_in_mitte()
##        if dp:
##            dorf = dp[0]
##            pos = [dorf.x, dorf.y]
##            dorf.set_pos(list(pos))
##            if i >= 1: print('dorf nach', i, 'versuchen gefunden', last_screenshot_file_name())
##            return
##    if dorf:
##        if i >= 1: print('dorf nach', i, 'versuchen nicht gefunden', last_screenshot_file_name())
##        pos = [dorf.x, dorf.y]
##    else:
##        raise Exception('Dorf wurde nicht gefunden', last_screenshot_file_name())

@im_menu('karte')
def scrolle_um(x, y):
    assert pos, 'starte_kartenpositionsbestimmung() vorher'
    if x == 0 and y == 0: return
    *__, mittex, mittey = _karten_koordinaten()
    max_scroll_x = breite_der_karte() // 2
    max_scroll_y = höhe_der_karte() // 2
    scroll_back = 0, 0
    while x != 0 or y != 0:
        sx = (x if abs(x) < max_scroll_x else max_scroll_x * sign(x))
        sy = (y if abs(y) < max_scroll_y else max_scroll_y * sign(y))
        if 0 < abs(sx) < 10 or 0 < abs(sy) < 10:
            sx += 30
            sy += 30
            assert scroll_back == (0, 0)
            scroll_back = -30, -30
##        print(sx, sy, x, y, max_scroll_x, max_scroll_y)
        to_x = mittex - sx //2
        to_y = mittey - sy //2
        from_x = mittex + sx - sx //2
        from_y = mittey + sy - sy //2
        x-= sx
        y -= sy
        mouse_drag(from_x, from_y, to_x, to_y)
        time.sleep(0.9)
        pos[0]-= sx
        pos[1]-= sy
    scrolle_um(*scroll_back)

class Ressource(Ressource):
    def scrolle_hin(self):
        assert pos, 'starte_kartenpositionsbestimmung() vorher'
        scrolle_um(pos[0] - self.pos[0], pos[1] - self.pos[1])

    def erkunde(self):
        self.scrolle_hin()
        v = ressource_erkunden(self.x, self.y)
        starte_kartenpositionsbestimmung()
        return v

    @property
    def relx(self):
        assert pos, 'starte_kartenpositionsbestimmung() vorher'
        return self.x - self.pos[0]

    @property
    def rely(self):
        assert pos, 'starte_kartenpositionsbestimmung() vorher'
        return self.y - self.pos[1]

    @property
    def abstand_zum_dorf(self):
        return ((self.relx - dorf.relx)**2 + (self.rely - dorf.rely)**2)**0.5

    def __lt__(self, other):
        return self.abstand_zum_dorf < other.abstand_zum_dorf

    def __eq__(self, other):
        differenz_pixel = 70 # 100 vielleicht?
        return (self.relx - other.relx)**2 + (self.rely - other.rely)**2 < \
               differenz_pixel**2

    def __hash__(self):
        return hash(1)

    def set_pos(self, pos):
        while self.pos:
            self.pos.pop()
        self.pos.extend(pos)

def sichte_ressourcen(zahl = 1000):
    res = set()
    h = höhe_der_karte() - 20
    b = breite_der_karte() - 20
    last = None
    for dx, dy in [(0,0),(0,h),(0,-h),(-b,0),(b,0),(b,h),(-b,h),(-h,b),(-b,-h)]:
        if last != (0,0):
            starte_kartenpositionsbestimmung()
        last = (dx, dy)
        scrolle_um(dx, dy)
        res.update(ressourcen_positionen())
        if len(res) >= zahl:
            break
    res = list(res)
    res.sort()
    return res
    
    
############################## Algorithmen

def algorithmus(funktion):
    

def test_erkunde_ressourcen(kundschafter = 3):
    def start():
        öffne_spiel()
        öffne_karte()
    ressourcen_erkundet = []
    start()
    while 1:
        try:
            res = sichte_ressourcen()
            if res:
                print(len(res), 'ressourcen gefunden:')
                for r in res:
                    if r in ressourcen_erkundet: erk = '(erkundet)'
                    else: erk = ''
                    print('\t', int(r.abstand_zum_dorf), '\t', r.name, erk, '\t', r)
            unbekannte = [r for r in res if r.name == 'Ressourcen' and \
                                            r not in ressourcen_erkundet]
            i = 0
            kein_kundschater_mehr = False
            for unbekannt in unbekannte:
                if unbekannt.erkunde():
                    ressourcen_erkundet.append(unbekannt)
                    print('erkunde unbekanntes', unbekannt)
                else:
                    kein_kundschater_mehr = True
                    break
                i += 1
            if res and not kein_kundschater_mehr:
                r = res[0]
                for i in range(i, kundschafter):
                    if r.erkunde():
                        ressourcen_erkundet.append(r)
                        print('erkunde', r)
                    else:
                        break
            print('kein Kundschafter mehr')
            time.sleep(60)
        except KeyboardInterrupt:
            while 1:
                try:
                    rrr = input('Keyboardinterrupt - pausiert. zum fortsetzen ENTER, zum beenden etwas anderes und ENTER')
                except KeyboardInterrupt: continue                
                if rrr:
                    raise KeyboardInterrupt()
                start()
                break
                

def test_erkunde_ressourcen1():
    öffne_spiel()
    öffne_karte()
    while 1:
        rp = ressourcen_positionen()
        if rp:
            for r in rp:
                print(r)
                if ressource_erkunden(r.x, r.y):
                    print('hingesendet')
                else:
                    print('kein kundschafter mehr')
                    time.sleep(300)
                öffne_dorf_auf_karte()
        else:
            time.sleep(10) # aktualisierungszeit



if __name__ == '__main__':
    test_erkunde_ressourcen()

