
#!/usr/bin/env python
"""
Installs the Wagtail Quick Create plugin which offers shortcut links on the admin
home screen to create defined pages under parent pages.
"""

from setuptools import setup, find_packages

setup(name='wagtail-quick-create',
      version='1.0.0',
      description='Offer links to the admin user to create content under sections quickly.',
      long_description='Offer links to the admin user to create content under sections quickly.',
      url='https://github.com/kevinhowbrook/wagtailquickcreate',
      author='Kevin Howbrook - Torchbox',
      author_email='kevin.howbrook@torchbox.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'wagtail>=2.0',
      ])