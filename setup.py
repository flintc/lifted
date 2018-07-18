from __future__ import print_function
from setuptools import setup, find_packages
#from setuptools.command.test import test as TestCommand
import io
import os
import sys

import lifted

#here = os.path.abspath(os.path.dirname(__file__))

# def read(*filenames, **kwargs):
#     encoding = kwargs.get('encoding', 'utf-8')
#     sep = kwargs.get('sep', '\n')
#     buf = []
#     for filename in filenames:
#         with io.open(filename, encoding=encoding) as f:
#             buf.append(f.read())
#     return sep.join(buf)

# long_description = read('README.txt', 'CHANGES.txt')

# class PyTest(TestCommand):
#     def finalize_options(self):
#         TestCommand.finalize_options(self)
#         self.test_args = []
#         self.test_suite = True

#     def run_tests(self):
#         import pytest
#         errcode = pytest.main(self.test_args)
#         sys.exit(errcode)

setup(
    name='lifted',
    version='0.0.1',
    url='https://github.com/flintc/lifted/',
    license='MIT',
    author='C Flint',
    author_email='flintc27@gmail.com',
    description='Abtraction of processing workflows, decision logic, logging, error-handling etc in a more functional way.',
    packages=['lifted'],
    include_package_data=True,
    platforms='any',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent'
        ]
)