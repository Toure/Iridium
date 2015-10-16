__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"

from setuptools import setup
import os


def read(fname):
    """
    Read function is used to provide a simple way to inject a more lengthy description without
    cluttering the setup.py file.
    :param fname: file name which will be used to provide the long_description.
    :return: file dump of provided file.
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="Iridium",
    version="0.1",
    author="Toure Dunnon",
    author_email="toure@redhat.com",
    description="OpenStack functional test framework.",
    license="Apache License 2",
    keywords="openstack test framework",
    url="http://toure.github.io/Iridium/",
    packages=['iridium', 'stack_tests'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache License",
        'Programming Language :: Python :: 3.4',
    ], requires=['python-keystoneclient', 'python-novaclient', 'python-glanceclient',
                 'python-ironicclient', 'python-heatclient', 'python-cinderclient', 'python-swiftclient',
                 'python-neutronclient', 'bugzilla']
)
