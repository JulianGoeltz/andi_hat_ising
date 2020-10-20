Idea for ISING class:

```
class ISING:
    get_state():
    update():
    set_params(temperature, field, connection_strength):
    get_params():
```
Idea of game:
 * lvling up is possible
 * goal is to reproduce given spin combination in the centre
 * starts with task to align one spin, first up then down,
 then 2, and so on
 * this makes for increasing complexity

## Worklflow Badges
![Python test](https://github.com/JulianGoeltz/andi_hat_ising/workflows/Python%20tests/badge.svg)
![Python codestyle](https://github.com/JulianGoeltz/andi_hat_ising/workflows/Python%20codestyle/badge.svg)

## Getting started
Install the packages with pip
´´´bash
pip install .
´´´
And run the tests to check if the installation has worked
´´´bash
nosetests
´´´
