import os
import os.path as osp

from setuptools import setup

cdir = os.path.abspath(os.path.dirname(__file__))
README = open(osp.join(cdir, 'readme.rst')).read()
CHANGELOG = open(osp.join(cdir, 'changelog.rst')).read()
VERSION = open(osp.join(cdir, '{{cookiecutter.project_namespace}}', 'version.txt')).read().strip()

setup(
    name='{{cookiecutter.project_class}}',
    version=VERSION,
    description='<short description>',
    author='{{cookiecutter.developer_name}}',
    author_email='{{cookiecutter.developer_email}}',
    url='',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
    ],
    packages=['{{cookiecutter.project_namespace}}'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # use this for libraries; or
        # use requirements folder/files for apps
    ],
    entry_points='''
        [console_scripts]
        {{cookiecutter.project_namespace}} = {{cookiecutter.project_namespace}}.cli:cli_entry
    ''',
)
