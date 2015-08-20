__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"

"""
Keystone module which will be responsible for authentication and base keystone commands.
"""

import os
import logging

from keystoneclient import client

from iridium.core.logger import glob_logger
from config import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_keystone_init(version=None, **kwargs):
    """
    Simple function to retrieve configuration information from
    the global environment, if no kwargs is passed in, the necessary
    information is retrieved from the environment (ie, as when you source
    keystonerc_admin)
    :param version sets the version of ReST protocol to implement. (ie. "/v2.0", "/v3")
    kwargs:
       auth_url location to contact the keystone server.
       username usename to authenticate against keystone server.
       password password for username.
       project_name (version 3) or tenant_name (version 2) project credential for user.
       user_domain_name domain for username only valid for version 3 protocol.
       project_domain_name domain for specified project onnly valid for version 3.
    :rtype : dict
    :return: A dictionary that can be used with keystone client.
    """
    if not kwargs and version is None:
        glob_logger.info("Reading Environmental variables..")
        creds = {"username": os.environ.get("OS_USERNAME"),
                 "password": os.environ.get("OS_PASSWORD"),
                 "auth_url": os.environ.get("OS_AUTH_URL"),
                 "tenant_name": os.environ.get("OS_TENANT_NAME")}

    # Here we use built-in config file.
    if not kwargs and version is not None:
        creds = {k: v for k, v in config.auth_info[version].items()
                 if v is not None}
    # Else we allow override of built-in dictionary.
    elif kwargs:
        creds = {k: v for k, v in kwargs.items()
                 if v is not None}

    glob_logger.debug("Using keystone creds: {}".format(creds))

    return creds


def create_keystone(version, **kwargs):
    """Creates the keystone object

    :param version of protocol to communicate with Keystone over, the two options are
    v2 or v3 which are translated into /v2.0 and /v3 respectfully.

    kwargs:
       auth_url location to contact the keystone server.
       username usename to authenticate against keystone server.
       password password for username.
       project_name (version 3) or tenant_name (version 2) project credential for user.
       user_domain_name domain for username only valid for version 3 protocol.
       project_domain_name domain for specified project onnly valid for version 3.

    """
    creds = get_keystone_init(version, **kwargs)

    # TODO additional checks for valid object creation.

    keystone = client.Client(**creds)

    return keystone


def get_endpoint(key_cl, name, end_type="publicURL"):
    return key_cl.service_catalog.url_for(service_type=name,
                                          endpoint_type=end_type)


def create_tenant(key_cl, name, **kwargs):
    tenant = key_cl.tenants.create(name, **kwargs)
    return tenant


def create_user(key_cl, tenant_id, name, **kwargs):
    user = key_cl.users.create(name, tenant_id=tenant_id, **kwargs)
    return user
