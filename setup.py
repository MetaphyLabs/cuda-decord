#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
from setuptools import setup, find_packages
from setuptools.command.install import install as _install

class InstallCommand(_install):
    def run(self):
        # Install system dependencies
        subprocess.check_call([ 'add-apt-repository', 'ppa:jonathonf/ffmpeg-4'])
        subprocess.check_call([ 'apt-get', 'update'])
        subprocess.check_call(['apt-get', 'install', '-y', 'build-essential', 'python3-dev', 'python3-setuptools', 'make', 'cmake'])
        subprocess.check_call([ 'apt-get', 'install', '-y', 'ffmpeg', 'libavcodec-dev', 'libavfilter-dev', 'libavformat-dev', 'libavutil-dev'])

        # Build Decord
        subprocess.check_call(['git', 'clone', '--recursive', 'https://github.com/dmlc/decord'])
        os.chdir('decord')
        os.makedirs('build', exist_ok=True)
        os.chdir('build')
        
        subprocess.check_call(['cmake', '..', '-DUSE_CUDA=OFF', '-DCMAKE_BUILD_TYPE=Release'])
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
