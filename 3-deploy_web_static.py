#!/usr/bin/python3
""" Fabric script that distributes an archive to your web servers,
using the function deploy.
"""

import os.path
from fabric.api import env, put, run, local
from datetime import datetime


def do_pack():
    """Function to compress files"""
    date = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(date.year,
                                                         date.month,
                                                         date.day,
                                                         date.hour,
                                                         date.minute,
                                                         date.second)
    if not os.path.exists("versions") and local("mkdir -p versions").failed:
        return
    if local("tar -cvzf {} web_static".format(file)).failed:
        return
    return file


def do_deploy(archive_path):
    """Distriputes an archive to the web servers

    Args:
        archive_path (str): Path to the archive
    Returns:
        True on success, False otherwise
    """

    if not os.path.isfile(archive_path):
        return False

    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed:
        return False

    if run("rm -rf /data/web_static/releases/{}/".format(name)).failed:
        return False

    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed:
        return False

    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
           .format(file, name)).failed:
        return False

    if run("rm /tmp/{}".format(file)).failed:
        return False

    if run("mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/"
           .format(name, name)).failed:
        return False

    if run("rm -rf /data/web_static/releases/{}/web_static"
            .format(name)).failed:
        return False

    if run("rm -rf /data/web_static/current").failed:
        return False

    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
           .format(name)).failed:
        return False
    return True


def deploy():
    """Creates and distributes an archive to the web servers
    Returns:
        True on success, False otherwise
    """
    path = do_pack()
    if not path:
        return False
    return do_deploy(path)
