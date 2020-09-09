import os
from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config.from_pyfile('config.py')

    from Blogger import db
    db.init_app(app)

    with app.app_context():
        from Blogger import auth, blog
        app.register_blueprint(auth.bp)
        app.register_blueprint(blog.bp)
        app.add_url_rule("/", endpoint="index")
    return app
