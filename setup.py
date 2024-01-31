from setuptools import setup, find_packages

setup(
    name='ga4gh-cli',
    version=open('VERSION', 'r').read().strip(),
    packages=find_packages(),
    py_modules=['ga4gh_cli'], 
    entry_points={
        'console_scripts': [
            'ga4gh-cli=main:cli',
        ],
    },
    author='Pavel Nikonorov',
    author_email='info@genxt.network',
    description='Console interface for GA4GH-compliant environments',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)