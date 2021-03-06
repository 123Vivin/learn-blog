import os
from datetime import datetime

from flask import Flask, request, render_template, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(255))
    text = db.Column(db.UnicodeText)
    create_time = db.Column(db.DateTime, default=datetime.now())
    publish_time = db.Column(db.DateTime)

def get_article_all():
    return Article.query.all()

def get_article_by_id(id):
    return Article.query.filter_by(id=id)[0]

def create_article(title, text):
    article = Article(title=title, text=text, publish_time=datetime.now())
    db.session.add(article)
    db.session.commit()

@app.route('/')
def index():
    content = dict()
    content['title'] = 'Home'
    content['article'] = get_article_all()
    return render_template('index.html',content=content)

@app.route('/article/<id>')
def view(id):
    content = dict()
    content['title'] = 'Article'
    content['article'] = get_article_by_id(id)
    return render_template('view.html',content=content)

@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        if title:
            create_article(title, text)
        return redirect(url_for('index'))
    content = dict()
    content['title'] = 'Article'
    return render_template('create.html',content=content)

if __name__ == '__main__':
    app.run(debug=True)
