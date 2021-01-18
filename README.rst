.. image:: https://github.com/jugmac00/flask-reuploaded/workflows/CI/badge.svg?branch=master
   :target: https://github.com/jugmac00/flask-reuploaded/actions?workflow=CI
   :alt: CI Status

.. image:: https://coveralls.io/repos/github/jugmac00/flask-reuploaded/badge.svg?branch=master
    :target: https://coveralls.io/github/jugmac00/flask-reuploaded?branch=master

.. image:: https://img.shields.io/pypi/v/flask-reuploaded   
    :alt: PyPI
    :target: https://github.com/jugmac00/flask-reuploaded

.. image:: https://img.shields.io/pypi/pyversions/flask-reuploaded   
    :alt: PyPI - Python Version
    :target: https://pypi.org/project/Flask-Reuploaded/

.. image:: https://requires.io/github/jugmac00/flask-reuploaded/requirements.svg?branch=master
    :target: https://requires.io/github/jugmac00/flask-reuploaded/requirements/?branch=master
    :alt: Requirements Status

.. image:: https://img.shields.io/pypi/l/hibpcli
    :target: https://github.com/jugmac00/flask-reuploaded/blob/master/LICENSE


Flask-Reuploaded
================

Flask-Reuploaded provides file uploads for Flask.


Notes on this package
---------------------

This is an independently maintained version of `Flask-Uploads`
based on the 0.2.1 version of the original,
but also including four years of unreleased changes,
at least not released to PyPi.

Noteworthy is the fix for the `Werkzeug` API change.


Goals
-----

- provide a stable drop-in replacement for `Flask-Uploads`
- regain momentum for this widely used package
- provide working PyPI packages


Migration guide from `Flask-Uploads`
------------------------------------

Incompatibilities between Flask-Reuploaded and Flask-Uploads
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Currently, there are no known incompatibilities.

Just follow the `Uninstall and install` instructions below.

Please note, that `Flask-Uploads`,
and thus also `Flask-Reuploaded` has an builtin **autoserve** feature.

This means that uploaded files are automatically served for viewing and downloading.

e.g. if you configure an `Uploadset` with the name `photos`,
and upload a picture called `snow.jpg`,
the picture can be automatically accessed at e.g. `http://localhost:5000/_uploads/photos/snow.jpg`
unless
- you set `UPLOADED_PHOTOS_URL` to an empty string, ie `""`
- you configure `UPLOADED_PHOTOS_URL` with a valid string
(then the picture is served from there)
- or you set `UPLOADS_AUTOSERVE` to `False`.

The last option is new in `Flask-Reuploaded`.

In order to stay compatible with `Flask-Uploads`,
by default `UPLOADS_AUTOSERVE` is currently set to `True`,

With `Flask-Reuploaded` version 1.0.0,
`UPLOADS_AUTOSERVE` will default to `False`,
as this feature is/was undocumented,
surprising,
and actually it could lead to unwanted data disclosure.

Setting it explicitly to `False` is recommended.


Uninstall and install
~~~~~~~~~~~~~~~~~~~~~

If you have used `Flask-Uploads` and want to migrate to `Flask-Reuploaded`,
you only have to install `Flask-Reuploaded` instead of `Flask-Uploads`.

That's all!

So, if you use `pip` to install your packages, instead of ...

.. code-block:: bash

    $ pip install `Flask-Uploads`  # don't do this! package is broken

... just do ...

.. code-block:: bash

    $ pip install `Flask-Reuploaded`

`Flask-Reuploaded` is a drop-in replacement.

This means you do not have to change a single line of code.


Installation
------------

.. code-block:: bash

    $ pip install Flask-Reuploaded


Getting started
---------------

create an UploadSet

.. code-block:: python

    from flask_uploads import IMAGES

    photos = UploadSet("photos", IMAGES)

configure your Flask app and this extension

.. code-block:: python

    app.config["UPLOADED_PHOTOS_DEST"] = "static/img"
    app.config["SECRET_KEY"] = os.urandom(24)
    configure_uploads(app, photos)

use `photos` in your view function

.. code-block:: python

    photos.save(request.files['photo'])

See below for a complete example.


Documentation
-------------

The documentation can be found at...

https://flask-reuploaded.readthedocs.io/en/latest/


Minimal example application
----------------------------


Application code, e.g. main.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import os

    from flask import Flask, flash, render_template, request
    # please note the import from `flask_uploads` - not `flask_reuploaded`!!
    # this is done on purpose to stay compatible with `Flask-Uploads`
    from flask_uploads import IMAGES, UploadSet, configure_uploads

    app = Flask(__name__)
    photos = UploadSet("photos", IMAGES)
    app.config["UPLOADED_PHOTOS_DEST"] = "static/img"
    app.config["SECRET_KEY"] = os.urandom(24)
    configure_uploads(app, photos)


    @app.route("/", methods=['GET', 'POST'])
    def upload():
        if request.method == 'POST' and 'photo' in request.files:
            photos.save(request.files['photo'])
            flash("Photo saved successfully.")
            return render_template('upload.html')
        return render_template('upload.html')


HTML code for `upload.html`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html

    <!doctype html>
    <html lang=en>
    <head>
        <meta charset=utf-8>
        <title>Flask-Reuploaded Example</title>
    </head>
    <body>
        {% with messages = get_flashed_messages() %}
        {% if messages %}
        <ul class=flashes>
        {% for message in messages %}
            <li>{{ message }}</li>
        {% endfor %}
        </ul>
        {% endif %}
        {% endwith %}

    <form method=POST enctype=multipart/form-data action="{{ url_for('upload') }}">
        <input type=file name=photo>
        <button type="submit">Submit</button>
    </form>
    </body>
    </html>


Project structure
~~~~~~~~~~~~~~~~~

The project structure would look as following...

.. code-block:: bash

    ❯ tree -I "__*|h*"
    .
    ├── main.py
    ├── static
    │   └── img
    └── templates
        └── upload.html


Running the example application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to run the application,
you have to enter the following commands...

.. code-block:: bash

    ❯ export FLASK_APP=main.py

    ❯ flask run

Then point your browser to `http://127.0.0.1:5000/`.


Contributing
------------

Contributions are more than welcome.

Please have a look at the `open issues <https://github.com/jugmac00/flask-reuploaded/issues>`_.

There is also a `short contributing guide <https://github.com/jugmac00/flask-reuploaded/blob/master/CONTRIBUTING.rst>`_.
