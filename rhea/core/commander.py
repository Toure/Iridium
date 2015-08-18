__author__ = "Sean Toner"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "stoner@redhat.com"
__status__ = "Alpha"

from subprocess import Popen, PIPE, STDOUT
import threading
import os
import shlex
from functools import wraps
try:
    import queue
except ImportError:
    import Queue as queue

from rhea.core.logger import glob_logger as LOGGER

LOG_DIR = "logs"
if not os.path.exists("logs"):
    os.mkdir("logs")
os.environ["PYTHONUNBUFFERED"] = "1"


def read_sysinfo(path):
    """
    Generally used to read one of the sysinfo files

    :param path: Path to the file
    :return:
    """
    with open(path, "r") as sysinfo:
        return sysinfo.read()


def write_sysinfo(path, val):
    """
    Writes val into the file specified by path.  Generally used for one of the
    /proc or /sys files

    :param path: Path in sysinfo to write
    :param val: New value the file will take
    :return: The value now in path
    """
    with open(path, "w") as sysinfo:
        sysinfo.write(val)
    with open(path, "r") as sysinfo:
        return sysinfo.read()


def freader(fobj, monitor=None, save=None, showout=True, proc=None):
    """
    Small function which can be thrown into a thread to read a long running
    subprocess

    :param fobj: a file like object that will be read from
    :param monitor: A Queue object
    :param interval: polling interval between reads
    :param save: (list) by default dont save, otherwise append output to this
    """
    while not fobj.closed:
        if proc is not None:
            if proc.poll() is not None:
                break
        try:
            item = monitor.get_nowait()
            if item == "stop":
                break
        except queue.Empty:
            pass
        except AttributeError:
            pass
        line = fobj.readline()  # blocks when nothing in fobj buffer
        if line and showout:
            LOGGER.info(line.strip())
        if save is not None:
            save.put(line)


def creader(cobj, interval=0.2, save=None):
    freader(cobj.proc.stdout, save=save)


class Result:
    """A simple way of declaring a result from an operation"""
    def __init__(self, rc, msg="", data=None):
        """
        Args:
          - rc(int): an integer value for the returncode
          - msg(str): a descriptive message
          - data(any): relevant data from the operation
        """
        self.result = rc
        self.description = msg
        if data is None:
            self.data = {}
        else:
            self.data = data


class ResultException(Exception):
    pass


def stringify(fn):
    @wraps(fn)
    def outer(*args, **kwargs):
        result = fn(*args, **kwargs)
        if isinstance(result, bytes):
            result = result.decode()
        return result
    return outer


class ProcessResult:
    """
    Represents the result of a subprocess.

    Because we might run the subprocess in a non-blocking manner (ie, not
    calling communicate), this class represents the current state of the
    process.  That means we may not have the returncode, stdout or stderr
    yet.

    This class models a "truthiness" value so a ProcessResult object can
    be used in truth value testing.  It also implements the == operator
    to make it easier to do return code checking.  This was done because
    subclassing from int made no sense if the subprocess was not complete
    since the result of popen_obj.poll() or popen_obj.returncode would be
    None, and int types must have an int value ('inf' and 'nan' are for
    float types)
    """
    def __init__(self, command=None, outp="", error="", meta=None, logger=LOGGER):
        """
        Args:
          - cmdobj(Command): the Command object
          - outp(str): a str used to hold output
          - error(str): a str used to hold error
          - logger(logging): logging object
        """
        if command is None or not isinstance(command, Command):
            raise ResultException("Must pass in a command object")

        self.logger = logger
        self.cmd = command
        self.proc = command.proc
        self._output = outp
        self._error = error
        self._rdr_thr = None
        self._returncode = self.proc.poll()
        self.block_read = False
        self.thread_mon = queue.Queue(maxsize=1)
        self.output_queue = queue.Queue()

    def __nonzero__(self):
        """
        Allows the ProcessResult object to be used for truthiness

        example::

            result = ProcessResult(proc)
            if result:
                print result.output
        """
        if self.returncode is not None:
            return True
        return False

    def __eq__(self, other):
        """
        Allows the ProcessResult object to be used for int equality
        checking.

        Usage::

            result = ProcessResult(proc)
            if result == 0:
                print("subprocess was successful")

        """
        if self.returncode == other:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def _check_filehandle(self, fh_name="stdout"):
        try:
            stdout = getattr(self.proc, fh_name)
            if not stdout.closed:
                return stdout
            # FIXME: What if stdout is closed?
        except AttributeError as ae:
            # TODO: no self.proc.stdout, check if self.proc is a file handle
            raise ae

    @property
    @stringify
    def output(self):
        if self._output:
            return self._output

        outp = self._check_filehandle()
        if self.proc.poll() is None:
            self.logger.warning("Process is not yet finished")
            mon = self.thread_mon
            rdr_thread = threading.Thread(target=freader, args=(outp,),
                                          kwargs={"save": self.output_queue,
                                                  "monitor": mon,
                                                  "proc": self.proc})
            rdr_thread.start()
            self._rdr_thr = rdr_thread
            if self.block_read:
                self._rdr_thr.join()
        elif not self._output:
            try:
                self._output = outp.read()  # this will block
            except AttributeError:
                self.logger.warning("proc.stdout was None")
                self._output = ""

        return self._output

    @output.setter
    def output(self, val):
        self.logger.error("output is read-only. Not setting to {}".format(val))

    @property
    def returncode(self):
        self._returncode = self.proc.poll()
        return self._returncode


class CommandException(Exception):
    def __init__(self, msg=""):
        super(CommandException, self).__init__(msg)
        self.msg = msg


class Command(object):
    """
    A class to handle executing subprocesses.

    The intention is to allow a simpler way to handle threading or
    multiprocessing functionality.  This also allows the caller to chose to
    block (waiting for the subprocess to return) or not.
    """
    def __init__(self, cmd=None, user="root", pw="", logr=None, stdin=PIPE,
                 stdout=PIPE, stderr=STDOUT, saveout=True, host=None):
        """
        *Args:*
            - cmd(str|list): The command to be executed, either in string or
                             list format
            - user(str): The user to run command as (if remote execution)
            - logr(Logger): a logging.Logger instance. if None, use LOGGER
            - stdin(file-like): defaults to PIPE, but can use file-like object
            - stdout(file-like): default uses PIPE, but can be file-like object
            - stderr(file-like): same as stdout
            - hosts(str): The ip or hostname to issue command to

        PreCondition:  If using remote execution, the public key must have been
        copied to the remote machine for passwordless authentication
        """
        self.cmd = cmd
        self.out = stdout
        self.err = stderr
        self.inp = stdin
        self.fails = {}
        self.pw = pw
        self.user = user
        self.host = host
        self.saveout = saveout
        if logr:
            self.logger = logr
        else:
            self.logger = LOGGER

    def __call__(self,
                 cmd=None,
                 showout=True,
                 showerr=True,
                 block=True,
                 checkresult=(True, 0),
                 throws=True,
                 remote=True,
                 timeout=None,
                 **kwds):
        """
        This is a wrapper around subprocess.Popen constructor.  The **kwds
        takes the same keyword args as the Popen constructor does.  During
        initialization, by default PIPE will be used for the stdout and stderr,
        however, file-like objects may be passed in instead (for example to
        log)

        *Args:*
            - cmd(str|list): the command and arguments to run
            - showout(bool): whether to show output or not
            - showerr(bool): whether to show stderr or not
            - block(bool)-=: if false, return immediately, else wait for
                             subprocess
            - checkresult((bool,int)): first element is to do checking,
                                       second is success return code
            - throws(bool): If true, raise CommandException on error
            - remote(bool): When False, even if self.hosts is not None, don't
                            execute remotely.
            - timeout: An optional timeout in seconds to wait for result.  If
                       None, there is no timeout.  Only valid if block is True
            - kwds: keyword arguments which will be passed through to the
                    Popen() constructor

        *Return*
            A ProcessResult object
        """
        if not cmd and not self.cmd:
            raise CommandException("Must have a command to execute")
        if cmd:
            self.cmd = cmd

        if self.host and remote:
            pre = "ssh {}@{} ".format(self.user, self.host)
            self.cmd = pre + self.cmd
        try:
            if isinstance(self.cmd, bytes):
                self.cmd = self.cmd.decode()
        except:
            pass
        if isinstance(self.cmd, str):
            cmd_toks = shlex.split(self.cmd)
        else:
            cmd_toks = self.cmd

        kwds['stdout'] = self.out
        kwds['stderr'] = self.err
        kwds['stdin'] = self.inp

        # Setup our return vals
        output = None
        err = None

        self.logger.debug("cmd_toks = {} type {}".format(cmd_toks, type(cmd_toks)))

        if block:
            proc = Popen(cmd_toks, **kwds)
            if timeout is not None:
                # call in a separate thread
                thr = threading.Thread(target=proc.communicate, name="command")
                endtime = time.time() + timeout
                while time.time() < endtime:
                    if proc.poll() is None:
                        time.sleep(1)
                    else:
                        break
                else:
                    # took too long
                    pass

                output = proc.stdout.read()
                err = proc.stderr.read()
            else:
                (output, err) = proc.communicate()  # FIXME: what about input?
            if showout and output:
                self.logger.info(output)
            if showerr and err:
                self.logger.error(err)
        else:
            proc = Popen(cmd_toks, **kwds)

        meta = {"cmd": self.cmd, "showout": showout, "showerr": showerr,
                "block": block, "checkresult": checkresult, "kwds": kwds}

        self.proc = proc
        result = (proc, output, err, meta)
        proc_res = {"command": self,
                    "outp": output,
                    "error": err,
                    "meta": meta,
                    "logger": LOGGER}

        if checkresult[0]:
            self.check_result(result, checkresult[1], throws=throws)
        return ProcessResult(**proc_res)

    def check_result(self, result, success=0, throws=False):
        """
        Simple checker for the return of a subprocess.

        *args*
            result(tuple)- same type as return from __call__()
            success(int)- the return code that indicates success
        """
        proc, output, err, meta = result
        returnval = proc.poll()
        if returnval == None:
            cmd = meta["cmd"]
            self.logger.warning("Process ({})' is still running".format(cmd))
            return None
        elif proc.returncode != success:
            self.logger.debug("ReturnCode: {0}".format(returnval))
            self.logger.debug("stderr: {0}".format(err))
            self.logger.debug("meta: {}".format(meta))
            self._add_fail(result)
            if throws:
                msg = "Command failed with return code {}"
                msg_f = msg.format(proc.returncode)
                raise CommandException(msg_f)
        return returnval

    def _add_fail(self, result):
        proc, out, err, meta = result
        self.fails[proc.pid] = {"returncode": proc.returncode,
                                "errmsg": err,
                                "meta": meta,
                                "command": self.cmd }

    def make_proxy(self, handler, *args, **kwds):
        """
        Spawns a thread so that we can read the stdout of a long running
        subprocess

        *Args:*
          - handler: the function that will be called in the new thread
          - args: the positional args to be passed to the handler
          - kwds: the keyword args to be passed to the handler

        *Return*
            The thread object which will monitor the stdout of the subprocess

        Usage::

            cmd = Command()
            result = cmd("python some_long_script.py --time=240", block=False)
            printer_thread = cmd.make_proxy(freader, result.proc.stdout)
            printer_thread.start()
            printer_thread.join()  ## only if your parent thread might finish
                                   ## before the thread

        PostCondition-
            When using this function, make sure that after calling start() on
            the thread, that the child thread may not outlive the parent thread.
            This will result in undefined behavior.
        """

        class CommandProxy(threading.Thread):
            def __init__(self, hdl, *args, **kwds):
                super(CommandProxy, self).__init__()
                self.handler = hdl
                self.args = args
                self.kwds = kwds

            def run(self):
                self.handler(*self.args, **self.kwds)

        return CommandProxy(handler, *args, **kwds)

# TODO: put this into a unittest
if __name__ == "__main__":
    cmd = Command("openstack-service status keystone", host="10.35.162.37")
    res = cmd(remote=True)
    out = res.output

    cmd = Command("journalctl -f", host="10.8.29.30")
    res = cmd(block=False, remote=True)
    mon = queue.Queue(maxsize=1)
    rdr_t = cmd.make_proxy(freader, res.proc.stdout, monitor=mon)
    rdr_t.daemon = True
    rdr_t.start()
    import time

    time.sleep(5)
    cmd.proc.terminate()
    while res.proc.poll() is None:
        time.sleep(1)

    res = cmd(block=False, remote=True)
    rdr_t = cmd.make_proxy(freader, res.proc.stdout, monitor=mon)
    rdr_t.daemon = True
    rdr_t.start()
    time.sleep(5)
    mon.put("stop")
    cmd.proc.terminate()
    while res.proc.poll() is None:
        time.sleep(1)
