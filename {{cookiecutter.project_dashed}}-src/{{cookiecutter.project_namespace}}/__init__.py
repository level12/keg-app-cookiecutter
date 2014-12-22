from __future__ import absolute_import
from __future__ import unicode_literals
from os import path as osp

_cdir = osp.abspath(osp.dirname(__file__))
VERSION = open(osp.join(_cdir, 'version.txt')).read().strip()
