Swiss Army KnifE
================

[![Build Status](https://drone.io/github.com/aureooms/sake/status.png)](https://drone.io/github.com/aureooms/sake/latest)
[![Code Health](https://landscape.io/github/aureooms/sake/master/landscape.png)](https://landscape.io/github/aureooms/sake/master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/aureooms/sake/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/aureooms/sake/?branch=master)

***sake*** is a module based tool


usage :

	$ <module> <action> <*arg>


currently available modules :

  - bitbucket
  - codeclimate
  - config
  - css
  - git
  - github
  - gmail
  - google
  - help
  - img
  - js
  - lib
  - os
  - site
  - sty
  - sublime
  - sys
  - tex
  - text



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

