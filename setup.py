#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
from setuptools import setup, Extension, find_packages
from setuptools.command.install import install as _install

class InstallCommand(_install):
    def run(self):
        # Build Decord
        subprocess.check_call(['git', 'clone', '--recursive', 'https://github.com/MetaphyLabs/cuda-decord'])
        os.chdir('decord')
        os.makedirs('build', exist_ok=True)
        os.chdir('build')
        subprocess.check_call(['cmake', '..', '-DUSE_CUDA=ON', '-DCMAKE_BUILD_TYPE=Release'])
        subprocess.check_call(['make'])
        
        # Install Decord Python Package
        os.chdir('../python')
        subprocess.check_call(['python3', 'setup.py', 'install', '--user'])

        _install.run(self)

setup(
    name='decord',
    version='0.1',
    description='Decord Video Loader',
    maintainer='Vivek Kornepalli',
    maintainer_email='vivek@metaphy.world',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.14.0',
        'setuptools>=42',
    ],
    url='https://github.com/MetaphyLabs/decord',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
    ],
    license='APACHE',
    cmdclass={
        'install': InstallCommand,
    },
)
