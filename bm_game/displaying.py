#!python3
"""Display code oto visulize the game in pygame."""
import time
import pygame
import numpy as np


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PIXEL_PER_SPIN = 25


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
    def __init__(self, x, y):
        """standard display constructor

        Args:
            x (int): gamefield size x-axes
            y (int): gamefield size y-axes
        """
        self.size_field = np.array([x, y])
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
                    "images/spinup.png"), (PIXEL_PER_SPIN, PIXEL_PER_SPIN)),
                pygame.transform.scale(pygame.image.load(
                    "images/spindown.png"), (PIXEL_PER_SPIN, PIXEL_PER_SPIN)),
                pygame.transform.scale(pygame.image.load(
                    "images/questionmark.png"), (PIXEL_PER_SPIN, PIXEL_PER_SPIN)),
            ],
            [
                pygame.transform.scale(pygame.image.load(
                    "images/spinup_fix.png"), (PIXEL_PER_SPIN, PIXEL_PER_SPIN)),
                pygame.transform.scale(pygame.image.load(
                    "images/spindown_fix.png"), (PIXEL_PER_SPIN, PIXEL_PER_SPIN)),
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
                self.font.render("YOU WON THE LEVEL!", True, RED),
                (2 * PIXEL_PER_SPIN, 4 * PIXEL_PER_SPIN))
            pygame.display.update()
            time.sleep(2.0)

        if self.level_new:
            self.level_new = False
            self.win.fill(BLACK)
            self.win.blit(
                self.font.render("new level, new target", True, RED),
                (2 * PIXEL_PER_SPIN, 4 * PIXEL_PER_SPIN))
            self.update_target()
            pygame.display.update()
            time.sleep(2)

        self.win.fill(BLACK)
        self.update_field(state, forced)
        self.update_target()
        pygame.display.update()

    def update_field(self, state, forced):
        """update spin field part"""
        for x in range(self.size_field[0]):
            for y in range(self.size_field[1]):
                img = self.images[forced[x, y]][state[x, y]]
                self.win.blit(img, (x * PIXEL_PER_SPIN,
                                    y * PIXEL_PER_SPIN))

    def update_target(self):
        """update target and level number part"""
        offset_x = (self.size_field[0] + 1) * PIXEL_PER_SPIN
        offset_y = PIXEL_PER_SPIN
        self.win.blit(self.level_txt_rendered, (offset_x + 10, 5))

        if self.target is not None:
            for i in range(3):
                for j in range(3):
                    img = self.images[0][self.target[i, j]]
                    self.win.blit(img, (i * PIXEL_PER_SPIN + offset_x,
                                        j * PIXEL_PER_SPIN + offset_y))

            pygame.draw.rect(self.win, BLACK,
                             (*((self.size_field // 2 - 2) * PIXEL_PER_SPIN),
                              3 * PIXEL_PER_SPIN, 3 * PIXEL_PER_SPIN,),
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
