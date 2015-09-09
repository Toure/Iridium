__author__ = "Toure Dunnon, Sean Toner"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com, stoner@redhat.com"
__status__ = "Alpha"

"""
This should eventually be replaced with Tempest'nova_tests logger
"""

import logging
import time
import sys
import os
from config import config


def make_timestamp():
    """
    Returns the localtime year-month-day-hr-min-sec as a string
    """
    timevals = time.localtime()[:-3]
    ts = "-".join(str(x) for x in timevals)
    return ts


def make_timestamped_filename(prefix, postfix=".log"):
    """
    Returns a string containing prefix-timestamp-postfix
    """
    fname = prefix + "-" + make_timestamp() + postfix
    return fname


def make_logger(loggername, handlers=(), loglevel=logging.DEBUG):
    logr = logging.getLogger(loggername)
    logr.setLevel(loglevel)

    for hdlr in handlers:
        logr.addHandler(hdlr)

    return logr


def make_stream_handler(fmt, loglevel=logging.INFO):
    # Handle a stupid 2.6 to 2.7 rename
    strm_handler = logging.StreamHandler()
    strm_handler.setLevel(loglevel)
    strm_handler.setFormatter(fmt)
    return strm_handler


def make_file_handler(fmt, filename, loglevel=logging.DEBUG):
    """
    """
    file_handler = logging.FileHandler(filename)
    file_handler.setFormatter(fmt)
    file_handler.setLevel(loglevel)
    return file_handler


def make_formatter(format_str=""):
    if not format_str:
        format_str = '%(asctime)s :: %(name)-12s : %(levelname)-8s : %(message)s'

    return logging.Formatter(format_str)


def get_simple_logger(logname, filename, loglvl=logging.DEBUG):
    """
    Simple wrapper around the other functions to create a basic logger.  This is
    useful as a module level debugger

    :param logname: (str) a name to give to the logger object
    :param filename: (str) the full path of where the log file will be written (defaults to current dir)
    :param loglvl: (int) a logging loglevel
    """
    # Do the stream handler and formatter
    stream_fmt = make_formatter()
    sh = make_stream_handler(stream_fmt)

    # Make the filename, file handler and formatter
    fname = make_timestamped_filename(filename, ".log")
    file_fmt = make_formatter()
    fh = make_file_handler(file_fmt, fname)

    # get the actual logger
    logr = make_logger(logname, (sh, fh))
    logr.setLevel(loglvl)
    return logr


log_dir = config.logging["log_dir"]
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_name = os.path.join(log_dir, "iridium")

glob_logger = get_simple_logger(__name__, log_name)
