PyProject CookieCutter
######################

This cookiecutter is a template for starting a python project.

Other Flavors
===============

This repo was designed so that other "flavors" of basic python projects could be based off this
intial template.  Since cookiecutter doesn't support multiple templates, it makes sense at this
time to use mercurial branching to facilitate this.

Flavor branches should merge just about everything from the pyproject "up" into their branches but
changes in the flavor branches should never get merged back into this default branch.

Current "Flavors"
-----------------

* Keg


Usage
=====

It's recommended that you install the latest version of cookiecutter at the user level::

    pip install -U cookiecutter --user

Once cookiecutter is installed, you can use this cookiecutter like::

    cd ~/projects
    cookiecutter ~/path/to/this/repo
