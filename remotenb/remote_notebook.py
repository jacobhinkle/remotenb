#!/usr/bin/env python

import re
import time
import random

import jinja2 as jin

import connection as co
import tunnel as tn

template = jin.Template('''#!/bin/bash
#SBATCH -J ipython_notebook
#SBATCH --qos {{queue}}
#SBATCH --time={{walltime}}
#SBATCH -N {{nodes}}
#SBATCH --ntasks-per-node {{cores}}
#SBATCH --output output-ipython_nodebook-%j

mkdir -p $HOME/.notebooks
echo $HOSTNAME > $HOME/.notebooks/node.ipython_notebook.$SLURM_JOB_ID

mkdir -p {{directory}}
cd {{directory}}

. /etc/profile.d/modules.sh

module load python/anaconda-1.9.1

ipython notebook --matplotlib=inline --port={{remote_port}} --ip='*' --script --no-browser

''')

class RemoteNotebook:

	def __init__(self, **kwargs):
		self.args = {}
		self.args['hostname'] = kwargs.get('hostname', None)
		self.args['username'] = kwargs.get('username', None)
		self.args['port'] = kwargs.get('port', 22)

		self.args['local_port'] = kwargs.get('local_port', 9999)
		self.args['walltime'] = kwargs.get('walltime', '01:00:00')
		self.args['queue'] = kwargs.get('queue', 'normal')
		self.args['directory'] = kwargs.get('directory', '$HOME')
		self.args['nodes'] = kwargs.get('nodes', 1)
		self.args['pwd'] = kwargs.get('pwd', True)
		self.args['remote_port'] = random.randint(9000,60000)
		self.args['cores'] = 12
		

	def __str__(self):
		tmp = 'RemoteNotebook\n'
		for key in self.args.keys():
			tmp += key + ': ' + str(self.args[key]) +'\n'
		return tmp

	def __del__(self):
		pass

	def _create_notebooks_dir(self, rc):
		try:
			rc.sftp.mkdir(".notebooks")
		except IOError:
			pass

	def _write_slurm_script(self, rc):

		slurm_script = template.render(self.args)
		rc.sftp.open('.notebooks/ipython_notebook.slurm', 'w').write(slurm_script)

	def _start_slurm_job(self, rc):
		print '\tsubmitting job'
		_, output, _ = rc.ssh.exec_command('cd .notebooks; /curc/slurm/slurm/current/bin/sbatch ipython_notebook.slurm')
		jobid = int(output.read().strip().split()[-1])
		return jobid

	def _get_nodename(self, rc):
		print '\twaiting for job', self.jobid, 'to start'
		while True:
			try:
				filename = '.notebooks/node.ipython_notebook.{0}'.format(self.jobid)
				nodename = rc.sftp.open(filename, 'r').read().strip()
				return nodename
			except IOError:
				time.sleep(10)	

	def _wait(self):
		print '\tCNTR-C to quit job and exit'
		try:
			while(True):
				time.sleep(60)
		except KeyboardInterrupt:
			print '\n\tattempting to cancel job...'
			self.close()
			print '\tnotebook closed'

	def close(self):
		rc = co.Connection(self.args['hostname'], 
						   username = self.args['username'],
						   port = self.args['port'],
						   pwd = self.args['pwd'])

		cmd = '/curc/slurm/slurm/current/bin/scancel {0}'.format(int(self.jobid))
		rc.ssh.exec_command(cmd)

		cmd = 'rm .notebooks/*'
		rc.ssh.exec_command(cmd)

		rc.close()

	def connect(self):

		rc = co.Connection(self.args['hostname'], 
						   username = self.args['username'],
						   port = self.args['port'],
						   pwd = self.args['pwd'])

		self.args['username'] = rc.username
		self.args['hostname'] = rc.hostname
		self.args['host'] = rc.host
		self.args['port'] = rc.port

		cstr = '\n\tconnecting to {0}@{1} -p {2}'
		cstr = cstr.format(self.args['username'],
							self.args['hostname'],
							self.args['port'])
		print cstr
		self._create_notebooks_dir(rc)
		self._write_slurm_script(rc)
		self.jobid = self._start_slurm_job(rc)
		self.nodename = self._get_nodename(rc)
		rc.close()
	    

		tn.delete_tunnels()
		tn.create_tunnel(self.nodename, 
						 local_port=self.args['local_port'], 
						 remote_port=self.args['remote_port'], 
						 hostname=self.args['hostname'],
						 username = self.args['username'],
						 port = self.args['port']
						 )

		self._wait()
		


if __name__ == '__main__':

	rn = RemoteNotebook(hostname='login', 
						directory='/projects/molu8455/notebooks', 
						queue='normal', 
						pwd=False)

	rn.connect() # Waits

