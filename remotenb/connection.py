#!/usr/bin/env python

import os
import sys
import paramiko
import getpass
import socket

class Connection:

	def __init__(self, hostname, username=None, port=None, pwd=True):

		self.ssh = paramiko.SSHClient()
		self.sftp = None

		#self.ssh.load_system_host_keys()
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

		conf = paramiko.SSHConfig()
		conf.parse(open(os.path.expanduser('~/.ssh/config')))
		host = conf.lookup(hostname)
		self.host = host
		self.hostname = host['hostname']
		self.username = host.get('user', username)
		self.port = int(host.get('port', port))
		self.key_filename = host.get('identityfile', None)
		self.proxy = self._set_proxy(host)
		self.password = self._get_password(pwd)

		self._open_ssh()
		self._open_sftp()

	def __enter__(self):
		return self

	def __exit__(self, type, value, tb):
		self.close()

	def __del__(self):
		self.close()

	def close(self):
		#print 'connection closed'
		if self.sftp:
			self.sftp.close()
		if self.ssh.get_transport():
			self.ssh.close()

	def _open_ssh(self):
		try:
			self.ssh.connect(
				self.hostname,
				username = self.username,
				port = self.port,
				key_filename = self.key_filename,
				password = self.password,
				sock = self.proxy
			)
		except socket.error, e:
			print e
			sys.exit(1)
		except paramiko.BadAuthenticationType, e:
			print e
			sys.exit(1)

	def _open_sftp(self):
		if not self.ssh.get_transport():
			self._open_ssh()
		self.sftp = self.ssh.open_sftp()

	def _set_proxy(self, host):
		proxy = None
		if host.get('proxycommand', None):
			proxy = paramiko.ProxyCommand(host.get('proxycommand', None))
		return proxy

	def _get_password(self, request_pwd):
		p = None
		if request_pwd:
			p = getpass.getpass('Password for %s@%s: ' % (self.username, self.hostname))
			p = p if len(p) > 0 else None
		return p

if __name__ == '__main__':

	print 'Test connection to login'

	conn = Connection('login', pwd=False)
	_, output, _ = conn.ssh.exec_command('ls -l')
	for out in output:
		print out

	conn.close()

	print 'Test connection to bumba'

	with Connection('bumba', pwd=False) as conn:
		_, output, _ = conn.ssh.exec_command('ls -l')
		for out in output:
			print out
