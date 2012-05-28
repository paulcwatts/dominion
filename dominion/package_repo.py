import copy

from fabric.api import run

from dominion.base import Requirement


class PackageRepo(Requirement):
    "Defines a package repository to be added (or removed) from the host."
    def __init__(self, repo_name, manager=None, *args, **kwargs):
        super(PackageRepo, self).__init__(*args, **kwargs)
        if type(repo_name) in (list, tuple):
            self.repo_name = ' '.join(repo_name)
        else:
            self.repo_name = repo_name
        self.manager = manager or "apt"

        # These could potentially be defined explicitly by subclasses
        if not hasattr(self, 'install'):
            self.install = getattr(self, '_install_' + self.manager, None)
        if not hasattr(self, 'uninstall'):
            self.uninstall = getattr(self, '_uninstall_' + self.manager, None)
        if not self.install or not self.uninstall:
            raise ValueError("Unknown package manager: " + self.manager)

    def __repr__(self):
        return 'dominion.PackageRepo:' + str(self.repo_name)

    def _install_apt(self):
        if self.repo_name.startswith('ppa:'):
            name = 'http://ppa.launchpad.net/' + self.repo_name[4:]
        else:
            name = self.repo_name

        fmt = """if [ -z "`cat /etc/apt/sources.list /etc/apt/sources.list.d/*.list | grep '%s'`" ]; then sudo apt-add-repository '%s'; sudo apt-get update; fi"""
        cmd = fmt % (name, self.repo_name)
        run(cmd)

    def _uninstall_apt(self):
        # No good way to do this
        pass

    def __deepcopy__(self, memo):
        obj = copy.copy(self)
        memo[id(self)] = obj
        return obj
