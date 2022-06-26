from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")

def home():
    name = request.args.get("name")
    if name == None:
        name = 'Anonymous'

    return render_template("index.html", name=name)

app.run(debug=True)