

class Requirement(object):
    """
    Requirements are the basis for Dominion. They define
    what needs to exist on a host/role, or perhaps what *mustn't* exist.

    Requirements are defined on Roles.
    """
    creation_counter = 0

    "The base class for requirements."
    def __init__(self, required=True, ensure=None, depends=None, post=None):
        self.required = required
        self.ensure = ensure or "exists"
        self.depends = depends or ()
        if self.ensure == "removed":
            self.required = False
        self.post = post or ()

        # Increase the creation counter, and save our local copy.
        self.creation_counter = Requirement.creation_counter
        Requirement.creation_counter += 1

    def __call__(self):
        self.apply()

    def apply(self):
        if self.ensure == "exists" or self.required:
            if hasattr(self, 'install'):
                return self.install()
        if self.ensure == "removed":
            if hasattr(self, 'uninstall'):
                return self.uninstall()
