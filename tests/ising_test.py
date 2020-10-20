"""test functions for the Ising model and its functionalities."""
import numpy as np
from nose import tools
from bm_game import ising



def test_conn_matrix():
    """Only test if it runs."""

    ising.create_connection_matrix(10)

    assert True


def test_red_and_black():
    """ test the reds and blacks """
    reds, blacks = ising.get_reds_and_blacks(4)
    tools.assert_true(np.all(blacks == np.array([1, 3, 4, 6, 9, 11, 12, 14])))
    tools.assert_true(np.all(reds == np.array([0, 2, 5, 7, 8, 10, 13, 15])))


test_ising = ising.IsingModel(10)


def test_update():
    """Test if the update runs."""
    test_ising.update()


def test_get_states():
    """Getting the states."""
    states = test_ising.get_states()
    tools.assert_equal(states.shape, (10**2,))


def test_get_rectangular_states():
    """getting rectangular states."""
    states = test_ising.get_rectangular_states()
    tools.assert_equal(states.shape, (10, 10))


def test_get_magnetization():
    """Check if the magnetization makes sense."""
    magnetization = test_ising.get_magnetization()
    tools.assert_true(magnetization >= 0)
    tools.assert_true(magnetization <= 1)
