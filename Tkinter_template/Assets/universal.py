'''
@version: 1.4.0
@author: CrossingVoid
@date: 2024/07/02

The universal.py is mainly for some goody function to save time
(mostly from previous project)

version 1.1.0:
  add new class MoveBg. it is like dynamic waterfall
  background

version 1.2.0:
  remove delete_extension function, using os.path.splitext instead

version 1.3.0:
  add more feature and function in class MoveBg:
  -- new text bg options
  -- fix some typos
  -- fix some issues

version 1.4.0:
  add new function check_valid_folder_name
'''
from Tkinter_template.Assets.project_management import effect_decorator
from Tkinter_template.Assets.image import tk_image
from Tkinter_template.Assets.font import font_get, measure
from dataclasses import dataclass
from typing_extensions import Iterable, Union
from datetime import date
import random
import json
import re
import os


def check_valid_folder_name(folder_name):
    return bool(re.match('^[^\\\\/:*?"<>|\r\n]+$', folder_name))


def str_tuple_date_change(arg):
    '''
    switch date tuple {(2022, 12, 12)}(includes datetime.date objs) and date string format {2022-12-12}
    '''
    if type(arg) == str:
        return (int(arg[:4]), int(arg[5:7]), int(arg[8:10]))
    elif type(arg) == tuple:
        return f'{arg[0]:04d}-{arg[1]:02d}-{arg[2]:02d}'
    elif type(arg) == date:
        return f'{arg.year:04d}-{arg.month:02d}-{arg.day:02d}'


def parse_json_to_property(app: object, json_file: str):
    '''
    support bool, int, float, str, list(max one layer)
    '''
    def category(value):
        '''
        only for zero layer object
        '''
        match value:
            case bool():
                return 'Boolean'
            case int():
                return 'Int'
            case float():
                return 'Double'
            case str():
                return 'String'
            case _:
                raise Exception('Parsing JSON error')

    def assign(name, value):
        app  # for exec app
        typename = category(value)
        if typename == 'String':
            exec(
                f'app.{name} = making_widget("{typename}Var")(app.root, value="{value}")'
            )
        else:
            exec(
                f'app.{name} = making_widget("{typename}Var")(app.root, value={value})'
            )

    with open(json_file) as f:
        settingDict = json.load(f)

    for key, value in settingDict.items():
        if type(value) == list:
            decoration = 0
            for sub_value in value:
                assign(f'{key}_{decoration}', sub_value)
                decoration += 1
        else:
            assign(key, value)


class MoveBg:
    '''
        A MoveBg obj only affects one canvas,
        if need to affect multiple canvas, build another Movebg object
    '''

    def __init__(self, canvas: object, canvas_side: tuple, rate: float, image_source_folder: Iterable[str] = ("images"), text_source_list: Iterable[str] = ()) -> None:
        self.c = canvas
        self.cs = canvas_side
        self.r = rate
        self.text_color = None

        # tuple (path, filename) for image or str "text" for text
        self.img_name = []
        self.__objs = []
        self.flush = None  # for bind effect decorator
        self.__gain_source_image(image_source_folder, text_source_list)
        self.__create_flush()

    def __gain_source_image(self, folders, texts):
        for folder in folders:
            for now, _, filelist in os.walk(folder):
                for filename in filelist:
                    if os.path.splitext(filename)[1].lower() in ('.png', '.tiff', '.jpg', '.ico', '.jpeg'):
                        self.img_name.append((now, filename))

        for char in texts:
            self.img_name.append(char)

    def __create_image_for_bg(self):
        for obj in self.__objs:
            if type(obj.img) == tuple:
                self.c.create_image(obj.x, obj.y, anchor='sw', tags=('moveBg'), image=tk_image(
                    obj.img[1], width=obj.size[0], dirpath=obj.img[0]
                ))
            else:
                self.c.create_text(obj.x, obj.y, anchor="sw", tags=("moveBg"), text=obj.img, font=font_get(obj.size[1]),
                                   fill=obj.color)

    def create_obj(self, number: int = 1):
        for _ in range(number):
            r = self.r

            img = random.choice(self.img_name)
            # width for image, height for text
            width = random.randint(int(self.cs[0]//(r+1)), int(self.cs[0]//r))
            if type(img) == tuple:
                height = tk_image(img[1], width=width,
                                  dirpath=img[0], get_image_size=True).height

            setting = {
                'x': random.randint(int(self.cs[0]//r), int(self.cs[0]-self.cs[0]//r)),
                'y': 0,
                'u': random.randint(-7, 7),
                'v': random.randint(3, 11),
                'size': (width, height) if type(img) == tuple else (measure(img, width), width),
                'img': img
            }

            obj = _BgObj(**setting)
            obj.color = (self.text_color if self.text_color else
                         f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
                         )
            self.__objs.append(
                obj
            )

    def __create_flush(self):
        # independent object of effect decorator
        @effect_decorator(0.05)
        def flush():
            self.c.delete('moveBg')
            self.__create_image_for_bg()
            try:
                self.c.tag_raise('moveBg', 'cover')
            except:
                try:
                    min = self.c.find_all()[0]
                    self.c.tag_lower('moveBg', min)
                except:
                    pass
            for obj in self.__objs:
                if obj.move(self.cs):
                    self.__objs.remove(obj)
                    self.create_obj()

        self.flush = flush


@dataclass
class _BgObj:
    x: int
    y: int
    u: int
    v: int
    size: tuple
    img: Union[tuple, str]

    def move(self, side):
        w, h = side
        self.x += self.u
        self.y += self.v
        if self.x < 0 or self.x > w-self.size[0]:
            self.u *= -1
        if self.y > h+self.size[1]:
            return True
