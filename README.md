soyprice
========

[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/limiear/soyprice?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![License](https://pypip.in/license/soyprice/badge.svg)](https://pypi.python.org/pypi/soyprice/) [![Downloads](https://pypip.in/download/soyprice/badge.svg)](https://pypi.python.org/pypi/soyprice/) [![Build Status](https://travis-ci.org/limiear/soyprice.svg?branch=master)](https://travis-ci.org/limiear/soyprice) [![Coverage Status](https://coveralls.io/repos/limiear/soyprice/badge.png)](https://coveralls.io/r/limiear/soyprice) [![Code Health](https://landscape.io/github/limiear/soyprice/master/landscape.png)](https://landscape.io/github/limiear/soyprice/master) [![PyPI version](https://badge.fury.io/py/soyprice.svg)](http://badge.fury.io/py/soyprice)
[![Supported Python versions](https://pypip.in/py_versions/soyprice/badge.svg)](https://pypi.python.org/pypi/soyprice/) [![Stories in Ready](https://badge.waffle.io/limiear/soyprice.png?label=ready&title=Ready)](https://waffle.io/limiear/soyprice)

A python script to estimate the soy price in and show it in the twitter timeline.


Requirements
============

If you want to use this script on any GNU/Linux or OSX system you just need to execute:

    $ pip install soyprice

If you want to improve this script, you should download the [github repository](https://github.com/limiear/soyprice) and execute:

    $ make virtualenv deploy

On Ubuntu Desktop there are some other libraries not installed by default (zlibc libssl libbz2-dev libxml2-dev libxslt1-dev python-gevent libpng12-dev) which may need to be installed to use these script. Use the next command to automate the installation of the additional C libraries:

    $ make ubuntu virtualenv deploy


Testing
=======

To test all the project you should use the command:

    $ make test

If you want to help us or report an issue join to us through the [Github issue tracker](https://github.com/limiear/soyprice/issues).


Example
=======

To run the bot you should execute:

    $ python -c "import soyprice.bot"


About
=====

This software is developed by [LIMIE](http://www.limie.com.ar). You can contact us to [limie.ar@gmail.com](mailto:limie.ar@gmail.com).
