import os
import flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import find_dotenv, load_dotenv
import random


load_dotenv(find_dotenv())

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
# Gets rid of a warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "I am a secret key"

db = SQLAlchemy(app)
class Shows(db.Model):
    """class person"""
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(80), unique=False, nullable=False)
    # rating = db.Column(db.String(80), unique=False, nullable=False)
    movie_id = db.Column(db.String(80), unique=False, nullable=False)


db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    """landing page"""
    external_ids = ["27205", "557", "419430", "496243"]
    new_id = random.choice(external_ids)
    if flask.request.method == "POST":
        data = flask.request.form
        add_comment = data.get("comment")
        # add_rating = data.get("rating")
        if add_comment:
            new_show = Shows(comment=add_comment, movie_id=new_id) #, rating=add_rating)
            db.session.add(new_show)
            db.session.commit()

    data = Shows.query.filter_by(movie_id=new_id).all()
    num_data = len(data)
    # use a for loop that cycles through all of this data and then access each part that I need.
    # how can the page stop refreshing? 
    return flask.render_template(
        "index.html",
        data=data,
        movie_id=new_id,
        num_data=num_data,
    )

@app.route("/handle_form", methods=["POST"])
def handle_form():
    """handle page"""
    data = flask.request.form
    campus_id = data.get("CampusID")
    if campus_id == "jlaurent4":
        return flask.redirect(flask.url_for("welcome")) # inside the quotations are function names
    else:
        flask.flash("Wrong campus id entered")
        return flask.redirect(flask.url_for("index")) # inside the quotations is a function name

if __name__ == "__main__":
    app.run()
   