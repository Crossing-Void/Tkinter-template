'''
@version: 1.2.1
@author: CrossingVoid
@date: 2024/07/01

The default_dashboard.py is mainly for 
well-built function in right side dashboard.

version 1.1.0:
  add class MusicPlayer wraping class Music and provide more precision operation
  for music playing or others

version 1.1.1:
  fix bug: time_show and date_show label configuration can be accessed by
  using variable receive the function return
  
version 1.2.1:
  new 
The `date_show` and `time_show` can access and modify by yourself
'''
from Tkinter_template.Assets.project_management import canvas_obj_states, making_widget
from Tkinter_template.Assets.font import font_get, font_span, measure, change_font, delete_font_set
from Tkinter_template.Assets.extend_widget import EffectButton
from Tkinter_template.Assets.image import tk_image
from mutagen.mp3 import MP3
from tkinter import *
import random
import time
import os


_time_, _date_ = None, None


def time_show(dashboard: object, side: tuple):
    global _time_
    _time_ = StringVar()
    time_label = Label(dashboard, textvariable=_time_,
                       font=font_get(font_span('00:00:00', side[0])), bd=1)
    time_label.grid()

    return time_label


def date_show(dashboard: object, side: tuple):
    global _date_
    _date_ = StringVar()
    date_label = Label(dashboard, textvariable=_date_,
                       font=font_get(font_span('2022/09/09  (Mon)', side[0])), bd=1)
    date_label.grid()

    return date_label


def table(canvas: object, dashboard: object, side: tuple):
    def click():
        if table_button['bg'] == 'gray':
            table_button['bg'] = 'red'
            canvas_obj_states(
                canvas, 'hidden', 'cover')
            # unbind all event
            for event in table_button.bind():
                table_button.unbind(event)
        elif table_button['bg'] == 'red':
            table_button['bg'] = 'gray'
            table_button.bind('<Enter>', enter)
            table_button.bind('<Leave>', leave)

    def enter(event):
        canvas_obj_states(
            canvas, 'hidden', 'cover')
        table_button['bg'] = 'gray'

    def leave(event):
        canvas_obj_states(
            canvas, 'normal', 'cover')
        table_button['bg'] = 'white'

    table_button = Button(dashboard, width=1, font=font_get(16),
                          bd=3, bg='white', command=click, text='P')
    table_button.place(
        x=side[0], y=side[1], anchor='se')
    table_button.bind('<Enter>', enter)
    table_button.bind('<Leave>', leave)


def time_flush():
    day_change = dict(zip((0, 1, 2, 3, 4, 5, 6),
                          ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')))
    time_now = time.localtime(time.time())
    timeStr = f'{time_now.tm_hour:02d}:{time_now.tm_min:02d}:{time_now.tm_sec:02d}'
    dateStr = f'{time_now.tm_year:04d}/{time_now.tm_mon:02d}/{time_now.tm_mday:02d}  ({day_change[time_now.tm_wday]})'
    try:
        _time_.set(timeStr)
    except:
        pass
    try:
        _date_.set(dateStr)
    except:
        pass


class MusicPlayer:
    '''
    a Music superset
    a Music package contain more fancy function
    '''

    def __init__(self, dashboard: object, music_obj: object):
        self.d = dashboard
        self.dw = self.d['width']
        self.fs = 16  # for font size
        self.mo = music_obj

        self.__music_now = making_widget('StringVar')()
        # for showing playing music name now
        self.__pass_time = making_widget('StringVar')()
        # for storing how the offset is
        self.__length = making_widget('StringVar')()
        # for storing how long the music is
        self.__enter_rec = making_widget('IntVar')(value=0)
        # for judging if user enter playduration rec
        self.__page_number = making_widget('IntVar')()
        # for recording the page number now

        self.__build_music_canvas()
        self.__build_initial_layout()

    def __build_music_canvas(self):
        self.__music_canvas = making_widget('Canvas')(
            self.d, width=self.dw, height=500,
            bg='lightblue', bd=0, highlightthickness=0
        )
        self.__music_canvas_side = int(self.__music_canvas['width']), int(
            self.__music_canvas['height'])
        self.__music_canvas.grid()

    def __second_fmt_change(self, sec):
        '''
        passing int -> '00:00' (str)
        passing str -> 254 (int)
        '''
        if type(sec) in (int, float):
            if 0 <= sec <= 59*60 + 59:
                return f'{int(sec//60):02d}:{int(sec%60):02d}'
            else:
                self.__music_canvas.itemconfigure(
                    'musicplayerplaybutton-pause', state='hidden')
                self.__music_canvas.itemconfigure(
                    'musicplayerplaybutton-play', state='normal')
                return '00:00'

        elif type(sec) == str:
            return 60*int(sec[:2]) + int(sec[3:5])

    def __music_now_label_change_color(self, dashboard, now_music):
        for child in dashboard.winfo_children():
            if type(child) == making_widget('Label'):
                if child['text'] == self.__music_now.get():
                    child['fg'] = 'Indigo'
                else:
                    if child['text'] != 'Empty!':
                        child['fg'] = 'black'

    def _get_mp3_info(self, filename, info):
        '''
        info(str){length, bitrate}
        '''

        return eval(f'MP3(os.path.join("musics", filename)).info.{info}')

    def __build_initial_layout(self):
        # auto play
        try:
            self.play_a_music(random.choice(os.listdir('musics')))
        except:
            pass
        # auto play
        cumulateHeight = 0

        def header():
            '''
            This do icon and title
            '''
            nonlocal cumulateHeight
            fit_height = font_span('Music List', self.__music_canvas_side[0])
            # for not to deformed
            cumulateHeight += fit_height
            self.__music_canvas.create_image(
                0, 0, image=tk_image('musicplayer.ico', fit_height, fit_height, dirpath='images\\musicplayer'), anchor='nw',
                tags=('musicplayer', 'musicplayericon'))
            self.__music_canvas.create_text(fit_height, 0, text='Music List', anchor='nw', font=font_get(
                font_span('Music List', self.__music_canvas_side[0]-fit_height)), tags=('musicplayer', 'musicplayertitle'))
            self.__music_canvas.create_line(0, cumulateHeight, self.__music_canvas_side[0], cumulateHeight, width=1, tags=('musicplayer',
                                                                                                                           'musicplayerline1'))
            cumulateHeight += 2 + 1

        def playing():
            '''
            This do now playing indication
            '''
            def pause():
                self.mo.pause = True
                self.__music_canvas.itemconfigure(
                    'musicplayerplaybutton-pause', state='hidden')
                self.__music_canvas.itemconfigure(
                    'musicplayerplaybutton-play', state='normal')

            def play():
                if self.__pass_time.get() == '00:00':
                    self.play_a_music(self.__music_now.get()+'.mp3')
                    return
                self.mo.pause = False
                self.__music_canvas.itemconfigure(
                    'musicplayerplaybutton-pause', state='normal')
                self.__music_canvas.itemconfigure(
                    'musicplayerplaybutton-play', state='hidden')

            nonlocal cumulateHeight
            self.__music_canvas.create_window(self.__music_canvas_side[0]//2, cumulateHeight, anchor='n', window=making_widget(
                'Label')(self.__music_canvas, font=font_get(self.fs), bg='lightblue', textvariable=self.__music_now),
                tags=('musicplayer', 'musicplayernow')
            )
            cumulateHeight += self.fs * 4 / 3
            self.__music_canvas.create_rectangle(self.__music_canvas_side[0]*0.2, cumulateHeight, self.__music_canvas_side[0]*0.8, cumulateHeight+50,
                                                 width=0, tags=('musicplayer', 'musicplayerdurationrec'))
            self.__music_canvas.tag_bind('musicplayerdurationrec',
                                         '<Enter>', lambda event: self.__enter_rec.set(1))
            self.__music_canvas.tag_bind('musicplayerdurationrec',
                                         '<Leave>', lambda event: self.__enter_rec.set(0))
            cumulateHeight += 25
            self.__music_canvas.create_line(self.__music_canvas_side[0]*0.2, cumulateHeight, self.__music_canvas_side[0]*0.8, cumulateHeight, width=1,
                                            tags=('musicplayer', 'musicplayerdurationbar'))
            self.__music_canvas.create_window(self.__music_canvas_side[0]*0.1, cumulateHeight, window=making_widget(
                'Label')(self.__music_canvas, font=font_get(self.fs), bg='lightblue', textvariable=self.__pass_time),
                tags=('musicplayer', 'musicplayertimer')
            )
            self.__music_canvas.create_window(self.__music_canvas_side[0]*0.9, cumulateHeight, window=making_widget(
                'Label')(self.__music_canvas, font=font_get(self.fs), bg='lightblue', textvariable=self.__length),
                tags=('musicplayer', 'musicplayerlength')
            )
            cumulateHeight += 25
            self.__music_canvas.create_line(0, cumulateHeight, self.__music_canvas_side[0], cumulateHeight, width=1, tags=('musicplayer',
                                                                                                                           'musicplayerline2'))
            self.__music_canvas.create_window(self.__music_canvas_side[0]/2, cumulateHeight, anchor='s', window=EffectButton(
                ('aqua', 'black'),  self.__music_canvas, command=pause, bg='lightblue', image=tk_image(
                    'pause.png', height=15, dirpath='images\\musicplayer'
                )), tags=('musicplayer', 'musicplayerplaybutton-pause'))
            self.__music_canvas.create_window(self.__music_canvas_side[0]/2, cumulateHeight, anchor='s', window=EffectButton(
                ('aqua', 'black'),  self.__music_canvas, command=play, bg='lightblue', image=tk_image(
                    'play.png', height=15, dirpath='images\\musicplayer'
                )), tags=('musicplayer', 'musicplayerplaybutton-play'), state='hidden')
            cumulateHeight += 3

        def music_list():
            '''
            This do music list frame
            '''
            nonlocal cumulateHeight
            self.listFrame = making_widget('Frame')(self.__music_canvas, width=self.__music_canvas_side[0],
                                                    height=self.__music_canvas_side[1]-50-cumulateHeight, bg='lightblue')
            self.__music_canvas.create_window(0, cumulateHeight, window=self.listFrame, anchor='nw', tags=('musicplayer',
                                                                                                           'musicplayerlistframe'))
            cumulateHeight = 450
            self.__music_canvas.create_line(0, cumulateHeight,  self.__music_canvas_side[0], cumulateHeight, width=3, tags=('musicplayer',
                                                                                                                            'musicplayerline3'))
            cumulateHeight += 3

        def change_page():
            '''
            This do page change function
            '''
            # start = 15, interval 10 real width 30
            # start = 3
            nonlocal cumulateHeight

            for i in range(1, 6):
                self.__music_canvas.create_window(15+40*(i-1),  self.__music_canvas_side[1], window=making_widget('Radiobutton')(self.__music_canvas, bg='white', indicatoron=0, variable=self.__page_number, value=i, selectcolor='purple', width=2,
                                                                                                                                 font=font_get(self.fs), text=str(i), command=lambda args=i: self.__set_page(args)), anchor='sw',
                                                  tags=('musicpplayer', f'musicplayerpagebutton{i}'))
            self.__music_canvas.create_window(*self.__music_canvas_side, window=EffectButton(('aqua', 'black'),  self.__music_canvas, bg='lightblue',
                                                                                             image=tk_image('right.png', 27, dirpath='images\\musicplayer'), command=lambda args='right': self.__set_page(extend_func=args)), tags=('musicplayer', 'musicplayerrightbutton'), anchor='se')
            self.__music_canvas.create_window(self.__music_canvas_side[0]-27-10, self.__music_canvas_side[1], window=EffectButton(('aqua', 'black'), self.__music_canvas, bg='lightblue',
                                                                                                                                  image=tk_image('left.png', 27, dirpath='images\\musicplayer'), command=lambda args='left': self.__set_page(extend_func=args)), tags=('musicplayer', 'musicplayerrightbutton'), anchor='se')

        header()
        playing()
        music_list()
        change_page()
        self.__set_page(1)

    def __load_music_list(self, dashboard, page):
        def get_number():
            for number in range(1, 51):
                if measure('n'*number, self.fs) > self.__music_canvas_side[0] - self.fs*4/3:
                    return number - 1

        def enter(event, args, play_):
            play_.grid(row=args, column=2)
            others = [effectbutton for effectbutton in dashboard.winfo_children() if type(
                effectbutton) == EffectButton]
            others.remove(play_)
            for other in others:
                other.grid_forget()

        def leave(event, play_):
            if measure('n'*get_number(), self.fs) < event.x < measure('n'*(get_number()+1), self.fs):
                pass
            else:
                play_.grid_forget()

        def dashboardleave(event):
            for play in dashboard.winfo_children():
                if type(play) == EffectButton:
                    play.grid_forget()

        musicPerPage = 7
        musicList = [music for music in os.listdir('musics')
                     if os.path.splitext(os.path.join('musics', music))[-1] == '.mp3']

        for child in dashboard.winfo_children():
            child.destroy()

        for musicIndex in range(start := musicPerPage*(page-1), end := musicPerPage*page):
            try:
                label = making_widget('Label')(dashboard, font=font_get(self.fs),
                                               text=os.path.splitext(musicList[musicIndex])[0], bg='lightblue', anchor='w',
                                               width=get_number())
                play = EffectButton(('aqua', 'black'), dashboard, bg='lightblue',
                                    image=tk_image('play.png', width=int(
                                        self.fs*4/3), dirpath='images\\musicplayer'),
                                    command=lambda args=musicList[musicIndex]: self.play_a_music(args))
                label.bind('<Enter>', lambda event, args=musicIndex -
                           start+1, play_=play: enter(event, args, play_))
                label.bind('<Leave>', lambda event,
                           play_=play: leave(event, play_))
                label.grid(row=musicIndex-start+1, column=1, sticky='we')
            except IndexError:
                if musicIndex == start:
                    making_widget('Label')(dashboard,
                                           font=font_get(50), text='Empty!', bg='lightblue',
                                           fg='red').grid()
                    break

        dashboard.bind('<Leave>', dashboardleave)

    def __set_page(self, page=0, extend_func=None):
        if extend_func:
            if extend_func == 'right':
                if (now := self.__page_number.get()) == 5:
                    pass
                else:
                    self.__page_number.set(now+1)
            elif extend_func == 'left':
                if (now := self.__page_number.get()) == 1:
                    pass
                else:
                    self.__page_number.set(now-1)
        else:
            self.__page_number.set(page)
        self.__load_music_list(self.listFrame, self.__page_number.get())
    # ---------------------------------------------------------------------------------

    def play_a_music(self, file):
        try:
            self.__music_canvas.itemconfigure(
                'musicplayerplaybutton-pause', state='normal')
            self.__music_canvas.itemconfigure(
                'musicplayerplaybutton-play', state='hidden')
        except:
            pass

        self.__length.set(self.__second_fmt_change(
            self._get_mp3_info(file, 'length')))
        self.__music_now.set(os.path.splitext(file)[0])
        self.mo.music = file

    # ---- need put in while loop ----
    def set_ball(self):
        time_pass = self.mo.get_play_time()

        self.__music_now_label_change_color(
            self.listFrame, self.__music_now.get())
        self.__pass_time.set(self.__second_fmt_change(
            time_pass
        ))

        self.__music_canvas.delete('musicplayerdurationball')
        ball_r = 3
        progress = time_pass / self.__second_fmt_change(
            self.__length.get())  # ratio
        a, b, c, d = self.__music_canvas.coords('musicplayerdurationbar')
        center = (c-a)*progress

        if self.__enter_rec.get():
            self.__music_canvas.create_oval(
                a+center-ball_r*3, b-ball_r*3, a+center+ball_r*3, b+ball_r*3, fill='white', tags=('musicplayer', 'musicplayerdurationball')
            )

        else:
            self.__music_canvas.create_oval(
                a+center-ball_r, b-ball_r, a+center+ball_r, b+ball_r, fill='black', tags=('musicplayer', 'musicplayerdurationball')
            )


class BulletinBoard:
    params = {
        "bg": "#FFE4B5",
        "title": "BULLETIN BOARD",
        "title display": True
    }

    def __init__(self, dashboard, height: int) -> None:
        self.p = self.__class__.params
        self.ds = int(dashboard["width"]), height

        # title
        if self.p["title display"]:
            font = font_get(1)[0]
            if font.lower() != "castellar":
                change_font("Castellar")
                making_widget("Label")(
                    dashboard, text=self.p["title"], bg=self.p["bg"], font=font_get(font_span(self.p["title"], self.ds[0]))).grid(sticky="nwse")
                change_font(font)
            else:
                making_widget("Label")(
                    dashboard, text=self.p["title"], bg=self.p["bg"], font=font_get(font_span(self.p["title"], self.ds[0]))).grid(sticky="nwse")
        self.c = making_widget("Canvas")(
            dashboard, width=self.ds[0], height=self.ds[1], bg=self.p["bg"])
        self.c.grid()

    def __compute_height(self):
        find = False
        for height in range(getattr(self, "start", 0), self.ds[1], 1):
            if self.c.find_overlapping(0, height, self.ds[0], height):
                find = True
            else:
                if find:
                    self.start = height
                    break

    def get_progress_bar_arguments(self):
        return {
            "canvas": self.c,
            "size": (self.ds[0], self.ds[1] - getattr(self, "start", 0)),
            "position": (0, getattr(self, "start", 0))
        }

    def paste_message_in_single_line(self, message: str, font_size_upper_bond: int = 1000):
        self.c.create_text(0, getattr(self, "start", 5), text=message, font=font_get(
            font_span(message, self.ds[0], upper_bound=font_size_upper_bond)), anchor="nw")

        self.__compute_height()

    def paste_message_in_mutiple_line(self, message: str, font_size: int, wrap: str = "word"):
        wrap = wrap.capitalize()
        if wrap == "None":
            self.c.create_text(0, getattr(
                self, "start", 5), text=message, font=font_get(font_size), anchor="nw")
            self.__compute_height()
        else:
            lines = []
            if wrap == "Word":
                message = message.split()
            while True:
                for i in range(len(message)):
                    print(message)
                    if measure(message[:i+1], font_size) > self.ds[0]:
                        lines.append(message[:i])
                        message = message[i:]
                        break
                else:
                    lines.append(message)
                    break

            # render lines
            for line in lines:
                self.c.create_text(0, getattr(
                    self, "start", 5), text=line, font=font_get(font_size), anchor="nw")
                self.__compute_height()
