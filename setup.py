#!/usr/bin/env python

import os
import setuptools

from opendrift.version import __version__

setuptools.setup(
    name        = 'OpenDrift',
    description = 'OpenDrift - framework for ocean trajectory modeling',
    author      = 'Knut-Frode Dagestad / MET Norway',
    url         = 'https://github.com/OpenDrift/opendrift',
    download_url = 'https://github.com/OpenDrift/opendrift',
    version = __version__,
    license = 'GPLv2',
    install_requires = [
        'numpy',
        'scipy',
        'matplotlib',
        'netCDF4',
        'future',
        'configobj',
        'pillow',
        'pyproj',
        'cartopy',
        'rasterio',
        'opendrift-landmask-data',
        'oil-library'
    ],
    packages = setuptools.find_packages(),
    include_package_data = True,
    setup_requires = ['setuptools_scm', 'pytest-runner'],
    tests_require = ['pytest'],
    scripts = ['opendrift/scripts/hodograph.py',
               'opendrift/scripts/readerinfo.py',
               'opendrift/scripts/opendrift_plot.py',
               'opendrift/scripts/opendrift_animate.py',
               'opendrift/scripts/opendrift_gui.py']
)

