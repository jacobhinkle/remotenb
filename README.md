Remote IPython Notebook
===============

The `remotenb` package lanuches an ipython notebook on the JANUS supercomputer.

- **Linux** and **OSX only**
- Author: Monte Lunacek <monte.lunacek@colorado.edu>

This package will launch a PBS job and a remote **IPython notebook** on the JANUS supercomputer. The package is installed locally and nothing needs to be setup on the remote connection.  Instead, *remotenb* uses the [*paramiko*](http://www.lag.net/paramiko/) to move files and execute commands.


Installation
------------
Requirements:

- [jinja2](http://jinja.pocoo.org/docs/) 2.7.1
- [paramiko](http://www.lag.net/paramiko/) 1.12.2

You should be able to build these packages with the following commands:

	pip install jinja2
	pip install paramiko

To build the package, type the following command:

	make build

To install the package:

	make install

If you would like to install this locally, run the following commands:

	python setup.py build
	python setup.py install --prefix=/install/path/

Then make sure your Python path `PYTHONPATH` points to `/install/path/`






