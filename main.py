from flask import Flask, request, render_template, redirect, url_for
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

db.create_all()

app.run(debug=True)