import pathlib

from setuptools import setup

cdir = pathlib.Path(__file__).parent
README = cdir.joinpath('readme.rst').read_text('utf-8')
CHANGELOG = cdir.joinpath('changelog.rst').read_text('utf-8')

VERSION_SRC = cdir.joinpath('{{cookiecutter.project_pymod}}', 'version.py').read_text('utf-8')
version_globals = {}
exec(VERSION_SRC, version_globals)


setup(
    name='{{cookiecutter.project_class}}',
    version=version_globals['VERSION'],
    description='<short description>',
    author='{{cookiecutter.developer_name}}',
    author_email='{{cookiecutter.developer_email}}',
    url='',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    packages=['{{cookiecutter.project_pymod}}'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # use this for libraries; or
        # use requirements folder/files for apps
    ],
    entry_points='''
        [console_scripts]
        {{cookiecutter.project_cli_bin}} = {{cookiecutter.project_pymod}}.cli:cli_entry
    ''',
)
