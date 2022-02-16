#!/usr/bin/env python

from distutils.core import setup
import os

thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + "/requirements.txt"
install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setup(
    name="eflm_meta_calculations",
    version="1.0",
    description="Web scraper for the EFLM biological variation database",
    author="William van Doorn",
    author_email="wptmdoorn@gmail.com",
    url="https://github.com/wptmdoorn/eflm_bv_calculations",
    packages=install_requires,
)
