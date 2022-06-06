import ast
import re
import os

from setuptools import setup

PACKAGE_NAME = 'SOL4Py'

setup(
    # metadata
    name=PACKAGE_NAME,
    version="4.0.0",

    # options
    packages=["SOL4Py", "SOL4Py/crypto", "SOL4Py/generator", "SOL4Py/keras", "SOL4Py/mysql", 
              "SOL4Py/network", "SOL4Py/opencv", "SOL4Py/opengl", "SOL4Py/opengl2", 
              "SOL4Py/openglarb", "SOL4Py/torch"],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.8',
    install_requires=[],
    extras_require={
        'dev': [
            'pytest>=3',
            'coverage',
        ],
    },
    entry_points='''
        [console_scripts]
        {app}={pkg}.cli:main
    '''.format(app=PACKAGE_NAME.replace('_', '-'), pkg=PACKAGE_NAME),
)