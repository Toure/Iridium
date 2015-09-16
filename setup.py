__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"

from setuptools import setup
import os


def read(fname):
    """

    :param fname:
    :return:
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="Iridium",
    version="0.1",
    author ="Toure Dunnon",
    author_email = "toure@redhat.com",
    description = ("Openstack functional test framework."),
    license = "Apache License 2",
    keywords = "openstack test framework",
    url = "http://toure.github.io/Iridium/",
    packages=['iridium', 'stack_tests'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache License",
        'Programming Language :: Python :: 2.7',
    ],
)