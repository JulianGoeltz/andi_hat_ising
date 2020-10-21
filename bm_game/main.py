#!/python3
import sys
import time

import displaying
import ising


# X, Y = 20, 10
N = 10


display = displaying.Display(N, N)
Ising = ising.IsingModel(N, bias=0.)


if __name__ == '__main__':
    print("Starting main loop")
    iteration = 0
    while True:
        iteration += 1
        print(f"start of loop {iteration}")
        states = Ising.get_rectangular_states()
        display.update(states)
        Ising.update()
        time.sleep(1)

        if iteration == 10:
            sys.exit()
