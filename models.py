from flask_sqlalchemy import SQLAlchemy

import datetime

db = SQLAlchemy()


def get_date():
    return datetime.datetime.now()


tag_entry_relation = db.Table(
    "tag_entry_relation",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id")),
    db.Column("entry_id", db.Integer, db.ForeignKey("entry.id")),
)


class Tag(db.Model):
    """
    A Class containing the tags for a post. The user creates the tags
    when creating a story. Tags are meant to be used for exploring
    categories of stories that interest a user.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1028), unique=False, nullable=False)
    entries = db.relationship(
        "Entry", secondary=tag_entry_relation, back_populates="tags"
    )

    def __repr__(self):
        return f"Tag {self.name} {self.entries}"


class Entry(db.Model):
    """
    A Class that represents a single story. It contains the story text,
    the user_id of poster, a title, and time of posting/editing.
    """

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(2048), unique=False, nullable=False)
    tags = db.relationship(
        "Tag", secondary=tag_entry_relation, back_populates="entries"
    )
    date_posted = db.Column(db.Date, default=get_date, unique=False, nullable=False)

    def __repr__(self):
        return f"Posted on date: {self.date_posted} \n {self.text}"
