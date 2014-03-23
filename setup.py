#!/usr/bin/env python

from distutils.core import setup

setup(
    name='django-qrauth',
    version='0.1.2',
    author='aruseni',
    author_email='aruseni.magiku@gmail.com',
    packages=['qrauth'],
    url='https://github.com/aruseni/django-qrauth',
    license='BSD licence, see LICENCE.md',
    description=('Nice QR codes that allow the users to instantly'
                 ' sign in to the website on their mobile devices'),
    long_description=open('README.md').read()[:-1],
    zip_safe=False,
    install_requires=['qrcode', 'redis', 'PIL'],
)
