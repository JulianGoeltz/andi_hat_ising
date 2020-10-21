# Game for Andie's hat

Defense on 11th November 2020

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
```bash
pip install .
```
And run the tests to check if the installation has worked
```bash
nosetests
```

## Maintenance manual

### Contribution workflow

1. Identify a task to.
2. Make local branch to track the changes. Push the changes to a remote branch on GitHub.
3. For style-consistency use [pycodestyle](https://pypi.org/project/pycodestyle/) and for linting (e.g. detecting bugs and codesmells) use [pylint](http://pylint.pycqa.org/en/latest/).
4. If you think you are ready, make a pull request on GitHub. Github will automatically run the testing worlflows to detect bugs, check style and to run the tests.
5. If all is green merge the changes on Github and remove the branch you used for development.

### Testing

Testing is done with [nosetest](https://nose.readthedocs.io/en/latest/). For an example see the existing tests in the _tests_ folder.

### The display for the raspi

We use a tft touch-screen for the visualization:
|Type|[2.4inch SPI Module ILI9341 SKU](http://www.lcdwiki.com/2.4inch_SPI_Module_ILI9341_SKU:MSP2402)|
|Screen|TFT touch-screen|
|color|RGB 65K|
|Resolution|320Wx240H|