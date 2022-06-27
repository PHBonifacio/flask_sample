import json
from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.sqlite3"

class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.String())
    author = db.Column(db.String())

    def to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        
        return result


@app.route("/")
def home():
    name = request.args.get("name")
    if name == None:
        name = 'Anonymous'
    
    posts = Post.query.all()


    return render_template("index.html", name=name, posts=posts)


@app.route("/post/add", methods=["POST"])
def add_post():
    try:
        form = request.form
        post = Post(title=form["title"], content=form["content"], author=form["author"])
        db.session.add(post)
        db.session.commit()
        
    except Exception as error:
        print("Error ", error)

    return redirect(url_for("home"))

@app.route("/post/<id>/edit", methods=["POST", "GET"])
def edit_post(id):
    if request.method == "POST":
        try:
            post = Post.query.get(id)
            form = request.form
            post.title = form["title"]
            post.content = form["content"]
            post.author = form["author"]
            db.session.commit()
            
        except Exception as error:
            print("Error ", error)

        return redirect(url_for("home"))
    else:
        try:
            post = Post.query.get(id)
            print(id)
            return render_template("edit.html", post=post)
            
        except Exception as error:
            print("Error ", error)

    
    return redirect(url_for("home"))

@app.route("/post/<id>/del")
def delete_post(id):
    try:
        post = Post.query.get(id)
        db.session.delete(post)
        db.session.commit()
        
    except Exception as error:
        print("Error ", error)

    return redirect(url_for("home"))


@app.route("/api/posts")
def api_list_post():
    name = request.args.get("name")
    if name == None:
        name = 'Anonymous'
    
    posts = Post.query.all()

    return jsonify([post.to_dict() for post in posts])


@app.route("/api/post/", methods=["PUT"])
def api_add_post():
    try:
        data = request.get_json()
        post = Post(title=data["title"], content=data["content"], author=data["author"])
        db.session.add(post)
        db.session.commit()
        return jsonify({"Success" : True})
        
    except Exception as error:
        print("Error: ", error)

    
    return jsonify({"Success" : False})

@app.route("/api/post/<id>", methods=["PUT"])
def api_edit_post(id):
    try:
        post = Post.query.get(id)
        data = request.get_json()
        post.title = data["title"]
        post.content = data["content"]
        post.author = data["author"]
        db.session.commit()
        return jsonify({"Success" : True})
    except Exception as error:
        print("Error ", error)

    return jsonify({"Success" : False})

    

@app.route("/api/post/<id>", methods=["DELETE"])
def api_delete_post(id):
    try:
        post = Post.query.get(id)
        db.session.delete(post)
        db.session.commit()
        return jsonify({"Success" : True})
    except Exception as error:
        print("Error ", error)

    return jsonify({"Success" : False})


db.create_all()

app.run(debug=True)