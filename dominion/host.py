
from fabric.api import env

class Host(object):
    "The definition of a single host in an environment."
    creation_counter = 0

    def __init__(self, hostname, roles=None):
        self.hostname = hostname
        self.rolenames = roles

        # Increase the creation counter, and save our local copy.
        self.creation_counter = Host.creation_counter
        Host.creation_counter += 1

    @property
    def roles(self):
        if hasattr(self, '_roles'):
            return self._roles
        self._roles = [env['denv'].roles[r] for r in self.rolenames]
        return self._roles

    def apply(self, name="all"):
        "Applies the role's requirements to this host."
        for r in self.roles:
            r.apply(name)
