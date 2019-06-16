import os
import datetime
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)

app.config['MONGO_URI']='mongodb+srv://root:Pablo51@myfirstcluster-8ubao.mongodb.net/recipes_database?retryWrites=true&w=majority'
app.config['MONGO_DBNAME']='recipes_database'

mongo = PyMongo(app)
recipes_collection = mongo.db.recipes
users_collection = mongo.db.users


@app.route('/')
@app.route('/get_recipes')
def get_recipes():
  return render_template("recipes.html", recipes=recipes_collection.find())

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
  if request.method == 'POST':
    form = request.form.to_dict()
    recipes = recipes_collection
    recipes.insert_one(
      {
        'name': form['name'],
        'description': form['description'],
        'author': form['author'],
        'cuisine': form['cuisine'],
        'allergens': form['allergens'],
        'ingredients': (form['ingredients'].split(',')),
        'preparation': form['preparation'],
        'vegetarian': bool(form['vegetarian']),
        'like': bool('false'),
        'votes': int('0'),
        'date_added': datetime.datetime.now()
      }
    )
  return render_template("addrecipe.html")

