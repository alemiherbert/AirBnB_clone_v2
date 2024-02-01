#!/usr/bin/python3
""" Fabric script that generates a .tgz archive from
the contents of the web_static folder of your AirBnB Clone repo,
using the function do_pack.
"""

import os.path
from fabric.api import local
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
