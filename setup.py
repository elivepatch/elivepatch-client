from setuptools import setup, find_packages

setup(
    name='elivepatch-client',
    version='0.01',
    description='Distributed live patch client and automatic kernel live patch for kernel CVE',
    url='https://wiki.gentoo.org/wiki/User:Aliceinwire/elivepatch, ' +\
        'https://github.com/aliceinwire/elivepatch-client',
    author='Alice Ferrazzi',
    author_email='alice.ferrazzi@gmail.com',
    license='GNU GPLv2+',
    packages=find_packages(),
    scripts=['bin/elivepatch'],
)
