'''
@version: 2.2.0
@author: CrossingVoid
@date: 2024/07/01

The project_management.py is mainly for whole project management,
mostly all function the project will use, is inside here

version 1.1.0:
  add function pregress_bar to show progress in a new window or on canvas

version 2.1.0:
  rewrite function new_window

version 2.2.0:
  add new decorator effect_decorator provides some common used function in 
  effect animation
'''
from Tkinter_template.Assets.image import tk_image
from Tkinter_template.Assets.font import font_get, font_span
from tkinter import *
import time
import os


def create_menu(root):
    '''
    Can made menu own and inner code also use, need to bind to top_menu
    '''
    return Menu(root, font=font_get(16), tearoff=0)


def new_window(title, size: tuple, icon=None, position: tuple = None, grab_set=False):
    child_root = Toplevel()
    child_root.title(title)
    child_root.geometry(f"{size[0]}x{size[1]}")
    if icon:
        child_root.iconbitmap(os.path.join('images\\bitmaps', icon))

    if position:
        child_root.geometry(f"+{position[0]}+{position[1]}")
    if grab_set:
        child_root.grab_set()

    child_root.resizable(0, 0)
    return child_root


def making_widget(widget: str):
    try:
        return eval(widget)
    except:
        raise ValueError(f'The widget: {widget} does not exist in Tk')


def canvas_obj_states(canvas, mode, *tag):
    '''
    canvas: select a canvas to make manipulation on it
    mode can accept: {delete, hidden, normal}
    tag(tuple): stand for remain tag

    ***** PUT `H` IN TAGS, IF YOU DO WANT KEEP HIDDEN OF THE OBJ 
          AND WIDGET USING `H` IN TAG BASICLLY SHOULD HAS `HIDDEN` STATE *****
    '''
    for id_ in canvas.find_all():
        for tags in canvas.gettags(id_):
            if tags in tag:
                # not do thing on it
                break
        else:
            if mode == 'delete':
                canvas.delete(id_)
            elif mode == 'normal':
                if 'H' in canvas.gettags(id_):
                    # some obj keep hidden even do the switch
                    pass
                else:
                    canvas.itemconfigure(id_, state='normal')
            elif mode == 'hidden':
                canvas.itemconfigure(id_, state='hidden')


def select_cover(canvas: object, side: tuple, file):
    canvas.delete('cover')
    for x in range(100):
        canvas.create_image(
            0, (side[1])*x, anchor='nw', image=tk_image(file, *side), tags=('cover'))

        canvas.tag_lower('cover', canvas.find_all()[0])


def canvas_reduction(canvas, canvas_side, music_obj=None, cover=None, music=None):
    canvas.delete('all')
    canvas.xview_moveto(0)
    canvas.yview_moveto(0)
    if music_obj:
        music_obj.music = None

    if cover:
        select_cover(canvas, canvas_side, cover)
    if music and music_obj:
        music_obj.music = music
    # can adding for common use bind keys
    canvas.update()
    # unbind all event
    for event in canvas.bind():
        canvas.unbind(event)


def progress_bar(use_window: bool, remain: bool = False):
    common_params = {
        'outline': ('black', 'green'),
        'line width': 10,
        'position': (0, 0),
        "size": None,

    }
    window_params = {
        'bg': '#FFF9A6',  # light yellow
        "icon": False
    }
    canvas_params = {
        "canvas": None
    }

    class ProgressBar:
        params = {}

        def __init__(self, func) -> None:
            self.func = func

        def __depict_progress(self, proportion=0):
            self.canvas.delete('progressbar')
            p = self.__class__.params
            w, h = p["size"]
            p1, p2 = p["position"]
            complete_ratio = (proportion / p["total"]) if proportion else 0

            # point
            if w >= h:
                point = (p1 + int((w-h)/2),
                         p2 + p["line width"]/2,
                         p1 + int((w-h)/2) + h,
                         p2 + h - p["line width"] / 2)

            else:
                point = (p1 + p["line width"] / 2,
                         p2 + int((h-w)/2),
                         p1 + w - p["line width"] / 2,
                         p2 + int((h-w)/2) + w)

            crr = int(complete_ratio*360)
            # complete part
            if crr == 360:
                self.canvas.create_oval(*point, width=p["line width"], outline=p["outline"][1],
                                        tags=('progressbar', 'progressbar-complete'))
            else:
                self.canvas.create_arc(*point, width=p["line width"], start=90-crr, extent=crr,
                                       style='arc', outline=p["outline"][1],
                                       tags=('progressbar', 'progressbar-complete'))
            # not complete part
            if crr == 0:
                self.canvas.create_oval(*point, width=p["line width"], outline=p["outline"][0],
                                        tags=('progressbar', 'progressbar-incomplete'))
            else:
                self.canvas.create_arc(*point,  width=p["line width"], start=90, extent=360-crr, style='arc',
                                       outline=p["outline"][0],
                                       tags=('progressbar', 'progressbar-incomplete'))
            self.canvas.create_text(
                p1+int(w/2), p2+int(h/2),
                text=f'{round(complete_ratio*100, 1)}%', font=font_get(font_span('100.0%', h*0.9 if w >= h else w*0.9)),
                tags=('progressbar', 'progressbar-ratio'))

            if hasattr(self, 'window'):
                t = self.window.title
                t(t()[:t().rfind("-")+1] + f' {round(complete_ratio*100, 1)}%')
            self.canvas.update()

        def __start(self):
            p = self.__class__.params
            if use_window:
                self.window = new_window(
                    f"{self.func.__name__} -- Start", p["size"], icon=p["icon"])

                self.canvas = making_widget("Canvas")(self.window, width=p['size'][0],
                                                      height=p['size'][1], bg=p["bg"])
                self.canvas.grid()
                # update
                self.canvas.update()
                self.window.update_idletasks()
            else:
                self.canvas = p['canvas']
            self.__depict_progress()

        def __call__(self, *args, **kwargs):
            # parameters empty test

            for key, value in self.__class__.params.items():
                if value is None:
                    raise ValueError(f"The parameter: {key} is empty")

            self.__start()
            self.func(*args, **kwargs)

            if not remain:
                if hasattr(self, 'window'):
                    self.window.destroy()
                else:
                    self.canvas.delete('progressbar')

        def add_arg(self, params=None, **kwargs):
            if params is None:
                params = {}
            if t := (type(params)) != dict:
                raise ValueError(
                    f"The parameter params should be a dict, but got {t}")
            params.update(kwargs)

            self.__class__.params.update(params)

        def compelete_part(self, proportion):
            if "total" not in self.__class__.params:
                raise ValueError(
                    "Add total part before the first complete_part")
            self.__depict_progress(proportion)

    common_params.update(window_params if use_window else canvas_params)
    ProgressBar.params = common_params
    return ProgressBar


def effect_decorator(time_interval):
    """
        ATTENTION! 
            decorator will NOT create a new instance if you only 
            decorates once.
    """
    class Decorator:
        def __init__(self, func) -> None:
            self.func = func
            self.timer = time.time()

        def __call__(self, *args, **kwargs):
            if (t := time.time()) - self.timer > time_interval:
                result = self.func(*args, **kwargs)
                self.timer = t
                return result
    return Decorator


def post_menu(canvas, event, menu):
    canvas.bind(event, lambda e: menu.post(e.x_root, e.y_root))
