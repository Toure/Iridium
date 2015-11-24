from tabulate import tabulate
import sys
from functools import wraps


def echo(func):
    """
    echo will return the name of the funciton and its arguments
    as well as its return values.
    """
    @wraps(func)
    def wrapper(*args, **kwargs): pass
    pass


def collector(input):
    """
    collector will format the return information from the
    decorator 'echo' and place it into a list
    """
    pass


def fcreate(filename, path=None):
    """
    fcreate will write the file out to the specified
    path and filename.
    """
    pass
