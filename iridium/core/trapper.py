from tabulate import tabulate
from functools import wraps
from .logger import glob_logger
from iridium.config import config
from .exceptions import FunctionException
import yaml


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
        collector(func.__name__, str(args), str(kwargs))
        return func(*args, **kwargs)
    return wrapper


def collector(fn_name, fn_args, fn_kwargs):
    """
    collector will format the return information from the
    decorator 'trap' and place it into a simple yaml file.
     :param fn_name:
     :param fn_args:
     :param fn_kwargs:
     :return file creation status and new file.
    """
    fh = open(config.iridium_function_calls['function_log'], mode='a')
    fname = fh.name

    if fh.mode != 'a':
        raise "Please make sure %s is writable." % fname
    fn_output = yaml.dump({'Function Attributes': {'Function Name': fn_name,
                                                   'Function Arguments': fn_args,
                                                   'Function Keyword Args': fn_kwargs}})
    status = fh.write(fn_output)

    if status > 0:
        ret_val = "Data written to %s" % fname
        fh.close()
    else:
        ret_val = "Please check %s data was not saved." % fname
        fh.close()
    return ret_val

