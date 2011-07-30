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
            if hasattr(v, 'contribute_to_class'):
                v.contribute_to_class(self, k)
            else:
                setattr(self, k, v)

        # Increase the creation counter, and save our local copy.
        self.creation_counter = Role.creation_counter
        Role.creation_counter += 1

    def apply(self, req="all"):
        if req == "all":
            return self._apply_seq(self.reqs.iteritems())
        if isinstance(req, tuple) or isinstance(req, list):
            seq = [(name, getattr(self, name)) for name in req if hasattr(self, name)]
            return self._apply_seq(seq)
        else:
            if not hasattr(self, req):
                return
            seq = ((req, getattr(self, req)),)
            return self._apply_seq(seq)

    def _unique(self, seq, idfun=None):
        if idfun is None:
            def idfun(x): return x
        seen = {}
        result = []
        for item in seq:
            marker = idfun(item)
            if marker in seen:
                continue
            seen[marker] = 1
            result.append(item)
        return result

    def _get_related(self, req):
        """
        Recursively collects the dependencies and post actions for
        the requirement.
        """
        depends = []
        reqdepends = getattr(req, 'depends', [])
        post = []
        for d in reqdepends:
            dreq = getattr(self, d)
            reldepends, relpost = self._get_related(dreq)
            depends.extend(reldepends)
            post.extend(relpost)
        depends.extend(reqdepends)
        post.extend(getattr(req, 'post', []))
        return depends, post

    def _apply_seq(self, seq):
        """
        Applies an ordered list of requirements, their dependencies,
        and their post actions.
        """
        # For each in the sequence, recursively add all requirements
        # Add all in the sequence that haven't been added
        # Add all the post actions
        to_apply = []
        post_apply = []
        for name, req in seq:
            depends, post = self._get_related(req)
            to_apply.extend(depends)
            to_apply.append(req)
            post_apply.extend(post)

        # We need to convert all to their appropriate requirements
        # objects before applying any uniqueness
        def _get(req):
            if callable(req):
                return req
            else:
                return getattr(self, req)
        to_apply = map(_get, to_apply)
        post_apply = map(_get, post_apply)

        to_apply = self._unique(to_apply)
        post_apply = self._unique(post_apply)
        to_apply.extend(post_apply)

        for req in to_apply:
            req()


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
