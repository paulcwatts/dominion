
from django.conf import settings

__version__ = '0.1.0'

__all__ = ('__version__', 'configure')

def configure(debug=False, template_dirs=()):
    settings.configure(DEBUG=debug,
                       TEMPLATE_DEBUG=debug,
                       TEMPLATE_DIRS=template_dirs)
