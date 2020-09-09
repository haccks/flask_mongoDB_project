import functools, datetime
from flask import (Blueprint, request, redirect, url_for, flash,
                   render_template, session, g)
from werkzeug.exceptions import abort
from bson.json_util import ObjectId
from Blogger.db import get_db_client
from Blogger.auth import login_required

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    blog_db = get_db_client().blogger
    pipeline = [
        {
            "$lookup":
                {
                    "from": "users",
                    "localField": "author_id",
                    "foreignField": "_id",
                    "as": "authors"
                }
        }
    ]
    posts = blog_db.articles.aggregate(pipeline=pipeline)
    return render_template('blog/index.html', posts=posts)


@login_required
@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        error = None

        if not title:
            error = 'Title is required.'

        if error is None:
            blog_db = get_db_client().blogger
            blog_db.articles.insert_one(
                {
                    'title': title,
                    'body': body,
                    'created_on': datetime.datetime.utcnow(),
                    'author_id': g.user['_id'],
                }
            )
            return redirect(url_for('blog.index'))

        flash(error)

    return render_template('blog/create.html')


def get_post(post_id):
    blog_db = get_db_client().blogger
    post = blog_db.articles.find_one({'_id': ObjectId(post_id)})

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(post_id))
    if post['author_id'] != g.user['_id']:
        abort(403)

    return post


@login_required
@bp.route('/<post_id>/update', methods=('GET', 'POST'))
def update(post_id):
    post = get_post(post_id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is None:
            blog_db = get_db_client().blogger
            blog_db.articles.update_one(
                {'_id': post['_id']},
                [
                    {'$set': {'title': title, 'body': body, 'lastModified': '$$NOW'}}
                ]
            )
            return redirect(url_for('blog.index'))

        flash(error)
    return render_template('blog/update.html', post=post)


@login_required
@bp.route('/<post_id>/delete', methods=('POST',))
def delete(post_id):
    post = get_post(post_id)
    blog_db = get_db_client().blogger
    blog_db.articles.delete_one({'_id': post['_id']})

    return redirect(url_for('blog.index'))
