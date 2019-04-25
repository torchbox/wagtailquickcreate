
#!/usr/bin/env python
"""
Installs the Wagtail Quick Create plugin which offers shortcut links on the admin
home screen to create defined pages under parent pages.
"""

from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='wagtail-quick-create',
      version='1.0.4',
      description='Offer links to the admin user to create content under sections quickly.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/kevinhowbrook/wagtailquickcreate',
      author='Kevin Howbrook - Torchbox',
      author_email='kevin.howbrook@torchbox.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'wagtail>=2.0',
      ])
