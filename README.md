Swiss Army Knife
================

[![Build Status](http://img.shields.io/travis/aureooms/sak.svg?style=flat)](https://travis-ci.org/aureooms/sak)
[![Scrutinizer Code Quality](http://img.shields.io/scrutinizer/g/aureooms/sak.svg?style=flat)](https://scrutinizer-ci.com/g/aureooms/sak/?branch=master)
[![Code Coverage](http://img.shields.io/scrutinizer/coverage/g/aureooms/sak.svg?style=flat)](https://scrutinizer-ci.com/g/aureooms/sak/?branch=master)
[![GitHub issues](http://img.shields.io/github/issues/aureooms/sak.svg?style=flat)](https://github.com/aureooms/sak/issues)

***sak*** is a module, submodule and action based tool

usage :

	$ <module> <submodule>* <action> <*args> <**kwargs>

will execute function `action` from file `sak/module(/submodule)*.py` with
`*args` and `**kwargs`.

`**kwargs` are POSIX-like options and flags, to set a flag to a falsy
value just prepend `no` in front of the flag name. For example `--prompt` sets
`kwargs["prompt"] = True` while `--noprompt` sets `kwargs["prompt"]` = False.

Examples,

  - retrieve info on git repos located under *.* and *workspace*

		$ git info . workspace

  - list actions available in module *site*

		$ help info site

All modules, submodules and actions support shortcuts,

  - hash remote ftp site:

		$ si h

  - concat js files in js/src and put output in js/min

		$ j b js

All actions support kwargs,

  - clone all your github repos:

		$ gth d --username aureooms --noprompt

All actions support shrinking kwargs,

  - clone all your github repos:

		$ gth d -u aureooms --nopro

currently available modules :

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
