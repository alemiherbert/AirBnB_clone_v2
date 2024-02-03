#!/usr/bin/python3
"""Fabric script that deletes out-of-date archives"""

from fabric.api import local, run, env

env.hosts = ["54.173.41.135", "18.208.120.167"]


def do_clean(number=0):
    """Cleans up old versions of the web static files."""

    number = int(number) + 1 if number else 2
    local('cd versions ; ls -t | tail -n +{} | xargs rm -rf'.format(number))
    path = '/data/web_static/releases'
    run('cd {} ; ls -t | tail -n +{} | xargs rm -rf'.format(path, number))
