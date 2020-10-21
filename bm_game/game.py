#!python3
"""actual game that includes the levels and winning conditions"""

import sys
import time
import numpy as np

import displaying
import ising


class Game:
    """this is where the magic happens: lvl control and general procedure"""
    def __init__(self, size):
        self.size = size
        self.levels = [
            [(1, 1, 0), ],
            [(1, 1, 1), ],
            [(0, 1, 0), (1, 1, 0), (2, 1, 0), ],
            [(1, 0, 1), (1, 1, 1), (1, 2, 1), ],
        ]
        self.level_no = 0

        self.display = displaying.Display(size, size)
        self.ising = ising.IsingModel(size, bias=-2.)

        # resetting and first display
        self.reset_field()
        self.set_up_level()
        self.force_spins()
        states = self.ising.get_rectangular_states()
        self.display.update(states, forced=(self.forced_spins > -1))

    def check_win(self):
        """determine whether target satisfied, if so upgrade lvl"""
        to_check = self.ising.get_rectangular_states()[self.size // 2 - 2:, self.size // 2 - 2:]
        to_check = to_check[:3, :3]
        # print(self.ising.get_rectangular_states())
        # print(to_check)
        # time.sleep(400)
        winning = np.all(to_check[self.target > -1] == self.target[self.target > -1])
        if not winning:
            return
        self.level_no += 1
        if self.level_no == len(self.levels):
            print("YOU BESTED THE GAME, no more levels. congrats")
            sys.exit()
        self.set_up_level()
        self.display.won_level()

    def reset_field(self):
        """unforce spins"""
        self.forced_spins = np.full((self.size, self.size), -1)

    def set_up_level(self):
        """seek out new target, reset"""
        self.reset_field()
        self.target = np.full((3, 3), -1)
        for tgt in self.levels[self.level_no]:
            self.target[tgt[:2]] = tgt[2]
        self.display.set_up_level(
            f"lvl {self.level_no}/{len(self.levels) - 1}", self.target)

    def force_spins(self):
        """forces set spins to corresponding value"""
        self.ising.force_states(self.forced_spins == 0,
                                np.full((self.forced_spins == 0).sum(), 0))
        self.ising.force_states(self.forced_spins == 1,
                                np.full((self.forced_spins == 1).sum(), 1))

    def run(self):
        """general procedure"""
        print("Starting the game")
        iteration = 0
        while True:
            iteration += 1
            # print(f"start of loop {iteration}")

            self.ising.update()
            self.force_spins()
            states = self.ising.get_rectangular_states()
            self.display.update(states, forced=(self.forced_spins > -1))
            self.check_win()

            time.sleep(1)

            if iteration == 1000:
                sys.exit()
