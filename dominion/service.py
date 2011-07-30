from fabric.api import sudo, settings

from dominion.base import Requirement

class Service(Requirement):
    "Defines a service running on the remote system."
    def __init__(self, name, *args, **kwargs):
        super(Service, self).__init__(*args, **kwargs)
        if not name:
            raise ValueError("name cannot be empty")
        self.name = name

    def __repr__(self):
        return 'dominion.Service:' + str(self.name)

    def contribute_to_class(self, role, name):
        setattr(role, name, self)
        def _start():
            getattr(role, name).start()
        def _stop():
            getattr(role, name).stop()
        def _restart():
            getattr(role, name).restart()
        setattr(role, name+"_start", _start)
        setattr(role, name+"_stop", _stop)
        setattr(role, name+"_restart", _restart)

    def install(self):
        pass

    def uninstall(self):
        pass

    def start(self):
        sudo("service %s start" % self.name)

    def stop(self, warn_only=True):
        with settings(warn_only=warn_only):
            sudo("service %s stop" % self.name)

    def restart(self, warn_only=True):
        self.stop(warn_only)
        self.start()
