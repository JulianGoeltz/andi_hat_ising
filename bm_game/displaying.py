#!python3
"""Display code oto visulize the game in pygame."""
import time
import pygame
import numpy as np
import os
from PIL import Image
from datetime import datetime
import digitalio
import busio
from board import SCK, MOSI, MISO, D24, D25, CE0
from adafruit_rgb_display import color565
import adafruit_rgb_display.ili9341 as ili9341


# set up the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# set up the hardware-dispaly related variables
CS_PIN = CE0
DC_PIN = D25
RST_PIN = D24
HW_SPI = busio.SPI(clock=SCK, MOSI=MOSI, MISO=MISO)
WIDTH = 240
HEIGHT = 320


class Display:

    """The display class in pygame

    Attributes:
        img_spindown: spin down image
        img_spinup: spin up image
        size_field: size of the gamefiled
        size_window: Size of the window to be shown
        win: handle to manipulate the display
    """

    # pylint: disable=C0103
    def __init__(self, x, y, pixel_per_spin):
        """standard display constructor

        Args:
            x (int): gamefield size x-axes
            y (int): gamefield size y-axes
        """
        if not os.path.exists("out"):
            os.makedirs('out')

        # hardware display
        self.hw_display = ili9341.ILI9341(
                                HW_SPI,
                                width=WIDTH,
                                height=HEIGHT,
                                baudrate=30000000,
                                cs=digitalio.DigitalInOut(CS_PIN),
                                dc=digitalio.DigitalInOut(DC_PIN),
                                rst=digitalio.DigitalInOut(RST_PIN))

        self.size_field = np.array([x, y])
        self.pixel_per_spin = pixel_per_spin
        self.size_window = 320, 240

        pygame.init()
        self.win = pygame.display.set_mode(list(self.size_window))
        pygame.display.set_caption("Ising spin field")
        self.font = pygame.font.SysFont(None, 24)

        self.set_up_level("", None)
        self.level_won = False
        self.level_new = False

        # Images
        self.images = [
            [
                pygame.transform.scale(pygame.image.load(
                    "images/spinup.png"), (self.pixel_per_spin, self.pixel_per_spin)),
                pygame.transform.scale(pygame.image.load(
                    "images/spindown.png"), (self.pixel_per_spin, self.pixel_per_spin)),
                pygame.transform.scale(pygame.image.load(
                    "images/questionmark.png"), (self.pixel_per_spin, self.pixel_per_spin)),
            ],
            [
                pygame.transform.scale(pygame.image.load(
                    "images/spinup_fix.png"), (self.pixel_per_spin, self.pixel_per_spin)),
                pygame.transform.scale(pygame.image.load(
                    "images/spindown_fix.png"), (self.pixel_per_spin, self.pixel_per_spin)),
            ],
        ]

    def update(self, state, forced):
        """Update the states on the sampled network

        Args:
            state: rectangular shaped states numpy array
        """
        if self.level_won:
            self.level_won = False
            self.win.fill(BLACK)
            self.win.blit(
                self.font.render("you won the level!", True, RED),
                (2 * self.pixel_per_spin, 4 * self.pixel_per_spin))
            pygame.display.update()
            time.sleep(2.0)

        if self.level_new:
            self.level_new = False
            self.win.fill(BLACK)
            self.win.blit(
                self.font.render("new level, new target", True, RED),
                (2 * self.pixel_per_spin, 4 * self.pixel_per_spin))
            self.update_target()
            pygame.display.update()
            time.sleep(2)

        self.win.fill(BLACK)
        self.update_field(state, forced)
        self.update_target()
        pygame.display.update()

        
        strFormat = 'RGB'
        raw_str = pygame.image.tostring(self.win, strFormat, False)
        image = Image.frombytes(strFormat, self.win.get_size(), raw_str)
        image = image.transpose(Image.ROTATE_90)
        self.hw_display.image(image)

    def update_field(self, state, forced):
        """update spin field part"""
        for x in range(self.size_field[0]):
            for y in range(self.size_field[1]):
                img = self.images[forced[x, y]][state[x, y]]
                self.win.blit(img, (x * self.pixel_per_spin,
                                    y * self.pixel_per_spin))

    def update_target(self):
        """update target and level number part"""
        offset_x = (self.size_field[0] + 1) * self.pixel_per_spin
        offset_y = self.pixel_per_spin
        self.win.blit(self.level_txt_rendered, (offset_x + 10, 5))

        if self.target is not None:
            for i in range(3):
                for j in range(3):
                    img = self.images[0][self.target[i, j]]
                    self.win.blit(img, (i * self.pixel_per_spin + offset_x,
                                        j * self.pixel_per_spin + offset_y))

            pygame.draw.rect(self.win, BLACK,
                             (*((self.size_field // 2 - 2) * self.pixel_per_spin),
                              3 * self.pixel_per_spin, 3 * self.pixel_per_spin,),
                             1)

    def set_up_level(self, level_txt, target):
        """at beginning of level save text and target"""
        self.level_txt = level_txt
        self.level_txt_rendered = self.font.render(level_txt, True, RED)
        self.target = target
        self.level_new = True

    def won_level(self):
        """keep record if level was won to display message"""
        self.level_won = True
