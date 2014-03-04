.. remotenb documentation master file, created by
   sphinx-quickstart on Tue Mar  4 10:39:03 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


.. _paramiko: http://www.lag.net/paramiko/
.. _jinja2: http://jinja.pocoo.org/docs/


Remote IPython Notebook
====================================

This package will launch a PBS job and a remote **IPython notebook** on the JANUS supercomputer. The package is installed locally and nothing needs to be setup on the remote connection.  Instead, *remotenb* uses `paramiko`_ to move files and execute commands.


Installation
-------------

Requirements:


- `jinja2`_ 2.7.1
- `paramiko`_ 1.12.2

You should be able to build these packages with the following commands::

	pip install jinja2
	pip install paramiko

To build the package, type the following command::

	make build


To install the package::

	make install

If you would like to install this locally, run the following commands::

	python setup.py build
	python setup.py install --prefix=/install/path/

Then make sure your Python path `PYTHONPATH` points to `/install/path/`

It is also important that you have an `.ssh/config` set up for JANUS.  First, you will need to create a control sockets directory::
	
	mkdir ~/.ssh/sockets

Then add the following lines of code your your `~/.ssh/config` file::

	Host login
		HostName login.rc.colorado.edu
		User molu8455
		ControlMaster auto
		ControlPath ~/.ssh/sockets/%r@%h:%p

This will allow you to access janus by simply typing::

	ssh login

Please make sure this works before testing the remote notebook.


Usage
-----------

The `remotenb` is really just an object and there are several ways to use it.  The most simple example just instantiates the object and calls the `connect()` method.  

:download:`example.py <../../example.py>`

.. literalinclude:: ../../examples/example.py
  :language: python

Once you have your ssh config file working, you can try this example out by typing::

	python example.py

You should see something like the following::

	bash-mac$ python example.py 
	Password for molu8455@login: 

	connecting to molu8455@login -p 53770
	submitting job
	2524645.moab.rc.colorado.edu
	waiting for job 2524645 to start
	creating new tunnel
	ssh -L 9999:node1073:24168 -f -N molu8455@login -p 53770
	CNTR-C to quit job and exit

To terminate your session, type `CTRL-C`::

	attempting to cancel job...
	notebook closed




Advanced Usage
-----------------

The following example provides an easy to use command line tool for managing your remote notebooks.

:download:`example.py <../../notebook.py>`

.. literalinclude:: ../../examples/notebook.py
  :language: python

I make this an executable and copy it to my `~/bin` directory.  Then I can type the following::

	notebook.py

which will launch my default location with my default values.  Or I may want to use a different queue and location::

	notebook.py infiniband -q crc-serial

this takes me to the `infiniband/notebooks` directory on a `crc-serial` queue.  Finally, I may want a few extra nodes::

	notebook.py tutorials -n 3














