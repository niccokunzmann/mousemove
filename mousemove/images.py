import .screenshot as _screenshot
import PIL.Image
import files
from Tkinter import PhotoImage

_screenshot = (None, 0) # filename, time

def screenshot():
    global _screenshot
    now = time.time()
    if now - 0.05 > _screenshot[1]:
        import screenshot
        filename = _screenshot.screenshot()
        _screenshot = filename, now
    else:
        filename = _screenshot[0]
    return PIL.Image.open(filename)

def last_screenshot_file_name():
    return _screenshot[0]

def pil2tkinter_image(img, master = None):
    if isinstance(img, str):
        img = open_image(img)
    x0, y0, width, height = img.getbbox()
    l = []
    for y in range(y0, height):
        l.append('{')
        for x in range(x0, width):
            l.append('#%02X%02X%02X' % img.getpixel((x, y)))
        l.append('}')
    data = ' '.join(l)
    pi = PhotoImage(master = master)
    pi.put(data, (0,0))
    return pi

name_zu_pfad = {}
namen = []

image_folder = files.image_folder

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



__all__ = 'screenshot last_screenshot_file_name pil2tkinter_image open_image'\
          ''.split()



