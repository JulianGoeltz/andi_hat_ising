#!/python3
"""define settings and instantiate game"""

import game


N = 8
PIXEL_PER_SPIN = 25


if __name__ == '__main__':
    gm = game.Game(N, PIXEL_PER_SPIN)

    gm.run()
