.. default-role:: code

Keg CookieCutter
################

Preparation
===========

You will need to do the following before you use this cookiecutter:

* Create a repo for the project on GitHub
* CircleCI

  * Projects -> Add Project
  * Project Settings -> API Permissions -> Create Status Token
  * Add token as `circle_badge_token` in `cookicutter.json`

* Codecov

  * Add new repository
  * Add "Upload Token" as `codecov_api_token` in `cookicutter.json`
  * Settings -> Badge -> copy token to `codecov_badge_token` in `cookicutter.json`

* Update all values in `cookiecutter.json`


Usage
=====

It's recommended that you install the latest version of cookiecutter at the user level::

    pip install -U cookiecutter --user

Once cookiecutter is installed, you can use this cookiecutter like::

    cookiecutter <KEG-CC-DIR> --no-input --overwrite-if-exists -o <CREATE-PROJ-IN-DIR>

Development
===========

* Dependencies: managed with pipenv
* Readme preview: `restview readme.rst`

In order to QA the output of this project, I run the cookiecutter and apply it to
`KegDemo <https://github.com/level12/keg-demo/>`_ (checked out locally)::

    # One-time run
    ~/projects/keg-app-cc-src$ ./cookie-run-demo

    # Watch cookiecutter files and run when they chanve
    ~/projects/keg-app-cc-src$ ./cookie-watch

These have a hard coded path in them for my (RLS) project's directory.  If someone else wants to
hack on this project, just change the bash scripts to use environment settings to change path
configurations.
