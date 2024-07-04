'''
@version: 1.3.0
@author: CrossingVoid
@date: 2024/07/02

The extend_widget.py is mainly for some widget basic on tk widget,
adding some features on them

version 1.1.0:
  add PlaceholderEnter class, inherited from Entry, provide placeholder
  features

version 1.2.0:
  add SelectLabel, it combines several labels and each label like a option
  allowed user to select

version 1.3.0:
  add Flipbook, it can emulate the behavior of a flipbook or notebook.

'''
from Tkinter_template.Assets.project_management import making_widget
from Tkinter_template.Assets.image import tk_image
from Tkinter_template.Assets.font import font_get, measure
from tkinter import Button, Entry, Label
from typing import Iterable


class BindButton(Button):
    '''
        for keyboard holdon feature
        need focus on
        like use 'Return' for enter key
    '''

    def __init__(self, char, root=None, **option):
        super().__init__(root, **option)
        self.char = char  # using None for every key
        self.__bind()

    def __bind(self):
        def keypress(event):
            if (self.char is None) or (event.keysym == self.char):
                self.config(relief='sunken')

        def keyrelease(event):
            if (self.char is None) or (event.keysym == self.char):
                self.config(relief='raised')
                self.invoke()

        self.bind('<KeyPress>', keypress)
        self.bind('<KeyRelease>', keyrelease)


class EffectButton(Button):
    '''
        achieve hover feature
    '''

    def __init__(self, color: tuple, root=None, **option):
        '''
        color(first for bg, second for fg)
        '''
        super().__init__(root, **option)
        self.color = color
        self.__bg = self['bg']
        self.__fg = self['fg']
        self.__bind()

    def __bind(self):
        def enter(event):
            self.config(bg=self.color[0], fg=self.color[1])

        def leave(event):
            self.config(bg=self.__bg, fg=self.__fg)

        self.bind('<Enter>', enter)
        self.bind('<Leave>', leave)


class PlaceholderEntry(Entry):
    """
        Custom Entry widget with placeholder text.

        Args:
            placeholder (str): Placeholder text to display when entry is empty.
            color (str): Color of placeholder text (default is 'gray').
            root: Parent widget or window.
            **options: Additional options to configure the Entry widget.
    """

    def __init__(self, placeholder, color='gray', root=None, **option):
        super().__init__(root, **option)
        self.placeholder = placeholder
        self.color = color
        self.origin_color = self['fg']
        self.__origin()
        self.__bind()

    def __origin(self):
        self['fg'] = self.color
        self.insert(0, self.placeholder)

    def __bind(self):
        def focus_in(event):
            if self.get() == self.placeholder:
                self.delete(0, 'end')
                self['fg'] = self.origin_color

        def focus_out(event):
            if self.get() == '':
                self.__origin()

        self.bind("<FocusIn>", focus_in)
        self.bind("<FocusOut>", focus_out)


class SelectLabel:
    """
        Using several label and allowed user can select function by
        using keyboard arrow keys
    """
    cycle = False
    apperence = {"fg": 'indigo', "bg": 'coral', "relief": 'solid'}

    def __init__(self, text_list, func, canvas=None, **option):
        self.func = func
        self.canvas = canvas
        self.labels = [Label(self.canvas, text=text, **option)
                       for text in text_list]

    def show(self, coordinate: tuple, interval: int):
        def select(arg):
            nonlocal choice_number
            if arg == 'down':
                n = choice_number + 1
                if n == len(self.labels):
                    if self.__class__.cycle:
                        choice_number = 0
                    else:
                        return
                else:
                    choice_number = n
            elif arg == 'up':
                n = choice_number - 1
                if n == -1:
                    if self.__class__.cycle:
                        choice_number = len(self.labels)-1
                    else:
                        return
                else:
                    choice_number = n

            for i in range(0, len(self.labels)):
                if i == choice_number:
                    self.canvas.itemconfig(
                        f'arrow-{i}', state='normal')
                    self.labels[i].config(
                        **self.__class__.apperence)

                    # H
                    self.canvas.dtag(
                        self.canvas.find_withtag(f"arrow-{i}")[0], "H")

                else:
                    self.labels[i].config(
                        fg='black', bg=self.canvas["bg"], relief='flat')
                    self.canvas.itemconfig(
                        f'arrow-{i}', state='hidden')
                    # H
                    self.canvas.addtag_withtag(
                        "H", self.canvas.find_withtag(f"arrow-{i}")[0])

        def choice(event):

            self.func(
                self.labels[choice_number]['text']
            )

        # unbind all arrow and enter
        self.canvas.unbind("<Down>")
        self.canvas.unbind("<Return>")
        self.canvas.unbind("<Up>")
        choice_number = 0

        for number, obj in enumerate(self.labels):
            self.canvas.create_window(coordinate[0], coordinate[1]+interval*number, anchor='w',
                                      window=obj, tags=f'label-{number}')
            font_size = self.labels[0]["font"].split(" ")[1]

            self.canvas.create_image(coordinate[0]-25, coordinate[1]+interval*number, anchor='e',
                                     image=tk_image('play.png', int(font_size), dirpath='images\\selectlabel'), tags=(f'arrow-{number}', "H"),
                                     state='hidden')

        self.canvas.bind(
            '<Down>', lambda event, args='down': select(args))
        self.canvas.bind(
            '<Up>', lambda event, args='up': select(args))
        self.canvas.bind('<Return>', choice)

        # select uppest
        select('initial')


class Flipbook:
    """
        The Flipbook Widget is a custom widget designed to emulate the behavior of a flipbook or a multi-page notepad. 
        It allows users to write and view different messages on multiple pages, 
        making it a versatile tool for various applications such as note-taking, journaling, 
        or simply organizing information across several pages.
    """
    params = {
        "position": (0, 0),  # internal canvas in passing canvas position
        "bg": "#ff6b87",  # internal canvas bg
        # if False, the repeat click on page will not invoke func
        "repeat click allowed": False,
        "origin color": ("#FFFFAD", "black"),
        "active color": ("#FFAA1D", "black"),
        "default page": 0  # None for no default
    }

    def __init__(self, canvas, pages: Iterable[str], font_size: int, func, root=None) -> None:
        self.pages = pages
        self.fs = font_size
        self.func = func

        p = self.__class__.params
        self.__interval = self.fs/1.5

        self.__c = making_widget("Canvas")(root, width=measure("".join(pages), self.fs) + (len(pages)+1)*self.__interval,
                                           height=self.fs*2, bg=p["bg"])
        canvas.create_window(*p["position"], anchor="nw", window=self.__c)

        self.__build_pages()

        # default
        if p["default page"] is not None:
            self.__click(self.pages[p["default page"]])

    def __build_pages(self):
        sum = 0
        h = int(self.__c["height"])
        for text in self.pages:
            sum += self.__interval
            self.__c.create_rectangle(sum, h-self.fs,
                                      sum + measure(text, self.fs), h+self.fs,
                                      tags=(f"rec-{text}", f"{text}"), fill=self.__class__.params["origin color"][0],
                                      outline=self.__class__.params["origin color"][0])
            self.__c.create_text(sum, h-self.fs, text=text, font=font_get(self.fs),
                                 tags=(f"text-{text}", f"{text}"), anchor="nw", fill=self.__class__.params["origin color"][1])
            sum += measure(text, self.fs)

            self.__c.tag_bind(f"{text}", "<Button-1>",
                              lambda event, t=text: self.__click(t))
        self.__origin_height = self.__c.coords(f"rec-{self.pages[0]}")[1]

    def __click(self, text):
        repeat = True
        p = self.__class__.params
        for page in self.pages:
            h = self.__c.coords(f"rec-{page}")[1]
            if page == text:
                # correct label
                if h > self.__origin_height - self.fs*0.4 + 2:
                    self.__c.move(f"{page}", 0, -self.fs*0.4)
                    repeat = False
                self.__c.itemconfig(
                    f"rec-{page}", fill=p["active color"][0], outline=p["active color"][0])
                self.__c.itemconfig(f"text-{page}", fill=p["active color"][1])

            else:
                if h < self.__origin_height - self.fs*0.4 + 2:
                    self.__c.move(f"{page}", 0, self.fs*0.4)
                self.__c.itemconfig(
                    f"rec-{page}", fill=p["origin color"][0], outline=p["origin color"][0])
                self.__c.itemconfig(f"text-{page}", fill=p["origin color"][1])
        if (not p["repeat click allowed"]) and repeat:
            return
        self.func(text)
