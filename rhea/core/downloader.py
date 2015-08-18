__author__ = "Sean Toner"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "stoner@redhat.com"
__status__ = "Alpha"

try:
    from urllib.request import urlopen
    from urllib.parse import urlparse as urlparse
except ImportError:
    from urllib2 import urlopen
    from urlparse import urlparse

import os

from rhea.core import commander
from rhea.core.logger import glob_logger
from rhea.core.commander import Result


class Downloader(object):
    """
    This is a class to help with downloading and installing various artifacts.
    These artifacts may be from the web, an ftp server, or even scp'ed or on a
    """
    pip_path = "https://raw.github.com/pypa/pip/master/contrib/get-pip.py"

    def __init__(self, executor=None, osinfo=None):
        if not executor:
            self.executor = commander.Command()
        else:
            self.executor = executor
        self.logger = self.executor.logger
        self.osinfo = osinfo

    @staticmethod
    def download_url(urlpath, output_dir=".", binary=False):
        try:
            thing = urlopen(urlpath)
        except Exception as e:
            print(str(e))
            return

        parsed = urlparse(urlpath)
        filename = os.path.basename(parsed.path)
        writemod = "wb" if binary else "w"

        fobj = thing.read()
        if output_dir != ".":
            if not os.path.exists(output_dir):
                glob_logger.error("{0} does not exist".format(output_dir))
                glob_logger.error("Writing file to {0}".format(os.getcwd()))
            else:
                filename = "/".join([output_dir,filename])
        with open(filename, writemod) as downloaded:
            try:
                downloaded.write(fobj)
            except TypeError:
                with open(filename, "wb") as downloaded:
                    downloaded.write(fobj)
        return os.path.exists(filename)

    def is_pip_installed(self):
        res = self.executor("pip --help")
        return not res.proc.returncode

    def install_pip(self, pipfile="get-pip.py"):
        if not self.download_url(Downloader.pip_path):
            err = "Could not download {0}".format(pipfile)
            self.logger.error(err)
            return Result(-1, err)

        cmd = "python {0}".format(pipfile)
        self.executor(cmd, checkresult=(True,0))

    def install_python_lib(self, scriptname):
        """
        This will install distutils based python scripts
        that use setup.py
        """
        ## FIXME:  we may want to use a different python
        ## for example python3, or a virtualenv python
        cmd = "{0} {1} install".format(self.python, scriptname)
        res = self.executor(cmd, checkresult=(True,0))

    def check_python_devel(self):
        try:
            from distutils import sysconfig as ds
            vars = ds.get_config_vars()
            if vars.has_key("INCLUDEPY"):
                if "Python.h" in os.listdir(vars["INCLUDEPY"]):
                    return True
            return False
        except ImportError:
            le = self.logger.error
            le("Can not determine if python devel libs installed")

    def pip_cmd(self, pkgnames, cmd="install", pip_args=None):
        if pip_args is None:
            pip_args = []

        try:
            from setuptools import find_packages
            import pip
        except ImportError as ie:
            glob_logger.error(ie.msg)

        pip_args.append(cmd)
        if isinstance(pkgnames, str):
            pip_args.append(pkgnames)
        else:
            ## concatenate the lists
            pip_args += [pkg for pkg in pkgnames]

        msg = "Running pip " + " ".join(pip_args)
        glob_logger.info(msg)
        try:
            import pip
            pip.main(initial_args=pip_args)
        except ImportError as ie:
            self.logger.error("Unable to import pip")
            raise ie


if __name__ == "__main__":
    r = Downloader.download_url("http://cloud.centos.org/centos/6/images/CentOS-6-x86_64-GenericCloud.qcow2", output_dir="/tmp")
    print(r)