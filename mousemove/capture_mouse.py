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


__all__ = 'capture_mouse_events MouseCapturer capture_mouse_position'.split()
