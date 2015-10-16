__author__ = 'toure'
import abc
from .tracker import Tracker
from bugzilla import Bugzilla


class Bugz(Tracker):

    def __init__(self):
        # TODO auth logic here
        pass

    def create_case(self, **kwargs):
        """
        Create initial bug.
        :param kwargs: product (str),
                       component (str),
                       summary (str),
                       version (str),
                       description (str)
        :return: Returns a new Bug object.
        """
        return Bugzilla.createbug(**kwargs)

    def update_case(self, bug_id, updates):
        """

        :return:
        """
        Bugzilla.update_bugs(ids=bug_id, updates=updates)

    def update_flag(self, id, flags_status):
        """
        Updates the flags associated with a bug report.
        :param idlist:
        :param flags:
        :return:
        """
        Bugzilla.update_flags(id, flags=flags_status)

    def get_component_info(self, product, component, force_refresh=False):
        """
        Get details for a single component.
        :param product:
        :param component:
        :param force_refresh:
        :return:
        """
        Bugzilla.getcomponentdetails(product, component, force_refresh)

    def attach_file(self, idlist, attachment, description, **kwargs):
        """
        Attach a file to the given bug IDs.
        :param idlist:
        :param attachment:
        :param description:
        :param kwargs:
        :return: Returns the ID of the attachment.
        """
        Bugzilla.attachfile(idlist, attachfile=attachment, description=description, **kwargs)
