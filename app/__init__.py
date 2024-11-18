from flask import Flask, g
from .app_factory import create_app
from .db_connect import close_db, get_db

app = create_app()
app.secret_key = 'your-secret'  # Replace with an environment variable

<<<<<<< HEAD
from app.blueprints.users import users
from app.blueprints.recipes import recipes
from app.blueprints.favorites import favorites

app.register_blueprint(users)
app.register_blueprint(recipes)
app.register_blueprint(favorites)
=======
from app.blueprints.sales import sales
from app.blueprints.regions import regions

app.register_blueprint(sales)
app.register_blueprint(regions)
>>>>>>> c3681a6c0a71549933b44a1402b765fd210b9af7

from . import routes

@app.before_request
def before_request():
    g.db = get_db()

# Setup database connection teardown
@app.teardown_appcontext
def teardown_db(exception=None):
    close_db(exception)