#!python3
"""Display code oto visulize the game in pygame."""
import numpy as np
import pygame


WHITE = (255, 255, 255)
PIXEL_PER_SPIN = 80


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
        self.size_window = PIXEL_PER_SPIN * self.size_field + np.array([30, 0])

        pygame.init()
        self.win = pygame.display.set_mode(list(self.size_window))
        pygame.display.set_caption("Ising spin field")

        # Images
        self.img_spinup = pygame.transform.scale(pygame.image.load(
            "images/spinup.png"), (PIXEL_PER_SPIN, PIXEL_PER_SPIN))
        self.img_spindown = pygame.transform.scale(pygame.image.load(
            "images/spindown.png"), (PIXEL_PER_SPIN, PIXEL_PER_SPIN))

    def update(self, state):
        """Update the states on the sampled network

        Args:
            state: rectangular shaped states numpy array
        """
        self.win.fill(WHITE)
        # draw spins
        for x in range(self.size_field[0]):
            for y in range(self.size_field[1]):
                img = self.img_spinup if state[x, y] else self.img_spindown
                self.win.blit(img, (x * PIXEL_PER_SPIN - img.get_width(),
                                    y * PIXEL_PER_SPIN - img.get_height()))

        # update display
        pygame.display.update()
