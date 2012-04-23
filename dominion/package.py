import copy

from fabric.api import sudo

from dominion.base import Requirement


class Package(Requirement):
    "Defines a package to be installed (or removed) from the host."
    def __init__(self, package_name, manager=None, *args, **kwargs):
        super(Package, self).__init__(*args, **kwargs)
        if type(package_name) in (list, tuple):
            self.package_name = ' '.join(package_name)
        else:
            self.package_name = package_name
        self.manager = manager or "apt"

        # These could potentially be defined explicitly by subclasses
        if not hasattr(self, 'install'):
            self.install = getattr(self, '_install_' + self.manager, None)
        if not hasattr(self, 'uninstall'):
            self.uninstall = getattr(self, '_uninstall_' + self.manager, None)
        if not self.install or not self.uninstall:
            raise ValueError("Unknown package manager: " + self.manager)

    def __repr__(self):
        return 'dominion.Package:' + str(self.package_name)

    def _install_apt(self):
        sudo("apt-get install -q -y " + self.package_name)

    def _uninstall_apt(self):
        sudo("apt-get remove -q -y " + self.package_name)

    def _install_pip(self):
        sudo("pip install -U " + self.package_name)

    def _uninstall_pip(self):
        sudo("pip uninstall " + self.package_name)

    def _install_easy_install(self):
        sudo("easy_install -q -U " + self.package_name)

    def _uninstall_easy_install(self):
        pass

    def __deepcopy__(self, memo):
        obj = copy.copy(self)
        memo[id(self)] = obj
        return obj
