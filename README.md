# Blogger
A simple blog app using Flask and mongoDB

Blogger a demo app to test the working of flask with mongoDB followed by the official flask [tutorial](https://flask.palletsprojects.com/en/1.1.x/tutorial/). [`jinja2`](https://jinja.palletsprojects.com/en/2.11.x/) is used to create templates and [`pymongo`](https://api.mongodb.com/python/current/api/pymongo/index.html) driver is used to work with mongoDB.

## How to run the app?

1. Create a file named `config.py` inside `instace` directory and paste these configuration values.

        SECRET_KEY='dev_$11@$/9'                    # use a strong secret key
        DATABASE_URI='mongodb://localhost:27017/'   # replace it with your mongoDB server URI if it is not running on local machine.

2. Open terminal and from `flaskTutorial` directory run these commands:

        $ export FLASK_APP=Blogger
        $ export FLASK_ENV=development
        $ flask run

    Make sure `mongod` server is running before running any of the above commands.  

Do not forget to create a virtual environment and install all the required python packages to run the application.
