import copy
from itertools import imap

from fabric.api import run, sudo

from dominion.base import Requirement


class ShellInstaller(Requirement):
    "Defines a remote package that is installed by invoking it as a shell script."
    def __init__(self, url, env=None, test=None, use_sudo=False, *args, **kwargs):
        super(ShellInstaller, self).__init__(*args, **kwargs)
        self.url = url
        self.env = env
        self.test = test
        self.use_sudo = use_sudo

    def __repr__(self):
        return 'dominion.ShellInstaller:' + self.url

    def install(self):
        if self.use_sudo:
            f = sudo
        else:
            f = run

        if self.env:
            env = " ".join(imap(lambda i: '='.join(i), self.env.iteritems()))
        else:
            env = ''

        cmd = "curl %s | %s sh" % (self.url, env)
        if self.test:
            f('if [ %s ]; then %s; fi' % (self.test, cmd))
        else:
            f(cmd)

    def uninstall(self):
        pass

    def __deepcopy__(self, memo):
        obj = copy.copy(self)
        memo[id(self)] = obj
        return obj
