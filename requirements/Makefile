# Reference: https://jamescooke.info/a-successful-pip-tools-workflow-for-managing-python-package-requirements.html
# I (RLS) don't really like this makefile, but it works for now.

objects = $(wildcard *.in)
outputs := $(objects:.in=.txt)


.PHONY: all check clean

all: $(outputs)

%.txt: %.in
	pip-compile -v --output-file $@ $<

# Dependency chain
dev.txt: common.txt

