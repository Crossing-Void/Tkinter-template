from Tkinter_template.Assets.universal import *
from Tkinter_template.Assets.project_management import *
from Tkinter_template.base import Interface
from Tkinter_template.Assets.extend_widget import Flipbook
from Tkinter_template.Assets.default_menu import adjust_volume
from Tkinter_template.Assets.default_dashboard import BulletinBoard
from Tkinter_template.Assets.music import Music
from Tkinter_template.Assets.soundeffect import Sound
from Tkinter_template.Assets.font import change_font
import random
import time

Interface.rate = 0.8


class Main(Interface):
    def __init__(self, title: str, icon=None, default_menu=True):
        super().__init__(title, icon, default_menu)
        self.modify_height()

        # c = making_widget("Canvas")(
        #     self.dashboard, width=self.dashboard_side[0], height=self.dashboard_side[1], bg="gold")
        # c.grid()

        # self.M = MoveBg(self.canvas, self.canvas_side,
        #                 8, text_source_list="456")
        # self.M.text_color = None
        # self.M2 = MoveBg(c, self.dashboard_side, 3, text_source_list="123")
        # self.M2.text_color = "violet"
        # self.M.create_obj(5)
        # self.M2.create_obj(10)

        # self.canvas['scrollregion'] = (
        #     0, 0, self.canvas_side[0],
        #     self.canvas_side[1]*1.5
        # )
        # self.canvas.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(-(event.delta//120), 'units')
        #                  )
        # self.canvas.create_line(
        #     0, self.canvas_side[1], self.canvas_side[0], self.canvas_side[1], width=3)
        # Flipbook.params["repeat click allowed"] = True
        # Flipbook.params["default page"] = None
        # f = Flipbook(self.canvas, ("碩", "博", "print",
        #              "ddf0", "我是誰"), 120, print)

        self.Music = Music()
        self.Sound = Sound()
        self.Sound.add_channel("f")
        self.top_menu.add_command(
            label="Testing Progressbar", command=lambda: self.sleep(self))

        post_menu(self.canvas, "<Button-1>", self.top_menu)

        self.B = BulletinBoard(self.dashboard, 500)
        self.B.paste_message_in_mutiple_line(
            "Download your favouritedt Nintendo Switch ROMs in NSP and XCI formats for Console and Emulators such as Suyu, Ryujinx,", 18, wrap="Word")
        self.sleep.add_arg(
            {"total": 5}, **self.B.get_progress_bar_arguments())

    @progress_bar(False, False)
    def sleep(self):
        for i in range(5):
            time.sleep(3)
            self.sleep.compelete_part(i+1)


if __name__ == "__main__":
    main = Main("Testing", "favicon.ico", False)

    while True:
        try:
            main.canvas.update()
            main.canvas.winfo_exists()
            time.sleep(0.01)
            # main.M.flush()
            # main.M2.flush()

        except:
            1 / 0
            break
