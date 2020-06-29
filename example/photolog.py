"""
photolog.py
===========
This is a simple example app for Flask-Uploads. It uses Flask-CouchDB as well,
because I like CouchDB. It's a basic photolog app that lets you submit blog
posts that are photos.
"""
import datetime
import uuid

from flask import Flask
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask.ext.couchdb import CouchDBManager
from flask.ext.couchdb import DateTimeField
from flask.ext.couchdb import Document
from flask.ext.couchdb import TextField
from flask.ext.couchdb import ViewField
from flask.ext.uploads import IMAGES
from flask.ext.uploads import UploadNotAllowed
from flask.ext.uploads import UploadSet
from flask.ext.uploads import configure_uploads

# defaults

DEBUG = False
SECRET_KEY = ('\xa3\xb6\x15\xe3E\xc4\x8c\xbaT\x14\xd1:'
              '\xafc\x9c|.\xc0H\x8d\xf2\xe5\xbd\xd5')

UPLOADED_PHOTOS_DEST = '/tmp/photolog'

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'flaskftw'

COUCHDB_SERVER = 'http://localhost:5984/'
COUCHDB_DATABASE = 'flask-photolog'


# application

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('PHOTOLOG_SETTINGS', silent=True)


# uploads

uploaded_photos = UploadSet('photos', IMAGES)
configure_uploads(app, uploaded_photos)


# documents

manager = CouchDBManager()

def unique_id():
    return hex(uuid.uuid4().time)[2:-1]


class Post(Document):
    doc_type = 'post'
    title = TextField()
    filename = TextField()
    caption = TextField()
    published = DateTimeField(default=datetime.datetime.utcnow)

    @property
    def imgsrc(self):
        return uploaded_photos.url(self.filename)

    all = ViewField('photolog', '''\
        function (doc) {
            if (doc.doc_type == 'post')
                emit(doc.published, doc);
        }''', descending=True)


manager.add_document(Post)
manager.setup(app)


# utils

def to_index():
    return redirect(url_for('index'))


@app.before_request
def login_handle():
    g.logged_in = bool(session.get('logged_in'))


# views

@app.route('/')
def index():
    posts = Post.all()
    return render_template('index.html', posts=posts)


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        photo = request.files.get('photo')
        title = request.form.get('title')
        caption = request.form.get('caption')
        if not (photo and title and caption):
            flash("You must fill in all the fields")
        else:
            try:
                filename = uploaded_photos.save(photo)
            except UploadNotAllowed:
                flash("The upload was not allowed")
            else:
                post = Post(title=title, caption=caption, filename=filename)
                post.id = unique_id()
                post.store()
                flash("Post successful")
                return to_index()
    return render_template('new.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        flash("You are already logged in")
        return to_index()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if (username == app.config['ADMIN_USERNAME'] and
            password == app.config['ADMIN_PASSWORD']):
            session['logged_in'] = True
            flash("Successfully logged in")
            return to_index()
        else:
            flash("Those credentials were incorrect")
    return render_template('login.html')


@app.route('/logout')
def logout():
    if session.get('logged_in'):
        session['logged_in'] = False
        flash("Successfully logged out")
    else:
        flash("You weren't logged in to begin with")
    return to_index()


if __name__ == '__main__':
    app.run(debug=True)
