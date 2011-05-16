from itertools import ifilter

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
        # Set all the requirements as attributes of this object for
        # easier access (this is in lieu of a more complex
        # contribute_to_class idiom like Django models)
        for k, v in self.reqs.iteritems():
            setattr(self, k, v)

        # Increase the creation counter, and save our local copy.
        self.creation_counter = Role.creation_counter
        Role.creation_counter += 1

    def execute(self):
        for name, req in self.reqs.iteritems():
            req.execute()

    def __getitem__(self, name):
        "Returns a Requirement with the given name."
        try:
            req = self.reqs[name]
        except KeyError:
            raise KeyError('Key %r not found in Role' % name)
        return req

class Role(BaseRole):
    "The role of a specific host."
    __metaclass__ = RoleMetaclass
