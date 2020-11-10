#!/usr/bin/env python
"""
  Setup for pip install using setuptools
"""

from setuptools import setup
import bm_game


setup(name='bm_game',
      version=bm_game.__version__,
      description='',
      author='Akos F. Kungl, Julian Göltz',
      author_email='fkungl@kip.uni-heidelberg.de',
      url='https://github.com/JulianGoeltz/andi_hat_ising',
      packages=["bm_game"],
      package_dir={
          "bm_game": "bm_game",
      },
      license="GNUv3",
      install_requires=["numpy"],
      package_data={"bm_game": ["bm_game/images"]},
      include_package_data=True
      )
