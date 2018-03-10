from app import db


class Issue(db.Model):
    __tablename__ = 'issue'

    id = db.Column(db.Integer(), primary_key = True)
    issue_title = db.Column(db.String())
    issue_description = db.Column(db.Text())
    image = db.Column(db.String()) #explore how to store images using the library SQLAlchemy-ImageAttach
    location = db.Column(db.String())
    date_submitted = db.Column(db.DateTime())
    date_fixed = db.Column(db.DateTime())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    status = db.Column(db.Boolean())

    def __init__(self, issue_title, issue_description, image, location, date_submitted, date_fixed, user_id, status):
        self.issue_title = issue_title
        self.issue_description = issue_description
        self.image = image
        self.location = location
        self.date_submitted = date_submitted
        self.date_fixed = date_fixed
        self.user_id = user_id
        self.status = status


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.password = password


