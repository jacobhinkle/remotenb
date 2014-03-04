#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import argparse

import remotenb as rnbk

def get_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('name', nargs='?', default='default')
    parser.add_argument('-q', help='queue name',default='janus-admin')
    parser.add_argument('-n', help='number of nodes', default=1)
    return parser.parse_args(argv)
 
if __name__ == '__main__':
	
	args = get_args(sys.argv[1:])

	# My directory options
	directory = dict()
	base_dir = '/projects/molu8455' # or $HOME
	directory['default'] = 'notebooks'
	directory['infiniband'] = 'infiniband/notebooks'
	directory['tutorials'] = 'tutorials/meetup_spring_2014/master/notebooks'

	# My defaults
	opts = dict()
	opts['hostname'] = 'login'
	opts['username'] = 'molu8455'
	opts['queue'] = args.q
	opts['pwd'] = False
	opts['nodes'] = args.n
	opts['walltime'] = '04:00:00'
	opts['local_port'] = 9999

	try:
		opts['directory'] = os.path.join(base_dir, directory[args.name])
	except KeyError:
		print('list of possible notebooks:')
		map(print, directory.keys())
		sys.exit()

	rn = rnbk.RemoteNotebook(**opts)
	rn.connect() # Waits
	




