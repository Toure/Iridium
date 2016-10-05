__author__ = "Toure Dunnon, Sean Toner"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com, stoner@redhat.com"
__status__ = "Alpha"

import logging
import time
import os

from iridium.config.configmanager import ConfigManager

cm = ConfigManager()


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
    """

    :param loggername:
    :param handlers:
    :param loglevel:
    :return:
    """
    logr = logging.getLogger(loggername)
    logr.setLevel(loglevel)

    for hdlr in handlers:
        logr.addHandler(hdlr)

    return logr


def make_stream_handler(fmt, loglevel=logging.INFO):
    """

    :param fmt:
    :param loglevel:
    :return:
    """
    strm_handler = logging.StreamHandler()
    strm_handler.setLevel(loglevel)
    strm_handler.setFormatter(fmt)
    return strm_handler


def make_file_handler(fmt, filename, loglevel=logging.DEBUG):
    """

    :param fmt:
    :param filename:
    :param loglevel:
    :return:
    """
    file_handler = logging.FileHandler(filename)
    file_handler.setFormatter(fmt)
    file_handler.setLevel(loglevel)
    return file_handler


def make_formatter(format_str=""):
    """

    :param format_str:
    :return:
    """
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


def _glob_logger(log_dir=None):
    """

    :param log_dir:
    :return:
    """
    if log_dir is None:
        log_dir = cm.cfg_manager("log_dir")

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_name = os.path.join(log_dir, "iridium")
    return log_name


glob_logger = get_simple_logger(__name__, _glob_logger())

