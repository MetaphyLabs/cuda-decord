#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
from setuptools import setup, find_packages
from setuptools.command.install import install as _install

class InstallCommand(_install):
    def run(self):
        # Install system dependencies
        self.install_system_dependencies()
        
        # Install CUDA dependencies
        cuda_path = self.find_nvcc()
        self.set_cuda_environment_variable(cuda_path)

        # Build Decord
        subprocess.check_call(['git', 'clone', '--recursive', 'https://github.com/dmlc/decord'])
        os.chdir('decord')
        os.makedirs('build', exist_ok=True)
        os.chdir('build')
        
        subprocess.check_call(['cmake', '..', '-DUSE_CUDA=ON', '-DCMAKE_BUILD_TYPE=Release'])
        subprocess.check_call(['make'])
        
        # Install Decord Python Package
        os.chdir('../python')
        subprocess.check_call(['python3', 'setup.py', 'install', '--user'])

        _install.run(self)

    def install_system_dependencies(self):
        """Install system dependencies including software-properties-common."""
        try:
            if os.path.isfile('script.sh'):
                subprocess.check_call(['chmod', '+x', 'script.sh'])
                subprocess.check_call(['./script.sh'])
            else:
                print("script.sh not found.")
                raise FileNotFoundError("script.sh not found.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while installing system dependencies: {e}")
            raise
        except FileNotFoundError as e:
            print(e)
            raise

    def find_nvcc(self):
        """Find the nvcc compiler."""
        try:
            result = subprocess.run(['which', 'nvcc'], capture_output=True, text=True, check=True)
            nvcc_path = result.stdout.strip()
            if nvcc_path:
                return nvcc_path
        except subprocess.CalledProcessError:
            pass
        
        # If `which` didn't find `nvcc`, search common installation directories
        common_paths = ['/usr/local/cuda/bin/nvcc', '/usr/local/cuda/bin']
        for path in common_paths:
            if os.path.isfile(path):
                return path
        return None

    def set_cuda_environment_variable(self, nvcc_path):
        """Set the CUDACXX environment variable."""
        if nvcc_path:
            os.environ['CUDACXX'] = nvcc_path
            print(f"Set CUDACXX environment variable to: {nvcc_path}")
        else:
            print("Cannot set CUDACXX environment variable because nvcc was not found.")

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
