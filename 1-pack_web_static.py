#!/usr/bin/python3
"""a fabfile that creates archive"""
# from fabric.api import *
# import time


# def do_pack():
#   """the function to create the archive"""
#  local("mkdir /versions")
# name_of_archive = "web_static_{}.tgz".format(time.strftime("%Y%m%d%H%M%S",
# time.localtime))
# create = local(f"tar -cvzf versions/{name_of_archive} web_static")
# if create is not None:
#   return name_of_archive
# else:
#   return None

from datetime import datetime
from fabric.api import *


def do_pack():
    """
    making an archive on web_static folder
    """

    time = datetime.now()
    archive = 'web_static_' + time.strftime("%Y%m%d%H%M%S") + '.' + 'tgz'
    local('mkdir -p versions')
    create = local('tar -cvzf versions/{} web_static'.format(archive))
    if create is not None:
        return archive
    else:
        return None
