from flask import render_template, url_for, flash, redirect, request
from exports.webApp import app, db
from exports.webApp.models import Image, Video, Post, Author
from datetime import datetime
import pickle
import os.path

import base64

@app.route('/')
@app.route('/home')
def home():
     load_posts()
     page = request.args.get('page', 1, type=int)
     posts = Post.query.order_by(Post.date_added.desc()).paginate(page=page, per_page=5)
     authors = Author.query.all()
     images = Image.query.all()
     videos = Video.query.all()
     return render_template('home.html', posts=posts, authors = authors, images = images, videos = videos)


def load_posts():
     if os.path.isfile('./storage/data.pickle'):
            with open('./storage/data.pickle', 'rb') as handle:
                b = pickle.load(handle)
     for key in b:
          if db.session.query(Post).filter_by(id=key).count() < 1:
               nested_post_id = None
               if(b[key].nested):
                    nested_post_id = key + "1"
                    if db.session.query(Post).filter_by(id=nested_post_id).count() < 1:
                         add_post_to_db(b[key].nested, nested_post_id, False, nested_post_id)
               add_post_to_db(b[key], key, True, nested_post_id)    
          if db.session.query(Author).filter_by(name=author_check(b[key].author)).count() < 1:              
               author = Author(name = author_check(b[key].author))
               db.session.add(author)
               db.session.commit()

def add_post_to_db(feed_element, post_id, is_origin, nested_post_id):
     post = Post(id = post_id, date_posted = feed_element.date, content = feed_element.body, author = author_check(feed_element.author), is_origin = is_origin, nested = nested_post_id)
     db.session.add(post)
     db.session.commit()
     if feed_element.images:
          for val in feed_element.images:
               image = Image(data = base64.b64encode(val.file_contents).decode("utf-8"), post_id = post_id)
               db.session.add(image)
               db.session.commit()
     if feed_element.videos:
          for val in feed_element.videos:
               video = Video(url = base64.b64encode(val.url_address).decode("utf-8"), post_id = post_id)
               db.session.add(video)
               db.session.commit()

def author_check(author):
     if "shared post" in author:
          return author.split(' shared post by ')[0]
     return author


@app.route("/author/<string:author_name>")
def author_posts(author_name):
     page = request.args.get('page', 1, type=int)
     authors = Author.query.all()
     images = Image.query.all()
     videos = Video.query.all()
     author = Author.query.filter_by(name=author_name).first_or_404()
     posts = Post.query.order_by(Post.date_added.desc()).all()
     author_posts = Post.query.filter_by(author=author.name)\
          .order_by(Post.date_added.desc())\
          .paginate(page=page, per_page=5)
     return render_template('author_posts.html', author_posts=author_posts, posts = posts, authors = authors, author=author, images = images, videos = videos)