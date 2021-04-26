# sak : Swiss Army Knife

[![PyPI release](https://img.shields.io/pypi/v/sak.svg?style=flat)](https://pypi.python.org/pypi/sak)
[![Build Status](http://img.shields.io/travis/make-github-pseudonymous-again/sak.svg?style=flat)](https://travis-ci.com/make-github-pseudonymous-again/sak)
[![Code Climate](http://img.shields.io/codeclimate/github/make-github-pseudonymous-again/sak.svg?style=flat)](https://codeclimate.com/github/make-github-pseudonymous-again/sak)
[![Scrutinizer Code Quality](http://img.shields.io/scrutinizer/g/make-github-pseudonymous-again/sak.svg?style=flat)](https://scrutinizer-ci.com/g/make-github-pseudonymous-again/sak/?branch=main)
[![Code Coverage](http://img.shields.io/scrutinizer/coverage/g/make-github-pseudonymous-again/sak.svg?style=flat)](https://scrutinizer-ci.com/g/make-github-pseudonymous-again/sak/?branch=main)
[![GitHub issues](http://img.shields.io/github/issues/make-github-pseudonymous-again/sak.svg?style=flat)](https://github.com/make-github-pseudonymous-again/sak/issues)

**sak** is a module, submodule and function based tool

install :

	pip3 install sak

usage :

	$ <module> <submodule>* <function> <*args> <**kwargs>

will execute function `<function>` from file `sak/module(/submodule)*.py` with
`*args` and `**kwargs`.

`**kwargs` are POSIX-like options and flags, to set a flag to a falsy
value just prepend `no` in front of the flag name. For example `--prompt` sets
`kwargs["prompt"] = True` while `--noprompt` sets `kwargs["prompt"]` = False.

Examples,

  - retrieve info on git repos located under *.* and *workspace*

		$ git info . workspace

  - list functions and submodules available in module *site*

		$ help info site

All modules, submodules and functions support shortcuts,

  - hash remote ftp site:

		$ si h

  - concat js files in js/src and put output in js/min

		$ j b js

All functions support kwargs,

  - clone all your github repos:

		$ gth d --username make-github-pseudonymous-again --noprompt

All functions support shrinking kwargs,

  - clone all your github repos:

		$ gth d -u make-github-pseudonymous-again --nopro

Currently available modules:

  - bitbucket
  - clipboard
  - codeclimate
  - config
  - cpm
  - css
  - date
  - git
  - github
  - gmail
  - google
  - help
  - img
  - js
  - navigator
  - npm
  - orddir
  - sak
  - site
  - sty
  - sublime
  - tex
  - text
  - train
  - update
  - url
