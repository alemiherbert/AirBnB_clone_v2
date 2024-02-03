#!/usr/bin/python3
""" Fabric script that distributes an archive to your web servers,
using the function do_deploy.
"""

import os.path
from fabric.api import env, put, run

env.hosts = ["54.173.41.135", "18.208.120.167"]


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
