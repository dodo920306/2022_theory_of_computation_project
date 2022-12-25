from extensions import db
import datetime

class User(db.Model):
    tablename = 'user'
    id = db.Column(db.Integer, primary_key=True)
    line_id = db.Column(db.String(50), unique=True)
    display_name = db.Column(db.String(255)) 
    picture_url = db.Column(db.String(255)) 
    created_on = db.Column(db.DateTime, default=datetime.datetime.now()) 
    reservation = db.relationship('Reservation', backref='user')
    def __init__(self, line_id, display_name, picture_url):
        self.line_id=line_id
        self.display_name=display_name
        self.picture_url=picture_url