from StringIO import StringIO

import django.utils.copycompat as copy

from fabric.api import put, run, sudo

from dominion.base import Requirement
from dominion.template import put_template

class File(Requirement):
    "Defines a file or directory to be installed (or removed) from the host."
    def __init__(self, name, directory=False, symlink=None,
                 template=None, content=None,
                 owner=None, group=None, mode=None,
                 dictionary=None,
                 use_sudo=False,
                 *args, **kwargs):
        super(File, self).__init__(*args, **kwargs)
        if not name:
            raise ValueError("name cannot be empty")
        self.name = name
        self.directory = directory
        self.symlink = symlink
        self.template = template
        self.content = content
        self.owner = owner
        self.group = group
        self.mode = mode
        self.dictionary = dictionary
        self.use_sudo = use_sudo

    def install(self):
        if self.use_sudo:
            f = sudo
        else:
            f = run

        if self.directory:
            f("mkdir -p '%s'" % self.name)

        elif self.symlink:
            f("ln -s '%s' '%s'" % (self.symlink, self.name))

        elif self.template:
            put_template(self.template, self.name,
                         self.dictionary, use_sudo=self.use_sudo)

        elif self.content:
            put(StringIO(self.content), self.name, use_sudo=self.use_sudo)

        if self.owner or self.group:
            if self.group:
                args = '%s:%s' % (self.owner or '', self.group or '')
            else:
                args = self.owner
            f("chown %s '%s'" % (args, self.name))

        if self.mode:
            f("chmod %s '%s'" % (self.mode, self.name))

    def uninstall(self):
        if self.use_sudo:
            f = sudo
        else:
            f = run

        if self.directory:
            f("rm -rf '%s'" % self.name)
        else:
            f("rm '%s'" % self.name)
