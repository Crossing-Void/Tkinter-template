'''
@version: 2.0.0
@author: CrossingVoid
@date: 2024/06/30

The soundeffect.py is mainly for sound effects,
particularly a short sound for special use in project like tk game.

version 2.0.0:
  use class to warp all function together.
  add channel feature to make sound more precision
'''
import pygame
import os

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
pygame.mixer.init()
_search_path = ['sounds']


class Sound:
    channel = 1

    def __init__(self) -> None:
        self.__channel = {"default": pygame.mixer.Channel(1)}
        self.__soundeffects = {}
        self.refactor_soundeffects()

    def refactor_soundeffects(self):
        for path in _search_path:
            if os.path.exists(path):
                walker = os.walk(path)
                break
        else:
            return

        for now, _, filelist in walker:
            for filename in filelist:
                self.__soundeffects[
                    (
                        *now.split("\\")[1:], os.path.splitext(filename)[0]
                    )
                ] = pygame.mixer.Sound(os.path.join(now, filename))

    def add_channel(self, name: str):
        if name in self.__channel:
            return
        self.__class__.channel += 1
        self.__channel[name] = pygame.mixer.Channel(self.__class__.channel)

    def get_channels_name(self) -> tuple:
        return tuple(
            self.__channel.keys()
        )

    def play_sound(self, *paths, channel="default"):
        self.__channel[channel].play(self.__soundeffects[paths])

    def manipulate_channel(self, manipulate, *args, channel="default"):
        channel = self.__channel[channel]

        method = getattr(channel, manipulate)
        if not callable(method):
            raise ValueError(
                f"The method: {method} is not a method of channel")

        if args:
            return method(*args)
        else:
            return method()

    # play sound directly
    #
    #
    #
    #
    #
    #
    #
