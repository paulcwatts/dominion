
class Requirement(object):
    creation_counter = 0

    "The base class for requirements."
    def __init__(self, required=True, ensure=None, depends=None):
        self.required = required
        self.ensure = ensure or "exists"
        self.depends = depends or ()
        if self.ensure == "removed":
            self.required = False

        # Increase the creation counter, and save our local copy.
        self.creation_counter = Requirement.creation_counter
        Requirement.creation_counter += 1

    def ensure_dependencies(self):
        if not self.depends:
            pass

    def execute(self):
        self.ensure_dependencies()
        if self.ensure == "exists" or self.required:
            return self.install()
        if self.ensure == "removed":
            return self.uninstall()
