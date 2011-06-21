from django.utils.datastructures import SortedDict

from fabric.api import env

def get_declared_fields(field_type, base_attr, declared_attr, bases, attrs, with_base_fields=True):
    """
    Create a list of field instances from the passed in 'attrs', plus any
    similar fields on the base classes (in 'bases'). This is used by both
    the Enviroment metaclass.

    If 'with_base_fields' is True, all fields from the bases are used.
    Otherwise, only fields in the 'declared_fields' attribute on the bases are
    used. The distinction is useful in ModelForm subclassing.
    Also integrates any additional media definitions
    """
    fields = [(field_name, attrs.pop(field_name)) for field_name, obj in attrs.items() if isinstance(obj, field_type)]
    fields.sort(key=lambda x: x[1].creation_counter)

    # If this class is subclassing another Form, add that Form's fields.
    # Note that we loop over the bases in *reverse*. This is necessary in
    # order to preserve the correct order of fields.
    if with_base_fields:
        for base in bases[::-1]:
            if hasattr(base, base_attr):
                fields = getattr(base, base_attr).items() + fields
    else:
        for base in bases[::-1]:
            if hasattr(base, declared_attr):
                fields = getattr(base, declared_attr).items() + fields

    return SortedDict(fields)
