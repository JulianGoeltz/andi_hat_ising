#!/python3
"""define settings and instantiate game"""

import game


N = 8


if __name__ == '__main__':
    gm = game.Game(N)

    gm.run()
