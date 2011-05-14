
from fabric.api import env

def get_host_role(host):
    """
    For a specific hostname, return the host's role.
    """
    for k,v in env.roledefs.iteritems():
        if host in v:
            return k
