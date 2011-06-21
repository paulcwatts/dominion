from fabric.api import env

from django.utils.copycompat import deepcopy

from dominion.host import Host
from dominion.role import Role
from dominion.utils import get_declared_fields

#
# This is patterned off of django Forms, which users
# a custom meta-class to set base_fields.
# In our case, we set base_roles and base_nodes,
# and subclasses can then modify those
#

class EnvMetaclass(type):
    """
    Metaclass that converts Host and Role attributes to a dictionary called
    'base_hosts' and 'base_roles, taking into account parent class as well.
    """
    def __new__(cls, name, bases, attrs):
        attrs['base_hosts'] = get_declared_fields(Host, 'base_hosts', 'declared_hosts', bases, attrs)
        attrs['base_roles'] = get_declared_fields(Role, 'base_roles', 'declared_roles', bases, attrs)
        new_class = super(EnvMetaclass,
                     cls).__new__(cls, name, bases, attrs)

        return new_class

class BaseEnvironment(object):
    def __init__(self):
        self.hosts = deepcopy(self.base_hosts)
        self.roles = deepcopy(self.base_roles)
        self.hostnames = dict((h.hostname, h) for h in self.hosts.itervalues())

    def get_roledefs(self):
        "Returns the Fabric roledefs for this environment."
        result = dict((k,[]) for k in self.roles.iterkeys())
        for host in self.hosts.itervalues():
            for r in host.rolenames:
                result[r].append(host.hostname)
        return result

    def get_host(self):
        "Returns the current Host object."
        return self.hostnames[env.host]

    def get_roles(self):
        "Returns the roles array for the current Host."
        return self.hostnames[env.host].roles


class Environment(BaseEnvironment):
    "The top-level class describing a deployment environment."
    __metaclass__ = EnvMetaclass
