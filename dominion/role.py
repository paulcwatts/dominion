from django.utils.copycompat import deepcopy

from dominion.base import Requirement
from dominion.utils import get_declared_fields

class RoleMetaclass(type):
    """
    Metaclass that converts Host and Role attributes to a dictionary called
    'base_hosts' and 'base_roles, taking into account parent class as well.
    """
    def __new__(cls, name, bases, attrs):
        attrs['base_reqs'] = get_declared_fields(Requirement, 'base_reqs', 'declared_reqs', bases, attrs)
        new_class = super(RoleMetaclass,
                     cls).__new__(cls, name, bases, attrs)

        return new_class

class BaseRole(object):
    "The role of a specific host."
    creation_counter = 0

    def __init__(self):
        self.reqs = deepcopy(self.base_reqs)

        # Increase the creation counter, and save our local copy.
        self.creation_counter = Role.creation_counter
        Role.creation_counter += 1

    def execute(self):
        for name, req in self.reqs.iteritems():
            req.execute()


class Role(BaseRole):
    "The role of a specific host."
    __metaclass__ = RoleMetaclass
