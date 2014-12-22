from __future__ import print_function
from os import path as osp

_cdir = osp.abspath(osp.dirname(__file__))
VERSION = open(osp.join(_cdir, 'version.txt')).read().strip()


def cli_entry():
    print('Hello World!')
    print('From {{cookiecutter.project_name}} version {}'.format(VERSION))
