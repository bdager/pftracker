from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding


# Get the long description from the relevant file
#with open("README.rst", "r", encoding='utf-8') as fh:
#with open("README.rst", "r") as fh:
#    long_description = fh.read()

with open('README.md') as f:
    long_description = f.read()


setup(
    name="pftracker",  
   
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # http://packaging.python.org/en/latest/tutorial.html#version
    version="0.0.1",

    description="Face tracking based on particle filter",
    long_description=long_description,
#    long_description_content_type="text/x-rst",
    long_description_content_type="text/markdown",

    # The project's main homepage.
    url='https://github.com/bdager/pftracker',

    # Author details
    author="Bessie Domínguez-Dáger",
    author_email="bessie.dominguez97@gmail.com",

    # Choose your license
#    license="GPLv3",

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Utilities',


        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        
        'Operating System :: Microsoft :: Windows',
#        'Operating System :: POSIX',
#        'Operating System :: Unix',
#        'Operating System :: MacOS'
    ],

    # What does your project relate to?
    keywords=['Face tracking', 'particle filter'],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    package_dir={"": "pftracker"},
    packages=find_packages(where="pftracker"),
#    python_requires="==3.6",

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/discussions/install-requires-vs-requirements/
#    install_requires=['numpy', 'matplotlib', 'opencv', 'imutils', 'dlib',
#                      'pyqt5', 'skimage', 'os', 'ctypes', 'time', 'filterpy'],

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        'pftracker': ['README.md', 'LICENSE'],
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages.
    # see http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    #data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    #entry_points={
    #    'console_scripts': [
    #        'sample=sample:main',
    #    ],
    #},
)
