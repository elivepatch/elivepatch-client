from setuptools import setup, find_packages

setup(
    name='elivepatch-client',
    version='0.1',
    description='Distributed live patch client and automatic kernel live patch for kernel CVE',
    url='https://wiki.gentoo.org/wiki/Elivepatch, ' +\
        'https://github.com/aliceinwire/elivepatch-client',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: System :: Operating System Kernels',
    ],

    author='Alice Ferrazzi',
    author_email='alice.ferrazzi@gmail.com',
    license='GNU GPLv2+',
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["GitPython", "requests"],
    entry_points={"console_scripts": ["elivepatch-client = elivepatch_client.__main__:main"]},
)
