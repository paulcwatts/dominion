"""
Django templates and fabric.

Each template can be overridden in a role or host specific directory.
This is in addition to the TEMPLATE_DIRS parameter.
"""
from StringIO import StringIO
from fabric.api import env, put

from django.template.loader import render_to_string
from django.conf import settings
from django.utils._os import safe_join


def get_templates(template_name):
    """
    Get the set of possible templates for the specific template name
    based on the current role and host.
    """
    result = []
    denv = env['denv']
    host = denv.get_host()
    host_name = host.hostname
    for d in settings.TEMPLATE_DIRS:
        try:
            result.append(safe_join(d, "hosts", host_name, template_name),)
            result.extend([safe_join(d, "roles", r, template_name) for r in host.rolenames])
            result.append(safe_join(d, "env", denv.name, template_name))
            result.append(safe_join(d, template_name))
        except UnicodeDecodeError:
            # The template dir name was a bytestring that wasn't valid UTF-8.
            raise
        except ValueError:
            # The joined path was located outside of this particular
            # template_dir (it might be inside another one, so this isn't
            # fatal).
            return template_name
    return result


def put_template(template_name, remote_path, dictionary=None, **kwargs):
    d = dictionary or {}
    d.update({
        'env': env
    })
    s = render_to_string(get_templates(template_name), d)
    put(StringIO(s), remote_path, **kwargs)
