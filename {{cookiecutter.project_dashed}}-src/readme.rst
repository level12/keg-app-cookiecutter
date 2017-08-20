.. default-role:: code

{{cookiecutter.project_name}}'s Readme
######################################

.. image:: https://circleci.com/gh/{{cookiecutter.gh_repo_path}}.svg?&style=shield&circle-token={{cookiecutter.circle_badge_token}}
    :target: https://circleci.com/gh/{{cookiecutter.gh_repo_path}}

.. image:: https://codecov.io/github/{{cookiecutter.gh_repo_path}}/coverage.svg?branch=master&token={{cookiecutter.codecov_badge_token}}
    :target: https://codecov.io/github/{{cookiecutter.gh_repo_path}}?branch=master

Project Setup Checklist
=======================

* `wheelhouse build`
* `tox`
* setup git hooks from /scripts
* create project on

    * GitHub
    * CodeCov: then add repo token to tox.ini
    * CircleCI
    * Appveyor?
    * Sentry

* Setup Slack integrations for

    * CircleCI
    * Appveyor
    * Sentry

* Git init, commit, push
* Verify

    ** CI builds pass
    ** Coverage is pushed
    ** Verify deliberate exception (/exception) shows up in Sentry
    ** Failed builds show up in Slack

* Update this readme


Celery
=================

The celery worker can be run with::

    ./scripts/celery-worker

View your queues and stuff using flower (`pip install flower`)::

    celery flower --app racebetter.celery.worker

Purging the queues::

    ./scripts/celery-purge
