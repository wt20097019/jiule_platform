# coding=utf8

import re
from setuptools import setup, find_packages
from pathlib import Path


def retrieve_version():
    p = Path('django_echarts', '__init__.py')
    with p.open(encoding='utf8') as f:
        version_file_content = f.read()
        version_match = re.findall(r"__version__\s=\s'([\d.]+)'", version_file_content)
        if version_match:
            return version_match[0]
        return RuntimeError("No version retrieved in package file.")


lib_classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Framework :: Django",
    "Framework :: Django :: 1.11",
    "Framework :: Django :: 2.0",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
    'Operating System :: OS Independent'
]

setup(
    name='django-echarts',
    version=retrieve_version(),
    packages=find_packages(exclude=['tests']),
    url='https://github.com/kinegratii/django-echarts',
    install_requires=['Django'],
    include_package_data=True,
    license='MIT',
    author='Kinegratii',
    author_email='kinegratii@gmail.com',
    description='A django app for Echarts integration with pyecharts as chart builder. ',
    classifiers=lib_classifiers
)
