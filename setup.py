# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in hr_customizations/__init__.py
from hr_customizations import __version__ as version

setup(
	name='hr_customizations',
	version=version,
	description='Attendance Request changes',
	author='STS',
	author_email='rajat@example.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
