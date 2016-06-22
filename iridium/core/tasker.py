"""
Tasker will take a command from that call it will inspect the registered list of functions / methods and
place it into a asynchronous task, this will allow users to spawn multiple functions and not block the terminal.
"""

import asyncio


class Tasker(object):
    def lookup(self, task_name: str) -> list:
        """
        lookup will be responsible for listing current task which are running in the
        background.
        :return: list of task
        """
        pass

    def launcher(self, task_name: str, task_args: str) -> object:
        """
        launcher will take the given task name to be loaded asynchronously.
        :return: async object
        """
        pass

    def status(self, task_name: str) -> str:
        """
        status will return information for the given task name.
        :return: string.
        """
        pass
