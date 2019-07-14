import os
import numpy as np
import datetime
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.json_util import dumps

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://root:Pablo51@myfirstcluster-8ubao.mongodb.net/recipes_database?retryWrites=true&w=majority"
app.config["MONGO_DBNAME"] = "recipes_database"


mongo = PyMongo(app)
recipes_collection = mongo.db.recipes
users_collection = mongo.db.users

#testing feature-1

def parse_string(string):
    arr_string = string.split(',')
    arr_trim = []
    for item in arr_string:
      arr_trim.append(item.strip())
    return arr_trim

@app.route("/test", methods=['POST'])
def test():
    query = request.json['q']

    results = recipes_collection.find(query)
    return dumps(results)

@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    return render_template("recipes.html", recipes=recipes_collection.find())

#user registration
@app.route("/register")
def register():
  return render_template("register.html")

#adding user to the database
@app.route("/insert_user", methods=["POST"])
def insert_user():
  form = request.form.to_dict()
  users_collection.insert_one(form)
  return redirect(url_for("add_recipe"))

# add recipe template
@app.route("/add_recipe")
def add_recipe():
    return render_template("addrecipe.html", authors=users_collection.find())

@app.route("/cuisines")
def cuisines():
  return render_template("cuisines.html", recipes=recipes_collection.find())

@app.route("/sorting/")
def sorting():
  if request.method=='GET':
    sort_term = request.args.get('sort', 'views')
    sort_direction_term = request.args.get('direction', 'desc')
    sort_direction_translated = {'asc': 1, 'desc': -1}[sort_direction_term]
    xxx=url_for('sorting') + '?sort=views&direction=asc'
  return render_template("recipes.html", recipes=recipes_collection.find().sort(sort_term, sort_direction_translated), xxx=xxx)

# insert recipe to the database
@app.route("/insert_recipe", methods=["POST"])
def insert_recipe():
    form = request.form.to_dict()
    recipes_collection.insert_one(
        {
            "name": form["name"],
            "description": form["description"],
            "author": form["author"],
            "cuisine": form["cuisine"].lower(),
            "allergens": parse_string(form["allergens"]),
            "ingredients": parse_string(form["ingredients"]),
            "preparation": form["preparation"],
            "likes": bool(0),
            "views": int("0"),
            "votes": int("0"),
            "date_added": datetime.datetime.now()
        }
    )
    return redirect(url_for("get_recipes"))


# single recipe view
@app.route("/single_recipe/<recipe_id>")
def single_recipe(recipe_id):
    recipes_collection.update(
        {"_id": ObjectId(recipe_id)},
        {"$inc": 
        {"views": 1}
      }
    )
    the_recipe = recipes_collection.find_one({"_id": ObjectId(recipe_id)})
    return render_template("singlerecipe.html", recipe=the_recipe)


# delete a recipe
@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    recipes_collection.remove({"_id": ObjectId(recipe_id)})
    return redirect(url_for("get_recipes"))


# edit a recipe
@app.route("/edit_recipe/<recipe_id>")
def edit_recipe(recipe_id):
    the_recipe = recipes_collection.find_one({"_id": ObjectId(recipe_id)})
    the_author = users_collection.find()
    return render_template("editrecipe.html", recipe=the_recipe, author=the_author)


# update recipe
@app.route("/update_recipe/<recipe_id>", methods=["POST"])
def update_recipe(recipe_id):
    recipes_collection.update(
        {"_id": ObjectId(recipe_id)},
        {"$set":
          {
            "name": request.form.get("name"),
            "description": request.form.get("description"),
            "author": request.form.get("author"),
            "cuisine": request.form.get("cuisine"),
            "allergens": parse_string(request.form.get("allergens")),
            "ingredients": parse_string(request.form.get("ingredients")),
            "preparation": request.form.get("preparation"),
          }
        }
    )
    return redirect(url_for("get_recipes"))