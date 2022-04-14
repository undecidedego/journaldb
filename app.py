from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
import os


load_dotenv(find_dotenv())
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "MrmpiNtSBM7MSp1QBnQd"


@app.route("/")
def main():
    return render_template("log.html")


from models import db

db.init_app(app)
with app.app_context():
    # db.drop_all()
    db.create_all()

from models import Entry, Tag, tag_entry_relation


@app.route("/save", methods=["POST"])
def save():
    data = request.form
    text = request.form.get("text")
    tags = tag_to_set(request.form.get("tags"))
    new_entry = Entry(text=text)

    if save_entry(new_entry):
        add_tags(new_entry, tags)
        flash("Entry submitted successfully.")
    return render_template("log.html")


@app.route("/view_entry", methods=["POST"])
def view_entry():
    data = request.form
    id = request.form.get("entry_id")
    print("fetching entry id: ", id)
    this_entry = Entry.query.filter_by(id=id).first()
    if not this_entry:
        flash("Error: No entries found with the given ID!")
        return render_template("log.html")
    date = this_entry.date_posted
    text = this_entry.text
    print(date, " ", text)
    return render_template("view.html", text=text, date=date, entry_id=id)


@app.route("/search_tags", methods=["POST"])
def search_tags():
    data = request.form
    name = request.form.get("tag_name")
    print("fetching tag name: ", name)
    tags = Tag.query.filter_by(name=name).all()
    if not tags:
        flash("Error: No entries found with the desired tag!")
        return render_template("log.html")
    entries = tags[0].entries
    texts = []
    dates = []
    for e in entries:
        texts.append(e.text)
        dates.append(e.date_posted)
    return render_template("search_tags.html", texts=texts, dates=dates, name=name)


def add_tags(entry, tags):
    for t in tags:
        tag = Tag.query.filter_by(name=t).first()
        if not tag:
            print("adding tag ", t)
            new_tag = Tag(name=t)
            print("new tag", new_tag)
            db.session.add(new_tag)
            db.session.commit()
    db.session.commit()

    for t in tags:
        tag = Tag.query.filter_by(name=t).first()
        entry.tags.append(tag)
    db.session.commit()


def tag_to_set(tagstring):
    tagset = set()
    for tag in tagstring.split(","):
        stag = tag.strip().lower()
        tagset.add(stag)
    if "" in tagset:
        tagset.remove("")
    return tagset


def save_entry(entry):
    if not (entry.text):
        print("failed to save entry")
        return False
    db.session.add(entry)
    db.session.commit()
    print("entry saved successfully")
    return True


if __name__ == "__main__":
    app.run()
