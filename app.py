import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)

app.config['MONGO_URI']='mongodb+srv://root:Pablo51@myfirstcluster-8ubao.mongodb.net/recipes_database?retryWrites=true&w=majority'
app.config['MONGO_DBNAME']='recipes_database'

mongo = PyMongo(app)
recipes_collection = mongo.db.recipes


@app.route('/')
@app.route('/get_recipes')
def get_recipes():
  return render_template("recipes.html", recipes=recipes_collection.find())

