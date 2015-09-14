__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"

from libs.trackers import bugz
from libs.trackers import launchy
from importlib import import_module


class TrackerBase(object):
    @staticmethod
    def import_mod():
        """
        Import mod will return an initialized import path from the specified module name.

        :param module_name: tracker module name of interest (str).
        :return: import object of requested module name.
        """
        return import_module("libs.trackers.tracker")


class Tracker(object):
    """
    Tracker will serve as an abstraction layer to provide a unified interface to bugzilla and launchpad.
    """

    def __init__(self, platform):
        """

        :param platform: dictionary key which will be used in the factory to return the correct
                         class object.
                         Valid keys: bz = bugzilla, lp = launchpad
        :return: class object
        """
        self.tracker = {'bz': 'bugzilla', 'lp': 'launchpad'}
        self.platform = platform

    @property
    def factory(self):
        """

        :return: tracker class instance.
        """
        if self.tracker[self.platform] == 'bugzilla':
            return bugz.Bugz()
        elif self.tracker[self.platform] == 'launchpad':
            return launchy.Launchz()
