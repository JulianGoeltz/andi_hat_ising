"""Class and support functions to simulate the ising model."""
import numpy as np
from scipy import special


def create_connection_matrix(n: int):
    """Create the connection matrix of the equal sided grid Ising model
       with periodic boundaries

    Args:
        n (int): one side of the Ising grid. It has to be an even number
    """

    w = np.zeros((n**2, n**2))
    for row in range(n):
        for col in range(n):
            unit_index = row * n + col

            # neigbors in the row
            nr_left = (unit_index + n - 1) if (col == 0) else (unit_index - 1)
            nr_right = (unit_index - n + 1) if (col ==
                                                n-1) else (unit_index + 1)

            # neighbors in the column
            nc_up = (unit_index + (n-1)*n) if (row == 0) else (unit_index - n)
            nc_down = (unit_index - (n-1)*n) if (row ==
                                                 (n-1)) else (unit_index + n)

            # set the connections to one
            w[unit_index, [nr_left, nr_right, nc_up, nc_down]] = 1

    return w


def get_reds_and_blacks(n: int):
    """get the indices of the red and black units

    Args:
        n (int): one side of the Ising grid. It has to be an even number

    Returns:
        reds: Indices of the reds
        blacks: Indices of the blacks
    """

    reds = []
    blacks = []
    for row in range(n):
        for col in range(n):
            unit_index = row * n + col
            if (row + col) % 2 == 0:
                reds.append(unit_index)
            else:
                blacks.append(unit_index)

    return np.array(reds), np.array(blacks)


class IsingModel:
    """docstring for IsingModel
       ising model handler that gives access to updating and the states
       and getting states about the model.
       The model uses periodic boundary conditions and uses the red-black
       update procedure.
       Imagine the red-black coding as
                r b r b r b
                b r b r b r
                r b r b r b
                b r b r b r
                r b r b r b
                b r b r b r
    """

    def __init__(self, n: int, bias: float = 0,
                 conn_strength: float = 1, temp: float = 1):
        """Create the states and connection matrix of the Isin model

        Args:
            n (int): one side of the Ising grid. It has to be an even number
            bias (float): bias of the units (external field)
            conn_strength (float): strength of the connection betweent the
                                   units
            temp (float): temperature of the model
        """

        if not n % 2 == 0:
            raise ValueError(f"The side of the Ising grid must be an even \
                               number to allow red-black update. \
                               Received: {n}.")

        self.n = n
        self.bias = bias
        self.conn_strength = conn_strength
        self.temp = temp
        self.states = np.random.randint(0, 2, self.n**2)
        self.connection_matrix = create_connection_matrix(
            self.n) * self.conn_strength
        self.reds, self.blacks = get_reds_and_blacks(self.n)

    def update(self):
        """Make one update on the states
        """

        # First update the reds, that is the odd ones
        energies = special.expit((np.dot(self.connection_matrix, self.states) +
                                  self.bias)/self.temp)
        rand = np.random.rand(self.n**2)
        self.states[self.reds] = (rand < energies)[self.reds]

        # First update the blacks
        energies = special.expit((np.dot(self.connection_matrix, self.states) +
                                  self.bias)/self.temp)
        rand = np.random.rand(self.n**2)
        self.states[self.blacks] = (rand < energies)[self.blacks]

    def get_states(self):
        """Report the states as a list
        """

        return self.states

    def get_rectangular_states(self):
        """Return the states as a rectangular grid
        """

        return np.reshape(self.states, (self.n, self.n))

    def get_magnetization(self):
        """Compute and return the mean magnetization of the state
        """

        return np.sum(self.states) / self.n**2
