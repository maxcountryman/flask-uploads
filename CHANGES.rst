Changelog
=========

unreleased
----------
- improve coverage


0.5.0
-----
- improve documentation of example app
- document surprising `autoserve` feature
- issue a warning when using `autoserve` without explicit configuration


0.4.0
-----
- add type annotations
- drop support for Python 2 and Python 3.5
  (`#8 <https://github.com/jugmac00/flask-reuploaded/issues/8>`_)
- deprecate `patch_request_class`
  (`#43 <https://github.com/jugmac00/flask-reuploaded/issues/43>`_)
- use a `src` directory for source code
  (`#21 <https://github.com/jugmac00/flask-reuploaded/issues/21>`_)
- add tox env for check-python-versions
  (`#20 <https://github.com/jugmac00/flask-reuploaded/issues/20>`_)
- add flake8-bugbear
- add short contribution guide
  (`#6 <https://github.com/jugmac00/flask-reuploaded/issues/6>`_)
- add `getting started`
  (`#59 <https://github.com/jugmac00/flask-reuploaded/issues/59>`_)
- delete broken example and add minimal example to README
  (`#15 <https://github.com/jugmac00/flask-reuploaded/issues/15>`_)
- add support for Python 3.9
- use gh actions instead of Travis CI


0.3.2
-----
- documentation update
  (`#5 <https://github.com/jugmac00/flask-reuploaded/issues/5>`_)

  * update docs/index.rst
  * use blue ReadTheDocs theme
  * update sphinx configuration
  * add documentation link to `setup.py`, so it shows on PyPi
  * add note about documentation in the README file
  * delete old theme files
- configure `isort` to force single line imports


0.3.1
-----
- add badges to README
  (`# 31 <https://github.com/jugmac00/flask-reuploaded/issues/31>`_)
- add migration guide from `Flask-Uploads` to `Flask-Reuploaded`
  (`#11 <https://github.com/jugmac00/flask-reuploaded/issues/11>`_)
- add packaging guide
  (`#28 <https://github.com/jugmac00/flask-reuploaded/issues/28>`_)
- update installation instruction in README


0.3
---

Besides including four years of unreleased changes from the original
package, most notable the fix for the Werkzeug API change, the
following changes happened since forking the original package.

- rename package from `Flask-Uploads` to `Flask-Reuploaded`
  (`#10 <https://github.com/jugmac00/flask-reuploaded/issues/10>`_)
- update `setup.py`
  (`#12 <https://github.com/jugmac00/flask-reuploaded/issues/12>`_)
- start using pre-commit.com
  (`#4 <https://github.com/jugmac00/flask-reuploaded/issues/4>`_)
- update README
  (`#14 <https://github.com/jugmac00/flask-reuploaded/issues/14>`_)
- setup CI (Travis)
  (`#3 <https://github.com/jugmac00/flask-reuploaded/issues/3>`_)
- fix broken tests
  (`#13 <https://github.com/jugmac00/flask-reuploaded/issues/13>`_)
- make use of `pytest` instead of the no longer maintained `nose`
  (`#2 <https://github.com/jugmac00/flask-reuploaded/issues/2>`_)
- add a changelog and start tracking changes
  (`#1 <https://github.com/jugmac00/flask-reuploaded/issues/1>`_)
