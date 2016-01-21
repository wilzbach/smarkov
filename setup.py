#!/usr/bin/env python3

from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))
readme = path.join(here, 'README.md')

try:
    import pypandoc
    long_description = pypandoc.convert(readme, 'rst')
except (IOError, ImportError):
    with open(readme, encoding='utf-8') as f:
        long_description = f.read()

setup(name='smarkov',
      version='1.0',
      description='Simple Markov and HMM',
      long_description=long_description,
      author='greenify',
      author_email='greenify@gmail.com',
      license='MIT',
      url='https://github.com/greenify/smarkov',
      package_dir={'smarkov': 'smarkov'},
      packages=['smarkov'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
      ],
      keywords='hmm markov'
      )
