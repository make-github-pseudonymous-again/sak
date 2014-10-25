Swiss Army KnifE
================

[![Build Status](https://travis-ci.org/aureooms/sake.svg)](https://travis-ci.org/aureooms/sake)
[![Code Coverage](https://scrutinizer-ci.com/g/aureooms/sake/badges/coverage.png?b=master)](https://scrutinizer-ci.com/g/aureooms/sake/?branch=master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/aureooms/sake/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/aureooms/sake/?branch=master)
[![GitHub issues](http://img.shields.io/github/issues/aureooms/sake.svg)](https://github.com/aureooms/sake/issues)

***sake*** is a module based tool


usage :

	$ <module> <action> <*args> <**kwargs>


where `**kwargs` are POSIX-like options and flags, to set a flag to a falsy value just prepend `no` in front of the flag name. For example `--prompt` sets `kwargs["prompt"] = True` while `--noprompt` sets `kwargs["prompt"]` = False.


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
  - sake
  - site
  - sitec
  - sty
  - sublime
  - tex
  - text
  - train
  - update
  - url




examples :

  - retrieve info on git repos located under *.* and *workspace*

		$ git info . workspace

  - list actions available in module *site*

		$ help info site


*All modules and action now support shortcuts, example :*


  - hash remote ftp site:

    $ si h

  - concat js files in js/src and put output in js/min

    $ j b js


*All modules and action now support kwargs, example :*


  - clone all your github repos:

    $ gth d --username aureooms --noprompt

