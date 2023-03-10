.. default-role:: code

Keg CookieCutter
################

.. image:: https://circleci.com/gh/level12/keg-app-cookiecutter.svg?style=svg&circle-token=5e00606556338515932f8552ad44f0f2fdbe14ea
    :target: https://circleci.com/gh/level12/keg-app-cookiecutter

Also see `KegDemo's <https://github.com/level12/keg-demo/>`_ badges/status.


Usage
=====

Per Project Customization
-------------------------

Setup a `.cookiecutterrc <https://cookiecutter.readthedocs.io/en/1.7.3/advanced/user_config.html>`_
config file with a `default_context` section.  Example:

::

  default_context:
    developer_name: Randy Syring
    developer_email: randy.syring@level12.io
    developer_password: password
    project_name: Green Blue EPR
    project_ident: epr
    project_class: GBEPR
    gh_repo_org: level12
    gh_repo_name: gb-epr
    database_host: circus
    onepass_secrets_vault: client-gb-epr-deploy
    circle_badge_token: [fill in]
    codecov_graphing_token: [fill in]
    codecov_upload_token: [fill in]
    celery_alive_key_beta: [fill in]
    celery_alive_key_prod: [fill in]

You should **typically NOT update cookiecutter.json** as it's checked into this project and has
useful defaults.  You should change the `.json` file if you alter the cookiecutter itself.


Per Project Setup
-----------------

You will need to do the following before you use this cookiecutter:

* Create a repo for the project on GitHub
* CircleCI

  * Projects -> Search for GH Repo -> Set Up Project

    * You may have to commit a temporary circleci config file so a build runs and you can get to
      the next screen.

  * Project Settings -> API Permissions -> Add API Token -> "Status" & "readme status"
  * Add token as `circle_badge_token` in your `default_context`

* Codecov

  * Add new repository -> Settings and copy to `default_context`:
  * Copy "Graphing Token" to `codecov_graphing_token`
  * Copy "Upload Token" as `codecov_upload_token`

* Cronitor

  * Create new Celery Alive monitors for beta & prod by copying one of the existing monitors
  * Copy monitor keys to `default_context`

* Check the `.json` file for new entries and update your `default_context` as needed
* Update any other values in `default_context` as applicable.


Create Project
--------------

It's recommended that you install the latest version of cookiecutter at the user level::

    pip install -U cookiecutter --user

Once cookiecutter is installed, you can use this cookiecutter like::

    cookiecutter <KEG-CC-DIR> --no-input --overwrite-if-exists -o <CREATE-PROJ-IN-DIR>


Icons
=====

Webgrid, by default, use Font-Awesome 5 Free for fonts. The font is loaded by the template
from the Font-Awesome server. We do not ship those files with this repo for licensing reasons.

Development
===========

* Dependencies: managed with pip-tools
* Readme preview: `restview readme.rst`

In order to QA the output of this project, I run the cookiecutter and apply it to
`KegDemo <https://github.com/level12/keg-demo/>`_ (checked out locally)::

    # One-time run
    ~/projects/keg-app-cc-src$ ./cookie-run-demo

    # Watch cookiecutter files and run when they change
    ~/projects/keg-app-cc-src$ ./cookie-watch

These have a hard coded path in them for my (RLS) project's directory.  If someone else wants to
hack on this project, just change the bash scripts to use environment settings to change path
configurations.
