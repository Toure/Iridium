from tabulate import tabulate
from functools import wraps
from .exceptions import ArgumentError
#from ..config import config
#import pickle


def echo(fh):
    """
    echo will return the name of the function and its arguments
    as well as its return values.
    :param fh: filehandle needed for collector.
    """
    def func_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ret = func(*args, **kwargs)
            if ret is None:
                ret = "empty"
            fn_calls = []
            if args:
                fn_calls.append([func.__name__, args, ret])
            elif kwargs:
                fn_calls.append([func.__name__, kwargs, ret])
            else:
                raise ArgumentError
            collector(fh, fn_calls)
        return wrapper
    return func_wrapper


def collector(filehandle, table_info, headers=None):
    """
    collector will format the return information from the
    decorator 'echo' and place it into a simple table format
    with the following structure:
     table = [["function1", (42, 12, 30), 20],
              ["function2", (32, 304, 3), 30]]
     headers = ["Function Name", "Arguments", "Return Values"]
     :param headers: this defines the layout of the table header see example above.
     :param filehandle: file handle which the formatted table will be written.
     :param table_info: three element list which will contain the format which
     is described in the docstrings.
     :return file creation status.
    """
    filename = filehandle.name

    if filehandle.mode != 'a':
        raise "Please make sure %s is writable." % filename
    if headers is None:
        headers = ["Function Name", "Arguments", "Return Values"]
    table_out = tabulate(table_info, headers, tablefmt="fancy_grid")
    status = filehandle.write(table_out)

    if status > 0:
        ret_val = "Data written to %s" % filename
        filehandle.close()
    else:
        ret_val = "Please check %s data was not saved." % filename
        filehandle.close()
    return ret_val


def packer(func, *args, **kwargs):
    """Packer is responsible for creating a datastructure which will be
    needed for replay.

    Args:
        func (TYPE): function object which will be store in datastructure.
        *args: arguments for function object.
        **kwargs: keyword arguments for function.

    Returns:
        TYPE: dict
    """
    pass
