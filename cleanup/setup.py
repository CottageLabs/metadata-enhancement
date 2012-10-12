from setuptools import setup, find_packages

setup(
    name = 'cleanup',
    version = '0.1',
    packages = find_packages(),
    install_requires = [],
    url = 'http://cottagelabs.com/',
    author = 'Richard Jones, Emanuil Tolev, Cottage Labs',
    author_email = 'us@cottagelabs.com',
    description = 'Metadata Cleanup Tools',
    license = 'Copyheart',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: Copyheart',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
