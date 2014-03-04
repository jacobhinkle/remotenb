##!/usr/bin/env python

import subprocess

def create_tunnel(nodename, **kwargs):

    print '\tcreating new tunnel'
    local_port = kwargs.get('local_port',None)
    remote_port = kwargs.get('remote_port', None)
    hostname = kwargs.get('hostname', None)
    username = kwargs.get('username', None)
    port = kwargs.get('port', None)

    cmd = 'ssh -L {0}:{1}:{2} -f -N {3}@{4} -p {5}'
    cmd = cmd.format(local_port,
                      nodename,
                      remote_port,
                      username,
                      hostname,
                      port)
   
    print '\t', cmd
    pro = subprocess.Popen(cmd, 
                           shell=True, 
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)
    pro.wait()
    return pro

def delete_tunnels():

    pro = subprocess.Popen("ps -fe | grep 'ssh -L'", 
                           shell=True, 
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)
    pro.wait()
    stdout, stderr = pro.communicate()

    for line in stdout.split('\n'):
        if len(line) > 0:
            cmd = 'kill -9 ' + str(line.split()[1])
            tmp = subprocess.Popen(cmd, 
                                   shell=True, 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
            tmp.wait()

