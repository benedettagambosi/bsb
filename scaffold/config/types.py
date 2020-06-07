from ..exceptions import *


def any():
    def type_handler(value):
        return value

    type_handler.__name__ = "any"
    return type_handler


def or_(*type_args):
    handler_name = "any of: " + ", ".join(map(lambda x: x.__name__, type_args))

    def type_handler(value):
        for t in type_args:
            try:
                v = t(value)
                break
            except (TypeError, CastError):
                continue
        else:
            raise TypeError("Couldn't cast {} into {}".format(value, handler_name))
        return v

    type_handler.__name__ = handler_name
    return type_handler


def scalar_expand(scalar_type, size=None, expand=None):
    """
        Create a method that expands a scalar into an array with a specific size or uses
        an expansion function.

        :param scalar_type: Type of the scalar
        :type scalar_type: type
        :param size: Expand the scalar to an array of a fixed size.
        :type size: int
        :param expand: A function that takes the scalar value as argument and returns the expanded form.
        :type expand: callable
        :returns: Type handler function
        :rtype: callable
    """

    def type_handler(value):
        # No try block: let it raise the cast error.
        v = scalar_type(value)
        # Expand the scalar.
        return expand(v)

    type_handler.__name__ = "expanded list of " + scalar_type.__name__
    return type_handler


_list = list


def list(type=str, size=None):
    def type_handler(value):
        v = _list(value)
        try:
            for i, e in enumerate(v):
                v[i] = type(e)
        except:
            raise TypeError(
                "Couldn't cast element {} of {} into {}".format(i, value, type.__name__)
            )
        if size is not None and len(v) != size:
            raise ValueError(
                "Couldn't cast {} into a {} element list".format(value, size)
            )
        return v

    type_handler.__name__ = "list{} of {}".format(
        "[{}]".format(size) if size is not None else "", type.__name__
    )
    return type_handler