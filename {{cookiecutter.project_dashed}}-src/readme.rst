.. default-role:: code

{{cookiecutter.project_name}}'s Readme
######################################

.. image:: https://circleci.com/gh/{{cookiecutter.gh_repo_path}}.svg?&style=shield&circle-token={{cookiecutter.circle_badge_token}}
    :target: https://circleci.com/gh/{{cookiecutter.gh_repo_path}}

.. image:: https://codecov.io/github/{{cookiecutter.gh_repo_path}}/coverage.svg?branch=master&token={{cookiecutter.codecov_badge_token}}
    :target: https://codecov.io/github/{{cookiecutter.gh_repo_path}}?branch=master

Project Setup Checklist
=======================

* `tox`
* setup git hooks from /scripts
* create project on

    * GitHub
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


Database Backup, Restore, and Migration Tests
---------------------------------------------

Backups
~~~~~~~

::

    # Schema and alembic table only
    .../ansible$ ansible-playbook -l prod db-backup.yaml -t sql

    # Complete backup with data
    .../ansible$ ansible-playbook -l prod db-backup.yaml -t full

    # Find the backups on your local machine
    $ ls -lh /tmp/{{cookiecutter.project_namespace}}-*

Files will be generated on the remote server, downloaded to `/tmp`, and then deleted from the
server.


Restore
~~~~~~~

::

    # Restore SQL files - schema, alembic table if it exists, but no data
    $ {{cookiecutter.project_namespace}} db-restore /tmp/{{cookiecutter.project_namespace}}-*.sql
    INFO - {{cookiecutter.project_namespace}}.libs.db - Restoring /tmp/{{cookiecutter.project_namespace}}-schema.sql to None:5433/{{cookiecutter.project_namespace}}
    restore finished

    # Or, full restore with data
    $ {{cookiecutter.project_namespace}} db-restore /tmp/{{cookiecutter.project_namespace}}-full.bak
    INFO - {{cookiecutter.project_namespace}}.libs.db - Restoring /tmp/{{cookiecutter.project_namespace}}-full.bak to None:5433/{{cookiecutter.project_namespace}}
    restore finished


Migration Tests
~~~~~~~~~~~~~~~

By default, when tests run, the db schema is cleared out at the beginning of the test run and
we use SQLAlchemy to create all DB objects before starting the tests.  This is convenient for most
development tests, but won't catch errors in DB migrations because they aren't being applied in
the testing process.

So, we would like a way to run tests on top of a DB that has been prepared by restoring & applying
Alembic migrations.  We have some pytest integration which does most of that work for us::

    $ py.test --db-restore {{cookiecutter.project_namespace}}

That will:

1. Restore the tests database using the files specified by DB_RESTORE_SQL_FPATH (see config example).
2. Run `alembic upgrade head` for the tests database.
3. Skip the DB init Keg would normally do during testing (since we get our schema from the restore + migration).
4. py.test continues as it otherwise would.
