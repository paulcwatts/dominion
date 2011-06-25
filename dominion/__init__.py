
from django.conf import settings
from dominion.environment import Environment
from dominion.file import File
from dominion.host import Host
from dominion.package import Package
from dominion.base import Requirement
from dominion.role import Role
from dominion.service import Service
from dominion.template import put_template

__all__ = ('configure',
    'put_template',
    'set_env',
    'Environment',
    'File',
    'Host',
    'Package',
    'Requirement',
    'Role',
    'Service')

def configure(debug=False, template_dirs=()):
    settings.configure(DEBUG=debug,
                       TEMPLATE_DEBUG=debug,
                       TEMPLATE_DIRS=template_dirs)

def set_env(env, denv):
    env['denv'] = denv
    env.user = denv.user
    env.roledefs = denv.get_roledefs()
    env.hosts = denv.get_host_list()
    env['name'] = denv.name
    env['get_host'] = denv.get_host
