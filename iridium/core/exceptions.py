__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"


class ArgumentError(Exception):
    pass


class ReadOnlyException(Exception):
    pass


class BootException(Exception):
    pass


class ConfigException(Exception):
    pass


class FreePageException(Exception):
    pass


class AmbiguityException(Exception):
    """
    Exception that is thrown when code can not determine what the correct
    choice should be from the given information
    """
    pass
