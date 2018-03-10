from CampusCompanion import db

class CCUser(db.Model):
    __tablename__ = 'ccuser'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password


class CCIssue(db.Model):
    __tablename__ = 'ccissue'

    id = db.Column(db.Integer(), primary_key = True)
    issue_title = db.Column(db.String(), nullable=False)
    issue_description = db.Column(db.Text(), nullable=False)
    image = db.Column(db.String()) #explore how to store images using the library SQLAlchemy-ImageAttach
    location = db.Column(db.String(), nullable=False)
    date_submitted = db.Column(db.DateTime())
    date_fixed = db.Column(db.DateTime())
    user_id = db.Column(db.Integer(), db.ForeignKey('ccuser.id'))
    fixed = db.Column(db.Boolean())

    def __init__(self, issue_title, issue_description, image, location, date_submitted, date_fixed, user_id, fixed):
        self.issue_title = issue_title
        self.issue_description = issue_description
        self.image = image
        self.location = location
        self.date_submitted = date_submitted
        self.date_fixed = date_fixed
        self.user_id = user_id
        self.fixed = fixed




