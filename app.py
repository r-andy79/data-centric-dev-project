import os
import datetime
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)



mongo = PyMongo(app)
recipes_collection = mongo.db.recipes
users_collection = mongo.db.users


@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    return render_template("recipes.html", recipes=recipes_collection.find())


# add recipe template
@app.route("/add_recipe")
def add_recipe():
    return render_template("addrecipe.html")

# insert recipe to the database
@app.route("/insert_recipe", methods=["POST"])
def insert_recipe():
    form = request.form.to_dict()
    recipes_collection.insert_one(
        {
            "name": form["name"],
            "description": form["description"],
            "author": form["author"],
            "cuisine": form["cuisine"],
            "allergens": form["allergens"],
            "ingredients": (form["ingredients"].split(",")),
            "preparation": form["preparation"],
            "like": bool("false"),
            "votes": int("0"),
            "date_added": datetime.datetime.now(),
        }
    )
    return redirect(url_for("get_recipes"))

# view a single recipe
@app.route("/single_recipe/<recipe_id>")
def single_recipe(recipe_id):
  the_recipe = recipes_collection.find_one({"_id": ObjectId(recipe_id)})
  return render_template('singlerecipe.html', recipe=the_recipe)

# delete a recipe
@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
  recipes_collection.remove({"_id": ObjectId(recipe_id)})
  return redirect(url_for('get_recipes'))
