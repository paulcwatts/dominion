"""
Django templates and fabric.

Each template can be overridden in a role or host specific directory.
This is in addition to the TEMPLATE_DIRS parameter.
"""

from StringIO import StringIO
from fabric.api import env, put

from django.template.loader import render_to_string
from django.utils._os import safe_join

from dominion.utils import get_host_role

def get_templates(template_name):
    """
    Get the set of possible templates for the specific template name
    based on the current role and host.
    """
    try:
        return [
            safe_join("hosts", env.host, template_name),
            safe_join("roles", get_host_role(env.host), template_name),
            template_name
        ]
    except UnicodeDecodeError:
        # The template dir name was a bytestring that wasn't valid UTF-8.
        raise
    except ValueError:
        # The joined path was located outside of this particular
        # template_dir (it might be inside another one, so this isn't
        # fatal).
        return template_name

def put_template(template_name, remote_path, dictionary=None, **kwargs):
    d = dictionary or {}
    d.update({
        'env': env
    })
    s = render_to_string(get_templates(template_name), d)
    put(StringIO(s), remote_path, **kwargs)
