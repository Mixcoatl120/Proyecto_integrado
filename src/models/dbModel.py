from app import db
from wtforms import SelectField

class Country(db.Model):
    __tablename__ = 'countries'
   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
   
class State(db.Model):
    __tablename__ = 'state'
   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    country_id = db.Column(db.Integer)
   
class City(db.Model):
    __tablename__ = 'city'
     
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    stateid = db.Column(db.Integer) 
  
class Form(FlaskForm):
    country = SelectField('country', choices=[])
    state = SelectField('state', choices=[])
    city = SelectField('city', choices=[])