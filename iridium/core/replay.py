"""
This module will read in output files and replay.
"""
import pickle


class Replay(object):
    """
    Replay will allow users to import a iridium history file and
    replay instructions at a set interval.
    """

    def importer(self):
        pass

    def _stepper(self):
        pass

    def packer(self, func, *args, **kwargs):
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
