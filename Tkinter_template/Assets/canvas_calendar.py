'''
@version: 1.0.0
@author: CrossingVoid
@date: 2024/07/02

The canvas_calendar.py is mainly for calendar function but can
draw on a canvas

'''
from Tkinter_template.Assets.font import font_get, font_span
import datetime
import calendar


class CanvasCalendar(calendar.Calendar):
    parameter = {
        "border width": 3,
        "skeleton": True,
        "zero rectangle": False,
        "fill": "white",
        "active fill": None,
        "holiday fill": "red",  # can change to outline
        "outline": "black",
        "day number position": (2, 0),  # can None
        "day number rate": 3,
        "day number size": "auto",
        "bind function": {},
        "default header": True,
        "header list": ("一", "二", "三", "四", "五", "六", "日"),
        "default name": True,
        "today highlight": ("red", None),
        "future hint": True
    }

    def __init__(self, canvas, first=0):
        self.canvas = canvas
        super().__init__(first)

        t = datetime.date.today()
        self.today = f"{t.year}-{t.month:02d}-{t.day:02d}"
        self.set_date(t.year, t.month)

    def get_date(self):
        return (self.year, self.month)

    def set_date(self, year, month):
        if (year not in range(datetime.MINYEAR, datetime.MAXYEAR+1)) or (month not in range(1, 13)):
            raise ValueError("datetime format not valid")
        self.year = year
        self.month = month

    @classmethod
    def get_parameter(cls):
        return cls.parameter

    @classmethod
    def set_parameter(cls, parameter, **kwarg):
        if (t := type(parameter)) != dict:
            raise ValueError(f"parameter must be a dict, but got {t}")
        parameter.update(kwarg)
        for key in parameter:
            if key not in cls.parameter:
                raise ValueError(f"The key: {key} does not support modified")
        cls.parameter.update(parameter)

    def __default_header(self, start_point, real_w):
        header = dict(
            zip(range(7), self.parameter['header list'])
        )
        x, y = start_point
        b = self.parameter['border width'] - 1
        font_size = int(real_w / 2.5)
        header_number = list(range(7))
        first = self.getfirstweekday()
        header_number = header_number[first:] + header_number[0:first]
        header_number = list(map(lambda x: header[x], header_number))

        for i in range(7):
            char = header_number[i]
            self.canvas.create_text(
                x + b + (2*i+1)*(b/2) + real_w*(i+0.5),
                y, font=font_get(font_size), text=char,
                fill=self.parameter['holiday fill'] if char in self.parameter['header list'][-2:] else self.parameter['outline'], anchor="s",
                tags=("calendar", f"calendar-header",
                      f"calendar-header-{char}")
            )

    def __default_name(self, start_point, real_w, real_h, week_number):
        x, y = start_point
        b = self.parameter['border width'] - 1
        font_size = int(font_span("2000年01月", 2*real_w, upper_bound=real_h))
        x1 = x + b +\
            (2*3+1)*(b/2) + \
            real_w*3.5
        y1 = y + b +\
            (2*week_number)*(b/2) + \
            real_h*week_number
        self.canvas.create_text(
            x1, y1+10, font=font_get(font_size),
            text=f"{self.year}年{self.month}月",
            fill=self.parameter['outline'], anchor="n",
            tags=("calendar", f"calendar-header")
        )

    def calerdar_to_canvas(self, start_point, size):
        def rec(date):
            self.canvas.create_rectangle(
                x1, y1, x2, y2, width=b+1, outline=self.parameter['outline'], fill=self.parameter['fill'],
                tags=(f"calendar", f"calendar-{date}")
            )
            if date[-2:] == "00":
                return
            if (self.parameter['future hint']) and (date > self.today):
                self.canvas.create_line(
                    x1, y1, x2, y2, width=b+1, fill=self.parameter['outline'],
                    tags=(f"calendar", f"calendar-{date}")
                )
                return
            color = self.parameter['active fill']
            if color:
                self.canvas.itemconfig(f"calendar-{date}", activefill=color)

        def bind(date):
            if (self.parameter['future hint'] == False) or (date <= self.today):
                for func_type, func in self.parameter['bind function'].items():
                    if func is None:
                        continue
                    self.canvas.tag_bind(f"calendar-{date}", func_type,
                                         lambda e, a=f"calendar-{date}", f=func: f(a))

        def number():
            p = self.parameter['day number position']
            r = self.parameter['day number rate']
            s = self.parameter['day number size']
            if p is None:
                return
            for rate in p:
                if rate not in range(r):
                    raise ValueError(
                        f"Day number position need in 0 ~ {self.parameter['day number rate']}"
                    )

            font_size = font_span(
                "00", (x2-x1)/r/1.5, upper_bound=(y2-y1)/r/1.5) if s == "auto" else s

            self.canvas.create_text(
                x1+(2*p[0]+1) * ((x2-x1)/r/2),
                y1+(2*p[1]+1) * ((y2-y1)/r/2),
                text=str(day), font=font_get(font_size),
                fill=self.parameter['holiday fill'] if self.getfirstweekday(
                )+day_in_week in [5, 6, 12] else self.parameter['outline'],
                tags=("calendar")
            )

        def outline():
            if self.parameter['skeleton']:
                self.canvas.create_rectangle(
                    x+b/2, y+b/2, x + b +
                    (2*6+1)*(b/2) +
                    real_w*6+b+real_w, y2+b, width=b+1, outline=self.parameter['outline'],
                    tags=("calendar"))

        # variables
        x, y = start_point
        w, h = size
        b = self.parameter['border width'] - 1
        real_w = (w - 9*b) // 7
        real_h = (h - 8*b) // 6
        month = self.monthdayscalendar(self.year, self.month)
        # variables

        week_in_month = 0
        for week in month:
            day_in_week = 0
            for day in week:
                date = f"{self.year}-{self.month:02d}-{day:02d}"
                if (day == 0) and not (self.parameter['zero rectangle']):
                    day_in_week += 1
                    continue
                # -----------------
                x1 = x + b +\
                    (2*day_in_week+1)*(b/2) + \
                    real_w*day_in_week
                x2 = x1 + real_w
                y1 = y + b +\
                    (2*week_in_month+1)*(b/2) + \
                    real_h*week_in_month
                y2 = y1 + real_h
                # -----------------
                rec(date)
                if day == 0:
                    day_in_week += 1
                    continue
                bind(date)
                number()
                day_in_week += 1
            week_in_month += 1

        outline()
        if self.parameter['default header']:
            self.__default_header(start_point, real_w)
        if self.parameter['default name']:
            self.__default_name(start_point, real_w, real_h, len(month))
        if self.parameter['today highlight']:
            outline_color, fill_color = self.parameter['today highlight']
            if outline_color:
                self.canvas.itemconfig(
                    f"calendar-{self.today}", outline=outline_color)
            if fill_color:
                self.canvas.itemconfig(
                    f"calendar-{self.today}", fill=fill_color)

    def clear(self):
        self.canvas.delete("calendar")
