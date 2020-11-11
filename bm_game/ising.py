"""Class and support functions to simulate the ising model."""
import numpy as np
from scipy import special


def create_connection_matrix(size: int):
    """Create the connection matrix of the equal sided grid Ising model
       with periodic boundaries

    Args:
        size (int): one side of the Ising grid. It has to be an even number
    """
    assert size % 2 == 0, "works only for even numbers"
    weights = np.zeros((size**2, size**2))
    for row in range(size):
        for col in range(size):
            unit_index = row * size + col

            # neigbors in the row
            nr_left = (unit_index + size - 1) if \
                (col == 0) else (unit_index - 1)
            nr_right = (unit_index - size + 1) if \
                (col == size-1) else (unit_index + 1)

            # neighbors in the column
            nc_up = (unit_index + (size-1)*size) if \
                (row == 0) else (unit_index - size)
            nc_down = (unit_index - (size-1)*size) if \
                (row == (size-1)) else (unit_index + size)

            # set the connections to one
            weights[unit_index, [nr_left, nr_right, nc_up, nc_down]] = 1

    return weights


def get_reds_and_blacks(size: int):
    """get the indices of the red and black units

    Args:
        size (int): one side of the Ising grid. It has to be an even number

    Returns:
        reds: Indices of the reds
        blacks: Indices of the blacks
    """

    reds = []
    blacks = []
    for row in range(size):
        for col in range(size):
            unit_index = row * size + col
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

    def __init__(self, size: int, bias: float = 0,
                 conn_strength: float = 1, temp: float = 1):
        """Create the states and connection matrix of the Isin model

        Args:
            size (int): one side of the Ising grid. It has to be an even number
            bias (float): bias of the units (external field)
            conn_strength (float): strength of the connection betweent the
                                   units
            temp (float): temperature of the model
        """

        if not size % 2 == 0:
            raise ValueError(f"The side of the Ising grid must be an even \
                               number to allow red-black update. \
                               Received: {size}.")

        self.size = size
        self.bias = bias
        self.conn_strength = conn_strength
        self.temp = temp
        self.states = np.random.randint(0, 2, self.size**2)
        self.connection_matrix = create_connection_matrix(
            self.size) * self.conn_strength
        self.reds, self.blacks = get_reds_and_blacks(self.size)

    def update(self):
        """Make one update on the states
        """

        # First update the reds, that is the odd ones
        # pylint: disable=maybe-no-member
        energies = special.expit((np.dot(self.connection_matrix, self.states) +
                                  self.bias)/self.temp)
        rand = np.random.rand(self.size**2)
        self.states[self.reds] = (rand < energies)[self.reds]

        # First update the blacks
        # pylint: disable=maybe-no-member
        energies = special.expit((np.dot(self.connection_matrix, self.states) +
                                  self.bias)/self.temp)
        rand = np.random.rand(self.size**2)
        self.states[self.blacks] = (rand < energies)[self.blacks]

    def force_states(self, indices_2d, values_2d):
        """after update, set spins at given indices to given values"""
        self.states[indices_2d.flatten()] = values_2d.flatten()

    def get_states(self):
        """Report the states as a list
        """

        return self.states

    def get_rectangular_states(self):
        """Return the states as a rectangular grid
        """

        return np.reshape(self.states, (self.size, self.size))

    def get_magnetization(self):
        """Compute and return the mean magnetization of the state
        """

        return np.sum(self.states) / self.size**2
