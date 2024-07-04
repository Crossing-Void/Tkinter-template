'''
@version: 1.2.0
@author: CrossingVoid
@date: 2024/07/02

The default_menu.py is mainly for optional
function in the selective function.

version 1.1.0:
  add function main_canvas_focus, it allowed user to
  set focus on main canvas by click menu command

version 1.2.0:
  add function adjuest_volume, it can adjust main background music and
  all channel of sound effect volume separately
'''
from Tkinter_template.Assets.project_management import new_window, select_cover, making_widget
from Tkinter_template.Assets.font import font_get
from Tkinter_template.Assets.image import tk_image
from PIL import ImageColor
from tkinter import *
import os


def background_color(canvas: object, icon=None):
    def color(position):
        str_of_color = f'#{red.get():02x}{green.get():02x}{blue.get():02x}'
        canvas.config(bg=str_of_color)

    def select_color(color):
        canvas.config(bg=color)
        win.destroy()

    if icon is None:
        win = new_window('Background Color', )
    else:
        win = new_window('Background Color', icon)

    red = Scale(win, font=font_get(20), bg='red', length=255, tickinterval=50, command=color,
                from_=0, to=255, label='Red')
    green = Scale(win, font=font_get(20), bg='green', length=255, tickinterval=50, command=color,
                  from_=0, to=255, label='Green')
    blue = Scale(win, font=font_get(20), bg='blue', length=255, tickinterval=50, command=color,
                 from_=0, to=255, label='Blue')

    color_select = ['chocolate', 'lightblue',
                    'violet', 'silver', 'indigo']
    x, y, z = ImageColor.getrgb(canvas['bg'])
    red.set(x)
    green.set(y)
    blue.set(z)
    red.grid(row=1, column=1, rowspan=len(
        color_select), sticky='sn')
    green.grid(row=1, column=2, rowspan=len(
        color_select), sticky='sn')
    blue.grid(row=1, column=3, rowspan=len(
        color_select), sticky='sn')

    index = 1
    for item in color_select:
        Button(win, font=font_get(20), bg=item, height=15//len(color_select), fg='black', text=item,
               command=lambda x=item: select_color(x)).grid(row=index, column=4, sticky='ew')
        index += 1


def canvas_cover(canvas: object, canvas_side: tuple, side: tuple = None, icon=None):
    def click(num):
        canvas_.itemconfigure(f'rec{num}', state='normal')
        for i in range(len(cover)):
            if i != num:
                canvas_.itemconfigure(f'rec{i}', state='hidden')

    def double_click(num):
        select_cover(canvas, canvas_side, cover[num])
        win.destroy()

    if side is None:
        side = canvas_side
    if icon is None:
        win = new_window(
            'Windows Cover', maxsize=side)
    else:
        win = new_window(
            'Windows Cover', icon, maxsize=side)
    scrollbar = Scrollbar(win)
    scrollbar.grid(row=1, column=2, sticky='ns')
    canvas_ = Canvas(win, width=side[0]-int(scrollbar['width']), height=side[1], bg=canvas['bg'],
                     yscrollcommand=scrollbar.set)
    canvas_.grid(row=1, column=1)
    scrollbar['command'] = canvas.yview

    cover = [img for img in os.listdir('images\\covers') if img.endswith('png')
             or img.endswith('jpg') or img.endswith('jpeg')]
    wi_inter, hi_inter = 100, 120
    wi = (int(canvas_['width']) - 2*wi_inter - 20)//3
    hi = wi * 3 // 4

    for i in range(len(cover)):

        canvas_.create_image(20+i % 3 * (wi + wi_inter), 20+i//3 * (hi + hi_inter), anchor='nw',
                             image=tk_image(
            cover[i], wi, hi),
            tags=(f'img{i}'))

        canvas_.create_text(20+i % 3 * (wi + wi_inter) + wi//2, 20+i//3 * (hi + hi_inter)+20+24//2 + hi, font=font_get(24),
                            text=cover[i], tags=(f'text{i}'))

        x, y, x2, y2 = (20+i % 3 * (wi + wi_inter), 20+i//3 * (hi + hi_inter),
                        20+i % 3 * (wi + wi_inter)+wi, 20+i//3 * (hi + hi_inter)+hi)
        canvas_.create_rectangle(x-4, y-4, x2+4, y2+4, width=4, outline='gold',
                                 state='hidden', tags=(f'rec{i}'))

        canvas_.tag_bind(f'img{i}', '<Button-1>',
                         lambda event, x=i: click(x))
        canvas_.tag_bind(
            f'img{i}', '<Double-Button-1>', lambda event, x=i: double_click(x))

    canvas_['scrollregion'] = (
        0, 0, int(canvas['width']), 20+i//3 *
        (hi + hi_inter)+20+24//2 + hi+60
    )
    canvas_.bind('<MouseWheel>', lambda event: canvas_.yview_scroll(-(event.delta//120), 'units')
                 )


def main_canvas_focus(canvas: object):
    canvas.focus_set()


def adjust_volume(music_object, soundeffect_object, icon=False):
    class Volume:
        order = 0
        img_name = ['Volume_mute', 'Volume_medium', 'Volume_high']

        def __init__(self, volume_body) -> None:
            self.volume_body = volume_body  # str for channel and object for music
            volume = (soundeffect_object.manipulate_channel("get_volume", channel=volume_body) if type(volume_body) == str
                      else volume_body.get_volume())
            self.var = making_widget("DoubleVar")(value=volume)
            self.scale = making_widget('Scale')(canvas, relief='solid', bd=3, length=400, orient='horizontal', from_=0, to=1, resolution=0.1,
                                                tickinterval=0.2, showvalue=0, width=15, variable=self.var, font=font_get(16), command=self.__adjust)
            self.label = making_widget('Label')(canvas, font=font_get(24, True),
                                                textvariable=self.var, bg='coral')
            o = self.__class__.order
            canvas.create_window(
                0, (100+separtae_line_width)*o, anchor='nw', window=self.scale)
            canvas.create_window(
                0,  (100+separtae_line_width)*o+60, anchor='nw', window=self.label)
            canvas.create_line(0, (100+(separtae_line_width+1)/2)*(o+1),
                               width, (100+(separtae_line_width+1)/2)*(o+1), width=separtae_line_width, tags=(f"line-{o}"))
            for img in self.__class__.img_name:
                canvas.create_image(
                    width, (100+separtae_line_width)*o, anchor='ne', image=tk_image(f"{img}.ico", 96, 96, dirpath="images\\adjust_volume"),
                    tags=(f"{self.var}-{img}"), state="hidden")
            canvas.create_text(width-96, (100+separtae_line_width)*o+96/2, anchor="e",
                               text=f"Channel\n{volume_body}" if type(volume_body) == str else "Music", justify="center", font=font_get(30))
            self.__class__.order += 1
            self.__adjust(None)

        def __adjust(self, position):
            if type(self.volume_body) == str:
                # channel
                soundeffect_object.manipulate_channel(
                    "set_volume", self.var.get(), channel=self.volume_body)
            else:
                music_object.set_volume(self.var.get())

            for name, condition in zip(self.__class__.img_name, ((0.0, 0.01), (0.1, 0.5), (0.6, 1.0))):
                canvas.itemconfig(
                    f"{self.var}-{name}", state="normal" if condition[0] <= self.var.get() <= condition[1] else "hidden")

    soundeffect_channels = soundeffect_object.get_channels_name()
    width = 700
    separtae_line_width = 3
    height = 100 + (100+separtae_line_width) * len(soundeffect_channels)

    win = new_window("Adjust Volume", (width, height), icon)
    canvas = making_widget('Canvas')(
        win, width=width, height=height, bg='coral', highlightthickness=0)
    canvas.grid()

    Volume(music_object)
    for channel in soundeffect_channels:
        Volume(channel)
    canvas.delete(f"line-{Volume.order-1}")
