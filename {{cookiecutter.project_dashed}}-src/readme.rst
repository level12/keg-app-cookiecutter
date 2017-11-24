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
    ** Failed CI builds show up in a Slack channel

* Update this readme


Celery
=================

The celery worker can be run with::

    ./scripts/celery-worker

View your queues and stuff using flower (`pip install flower`)::

    celery flower --app racebetter.celery.worker

Purging the queues::

    ./scripts/celery-purge

Deploy
==================

All commands are given for beta, change to `-l prod` for production.

A user with sudo permissions on the server must run the provision::

    ansible-playbook -l beta provision.yaml

You can verify the provision by browsing to (something like)::

    https://yourapp-beta.level12.biz

Assuming that is successful, you should then deploy::

    # For the first run, create the database from the model
    ansible-playbook -l beta deploy.yaml --extra-vars=first_run=true

    # Subsequent deploys will use Alembic migrations
    ansible-playbook -l beta deploy.yaml

You can verify the deploy by:

* Browsing to: https://yourapp-beta.level12.biz/ping-db
* Browsing to: https://yourapp-beta.level12.biz/exception-test

  * Verify this shows up in Sentry

* Verify the app's logging messages through Celery, which cron should be running once a minute.
  You can run manually with: `{{cookiecutter.project_namespace}} log` and `{{cookiecutter.project_namespace}} celery ping`.

  * Look on the server in ~/syslogs/app.log for the app's log messages
  * Look at logzio, the messages should have shipped there as well through rsyslog

* Setup an alert in Logz.io for the "ping-pong" log message to arrive 5 times in 10 minutes.  This
  ensures both that Celery is running and that log messages are shipping correctly.

