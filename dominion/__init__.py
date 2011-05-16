
from django.conf import settings
from dominion.environment import Environment
from dominion.file import File
from dominion.host import Host
from dominion.package import Package
from dominion.base import Requirement
from dominion.role import Role
from dominion.template import put_template
from dominion.utils import get_host_role


__version__ = '0.1.0'

__all__ = ('__version__',
    'configure',
    'get_host_role',
    'put_template',
    'set_env',
    'Environment',
    'File',
    'Host',
    'Package',
    'Requirement',
    'Role')

def configure(debug=False, template_dirs=()):
    settings.configure(DEBUG=debug,
                       TEMPLATE_DEBUG=debug,
                       TEMPLATE_DIRS=template_dirs)

def set_env(env, denv):
    env['denv'] = denv
    env.user = denv.user
    env.roledefs = denv.get_roledefs()
    env['name'] = denv.name
    env['get_host'] = denv.get_host
    env['get_role'] = denv.get_role
