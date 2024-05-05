#!/usr/bin/python3
"""a fabfile that creates archive"""


from datetime import datetime
from fabric.api import *
import os

env.hosts = ['54.172.227.144', '54.144.151.176']
env.user = ['ubuntu']


def do_pack():
    """
    making an archive on web_static folder
    """

    time = datetime.now()
    archive = 'versions/web_static_' + time.strftime("%Y%m%d%H%M%S") + '.tgz'
    if os.path.isdir("versions") is False:
        local('mkdir versions')
    create = local('tar -cvzf {} web_static'.format(archive))
    if create is not None:
        return archive
    else:
        return None


def do_deploy(archive_path):
    """a function that deploys"""
    if os.path.exists(archive_path):
        try:
            file = archive_path.split('/')[-1]
            file_w_ext = file[:-4]  # file_without_extension
            source_path = '/data/web_static/releases/'
            put(archive_path, '/tmp/')
            run('mkdir -p {}{}/'.format(source_path, file_w_ext))
            run('tar -xzf /tmp/{} -C {}{}/'.format(file, source_path,
                file_w_ext))
            run('rm /tmp/{}'.format(file))
            run('mv {0}{1}/web_static/* {0}{1}/'.format(source_path,
                file_w_ext))
            run('rm -rf {}{}/web_static'.format(source_path, file_w_ext))
            run('rm -rf /data/web_static/current')
            run('ln -s {}{}/ /data/web_static/current'.format(source_path,
                file_w_ext))
            return True
        except:
            return False
    else:
        return False


def deploy():
    """creates and distributes an archive to server"""
    archive_path = do_pack()
    if archive_path:
        return do_deploy(archive_path)
    return False
