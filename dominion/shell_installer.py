import copy

from fabric.api import sudo

from dominion.base import Requirement


class ShellInstaller(Requirement):
    "Defines a remote package that is installed by invoking it as a shell script."
    def __init__(self, url, env=None, *args, **kwargs):
        super(ShellInstaller, self).__init__(*args, **kwargs)
        self.url = url
        self.env = env

    def __repr__(self):
        return 'dominion.ShellInstaller:' + self.url

    def install(self):
        if self.env:
            env = " ".join(["%s=%s" % i for i in self.env.iteritems()])
        else:
            env = ''

        sudo("curl %s | %s sh" % (self.url, env))

    def uninstall(self):
        pass

    def __deepcopy__(self, memo):
        obj = copy.copy(self)
        memo[id(self)] = obj
        return obj
