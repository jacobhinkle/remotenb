#!/usr/bin/env python

import re
import time
import random

import jinja2 as jin

import connection as co
import tunnel as tn

template = jin.Template('''
#!/bin/bash
#PBS -N ipython_notebook
#PBS -q {{queue}}
#PBS -l walltime={{walltime}}
#PBS -l nodes={{nodes}}:ppn={{cores}}
#PBS -j oe
#PBS -o output-$PBS_JOBNAME-$PBS_JOBID

mkdir -p $HOME/.notebooks
echo $HOSTNAME > $HOME/.notebooks/node.$PBS_JOBNAME.$PBS_JOBID

mkdir -p {{directory}}
cd {{directory}}

module load python/anaconda-1.9.1

ipython notebook --matplotlib=inline --port={{remote_port}} --ip='*' --script --no-browser

''')

class RemoteNotebook:

	def __init__(self, **kwargs):
		self.args = {}
		self.args['hostname'] = kwargs.get('hostname', None)
		self.args['username'] = kwargs.get('username', None)
		self.args['port'] = kwargs.get('port', None)

		self.args['local_port'] = kwargs.get('local_port', 9999)
		self.args['walltime'] = kwargs.get('walltime', '04:00:00')
		self.args['queue'] = kwargs.get('queue', 'janus-debug')
		self.args['directory'] = kwargs.get('directory', '$HOME')
		self.args['nodes'] = kwargs.get('nodes', 1)
		self.args['pwd'] = kwargs.get('pwd', True)
		self.args['remote_port'] = random.randint(9000,60000)
		#self.args['remote_port'] = int(np.random.uniform(9000,60000,size=1)[0])
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

	def _write_pbs_script(self, rc):

		pbs_script = template.render(self.args)
		rc.sftp.open('.notebooks/ipython_notebook.pbs', 'w').write(pbs_script)

	def _start_pbs_job(self, rc):
		print '\tsubmitting job'
		_, output, _ = rc.ssh.exec_command('cd .notebooks; /curc/tools/free/redhat_6_x86_64/torque-4.2.3/bin/qsub ipython_notebook.pbs')
		
		for lines in output:
			m = re.match(r'([0-9]+).moab.rc.colorado.edu', lines)
			if m:
				jobid = m.group(1)
				return jobid

	def _get_nodename(self, rc):
		print '\twaiting for job', self.jobid, 'to start'
		while True:
			try:
				filename = '.notebooks/node.ipython_notebook.{0}.moab.rc.colorado.edu'.format(self.jobid)
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
						   username = self.args['hostname'],
						   port = self.args['hostname'],
						   pwd = self.args['pwd'])

		cmd = '/curc/tools/free/redhat_6_x86_64/torque-4.2.3/bin/qdel {0}'.format(self.jobid)
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

		cstr = '\n\tconnecting to {0}@{1} -p{2}'
		cstr = cstr.format(self.args['username'],
							self.args['hostname'],
							self.args['port'])
		print cstr
		self._create_notebooks_dir(rc)
		self._write_pbs_script(rc)
		self.jobid = self._start_pbs_job(rc)
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
						queue='janus-admin', 
						pwd=False)

	rn.connect() # Waits








