#!python3

import numpy as np
import pygame


WHITE = (255, 255, 255)
pixel_per_spin = 80


class Display:
    def __init__(self, x, y):
        self.size_field = np.array([x, y])
        self.size_window = pixel_per_spin * self.size_field + np.array([30, 0])

        pygame.init()
        self.win = pygame.display.set_mode(list(self.size_window))
        pygame.display.set_caption("Ising spin field")

        # Images
        self.img_spinup = pygame.transform.scale(pygame.image.load("images/spinup.png"), (pixel_per_spin, pixel_per_spin))
        self.img_spindown = pygame.transform.scale(pygame.image.load("images/spindown.png"), (pixel_per_spin, pixel_per_spin))

    def update(self, state):
        self.win.fill(WHITE)
        # draw spins
        for x in range(self.size_field[0]):
            for y in range(self.size_field[1]):
                img = self.img_spinup if state[x, y] else self.img_spindown
                self.win.blit(img, (x * pixel_per_spin - img.get_width(),
                                    y * pixel_per_spin - img.get_height()))

        # update display
        pygame.display.update()
