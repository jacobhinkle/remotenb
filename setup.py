
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = "remotenb",
    version = "0.1",
    author = "Monte Lunacek",
    author_email = "monte.lunacek@colorado.edu",
    description = ("Lanch remote ipython notebooks on JANUS"),
    license = "BSD",
    keywords = "IPython notebook supercomputer",
    url = "https://github.com/ResearchComputing/remotenb",
    packages=['remotenb'],
    long_description=open('README.md').read(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ]
)