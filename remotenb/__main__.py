"""Main function. Call this with python -mremotenb"""

import remote_notebook as rnbk

import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('name', nargs='?', default='default')
parser.add_argument('-q', help='queue name',default='janus-admin')
parser.add_argument('-n', help='number of nodes', default=1)
args = parser.parse_args(sys.argv[1:])

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
opts['nodes'] = args.n
opts['walltime'] = '04:00:00'
opts['local_port'] = 9999

try:
    opts['directory'] = os.path.join(base_dir, directory[args.name])
except KeyError:
    print('list of possible notebooks:')
    for k in directory.keys():
        print k
    sys.exit()

rn = rnbk.RemoteNotebook(**opts)
rn.connect() # Waits


