import os
import flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import find_dotenv, load_dotenv

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
    tvshow = db.Column(db.String(80), unique=True, nullable=False)

db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    """landing page"""
    if flask.request.method == "POST":
        data = flask.request.form
        add_show = data.get("addShow")
        delete_show = data.get("deleteShow")
        if add_show:
            new_show = Shows(tvshow=add_show)
            db.session.add(new_show)
            db.session.commit()
        elif delete_show:
            if Shows.query.filter_by(tvshow=delete_show):
                Shows.query.filter_by(tvshow=delete_show).delete()
            db.session.commit()
    data = Shows.query.all()
    num_shows = len(data)
    return flask.render_template(
        "index.html",
        data=data,
        num_shows=num_shows,
    )

if __name__ == "__main__":
    app.run()
   