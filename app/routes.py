from flask import render_template
from . import app

@app.route('/')
def index():
    return render_template('index.html')
<<<<<<< HEAD

@app.route('/recipes')
def recipes():
    return render_template('recipes.html')
=======
>>>>>>> c3681a6c0a71549933b44a1402b765fd210b9af7
