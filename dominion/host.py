
from fabric.api import env

class Host(object):
    "The definition of a single host in an environment."
    creation_counter = 0

    def __init__(self, hostname, role=None):
        self.hostname = hostname
        self.rolename = role

        # Increase the creation counter, and save our local copy.
        self.creation_counter = Host.creation_counter
        Host.creation_counter += 1

    @property
    def role(self):
        if hasattr(self, '_role'):
            return self._role
        return env['denv'].roles[self.rolename]
