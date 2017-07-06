from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


setup(
    name='fakemenot',

    version='0.0.1',

    description='A simple python package to check if a Tweet is genuine or not',

    # The project's main homepage.
    url='https://github.com/sachinkamath/fakemenot',

    # Author details
    author='Sachin S Kamath',
    author_email='me@sachinwrites.xyz',


    # What does your project relate to?
    keywords='twitter fake tweets',

    install_requires=['pytesseract', 'twittersearch']

)
