from tabulate import tabulate
from functools import wraps
from .logger import glob_logger
from iridium.config import config
from .exceptions import FunctionException


def tracer(func):
    """
    tracer will decorate a given function which allow users to step through
    a function call on error.
    :param func: Function which is to be wrapped.
    :return: decorated function.
    """
    import pdb
    from inspect import signature

    @wraps(func)
    def wrapper(*args, **kwargs):
        glob_logger.information("calling: {0} with these args: {1}".format(func.__name__, signature(func)))
        try:
            return func(*args, **kwargs)
        except FunctionException as fne:
            print('We catch a function: {0:s} with a value of: {1:s} doing something bad'.format(fne.func_name,
                                                                                                 fne.value))
            pdb.set_trace()
    return wrapper


def trap(func):
    """
    trap will return the name of the function and its arguments
    as well as its return values.
    :param func: function for which to decorate.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        fn_calls = list([func.__name__, str(args), kwargs])
        collector(fn_calls)
        return func(*args, **kwargs)
    return wrapper


def collector(table_info, headers=None):
    """
    collector will format the return information from the
    decorator 'trap' and place it into a simple table format
    with the following structure:
     table = [["function1", (42, 12, 30), 20],
              ["function2", (32, 304, 3), 30]]
     headers = ["Function Name", "Arguments", "Return Values"]
     :param headers: this defines the layout of the table header see example above.
     :param table_info: three element list which will contain the format which
     is described in the docstrings.
     :return file creation status and new file.
    """
    filehandle = open(config.iridium_function_calls['function_log'], mode='a')
    filename = filehandle.name

    if filehandle.mode != 'a':
        raise "Please make sure %s is writable." % filename
    if headers is None:
        headers = ["Function Name", "Arguments", "Keyword Arguments"]
    table_out = tabulate(table_info, headers, tablefmt="grid")
    status = filehandle.write(table_out)

    if status > 0:
        ret_val = "Data written to %s" % filename
        filehandle.close()
    else:
        ret_val = "Please check %s data was not saved." % filename
        filehandle.close()
    return ret_val

