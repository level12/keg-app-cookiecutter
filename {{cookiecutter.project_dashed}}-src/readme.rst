.. default-role:: code

{{cookiecutter.project_name}}'s Readme
######################################

Project Setup Checklist
=======================

* `wheelhouse build`
* `tox`
* setup git hooks from /scripts
* create project on

    * GitHub
    * Coveralls: then add repo token to tox.ini
    * Shippable

        * your account has to have an integration with our dockerhub account (creds in LP)
        * pull image from: level12/shippable-python
        * HUB: the dockerhub integration you setup in your account

    * Appveyor
    * Sentry

* Setup Slack integrations for

    * Shippable
    * Appveyor
    * Sentry

* Git init, commit, push
* Verify

    ** CI builds pass
    ** Coverage is pushed
    ** Verify deliberate exception (/exception) shows up in Sentry
    ** Failed builds show up in Slack

* Update this readme


