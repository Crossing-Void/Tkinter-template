'''
@version: 2.2.0
@author: CrossingVoid
@date: 2024/07/04

The font.py is mainly for font manipulations

version 1.1.0:
  add function check font, checking _font_family is in 
  your computer font or not
  add function set font, useing windows os to show font install window
  make user install font

version 2.1.0:
  add alternate font family in _font_family,
  parse font from index 0 to last. useing font
  as long as it is on your PC's font

  modify check_font function, add one arguments
  modify change_font function 
  modify font_get function
  rename some variable

version 2.2.0:
  add new function delete_font_set, set the _using_font variable to None
  make function font_get to parse fonts again

'''

from tkinter.font import Font
import tkinter.font as font
import os


_alternate_fonts = ("UD Digi Kyokasho NP-R",
                    "Inconsolata",
                    "Castellar"
                    )
_font_file_location = os.path.join("data", "fonts_install")

_using_font = None  # currently use


def check_font(font_):
    if font_ in font.families():
        return True


def set_font():
    # hasn't been tested on platforms other than windows
    os.system(os.path.join(_font_file_location, f"{_alternate_fonts[0]}.ttf"))


def change_font(font_: str):
    global _using_font
    if not check_font(font_):
        print(f"Warning: {font_} is not found on your computer.\nContinue using the font: {_using_font}."
              )
        return
    _using_font = font_


def delete_font_set():
    global _using_font
    _using_font = None


def font_get(size, bold=False):
    """
    can be used to get _using_font
    """
    global _using_font
    if _using_font is None:
        # write _using_font
        for font_ in _alternate_fonts:
            if check_font(font_):
                _using_font = font_
                break
    return (_using_font, size, 'bold' if bold else '')


def font_span(text, fit_size, *, upper_bound=1000):
    '''
    Giving a width and text, generate exact font size.
    '''

    size = 1
    while True:
        if size >= upper_bound:
            return upper_bound
        if Font(font=font_get(size)).measure(text) > fit_size:
            break
        size += 1
    return size - 1


def measure(text, size):
    return Font(font=font_get(size)).measure(text)
