__author__ = 'toure'

import jenkins


def connect(url: str, username: str, password: str, timeout: int=None) -> object:
    """
    Jenkins Connect will attach to the specified server and return a session
    object.
    :param url: server ip or hostname with specified port. ei. localhost:8080, str
    :param username: users name for the corresponding project, str
    :param password: password for user, str
    :param timeout: Server connection timeout in secs (default: not set), int
    :return: connection object.
    """
    server = jenkins.Jenkins(url, username=username, password=password, timeout=timeout)

    return server


def get_job_name(name: str) -> object:
    """
    That is roughly an identity method which can be used to quickly verify a job exist or is accessible
    without causing too much stress on the server side.
    :param name: Job name, str
    :return: Name of job or None
    """
    pass


def debug_job_info(job_name):
    """
    Print out job info in more readable format.

    :param job_name:
    :return:
    """
    pass


def get_build_info(name, number, depth=0):
    """

    :param name:
    :param number:
    :param depth:
    :return:
    """
    pass


def get_node_info(name, depth=0):
    """
    Get node information dictionary
    :param name: Node name, str
    :param depth: JSON depth, int
    :return: Dictionary of node info, dict
    """
    pass


def node_exists(name: str) -> bool:
    """

    :param name:
    :return:
    """
    pass


def delete_node(name: str) -> bool:
    """

    :param name:
    :return:
    """
    pass


def create_node(name: str, numExecutors: int=2, nodeDescription: str=None, remoteFS: str='/var/lib/jenkins',
                labels: str=None, exclusive: bool=False, launcher: object='hudson.slaves.CommandLauncher',
                launcher_params: dict={}) -> bool:
    """

    :param name:
    :param numExecutors:
    :param nodeDescription:
    :param remoteFS:
    :param labels:
    :param exclusive:
    :param launcher:
    :param launcher_params:
    :return:
    """
    pass


def get_node_config(name: str) -> dict:
    """

    :param name:
    :return:
    """
    pass
