"""
Keystone module which will be responsible for authentication and base keystone commands.
"""

import os
import logging
from core.logger import glob_logger
from keystoneclient import client

from config import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_keystone_init(type, **kwargs):
    """
    Simple function to retrieve configuration information from
    the global environment.  If no kwargs is passed in, the necessary
    information is retrieved from the environment (ie, as when you source
    keystonerc_admin)
    :param type

    The valid (optional) kwargs are:
      username: -> "OS_USERNAME"
      password: -> "
    :rtype : dict
    :return: A dictionary that can be used for keystone client
    """
    if not kwargs:
        os.environ.update({k: v
                           for k, v in config["credentials"].items()
                           if v is not None})

    creds = {"username": os.environ.get("OS_USERNAME"),
             "password": os.environ.get("OS_PASSWORD"),
             "auth_url": os.environ.get("OS_AUTH_URL"),
             "tenant_name": os.environ.get("OS_TENANT_NAME")}


    # could have used short-cut evaluation, but this seemed more functional
    creds.update({k: v for k, v in kwargs.items()
                  if k in creds and v is not None})
    glob_logger.debug("Using keystone creds: {}".format(creds))

    valid_versions = ("/v2.0", "/v3")
    for v in valid_versions:
        if creds["auth_url"].endswith(v):
            creds["auth_url"] += "/v2.0/"

    return creds


def create_keystone(type, **kwargs):
    """Creates the keystone object

    kwargs:
      user: The username
      password: The password for the user
    """
    creds = get_keystone_init(type, **kwargs)
    creds["debug"] = True

    # Dictionary comprehension equivalent to this:
    # for k,v in kwargs.items():
    #   if k in ("user", "password") and v is not None:
    #     creds[k] = v
    if kwargs:
        valid = {k: v for k, v in kwargs.items()
                 if k in ("username", "password") and v is not None}
        creds.update(valid)

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
