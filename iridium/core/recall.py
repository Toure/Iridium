

class Recall(object):
    """ Recall will act as the remote log inspector which will retrieve logs of
    a certain signature and perform basic analysis.
    """
    def load(self, filename):
        """
        load will analysis class, method information, and make them available in the shell.
        :return:
        """
        pass

    def display(self):
        """
        display will print an account of transactions which were recorded.
        :return:
        """
        pass

    def lintr(self, filename):
        """
        lintr will check to make sure file format is correct.
        :param filename:
        :return:
        """
        pass
