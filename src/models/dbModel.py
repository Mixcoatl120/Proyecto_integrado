"""Este .py contiene los modelos de las bases de datos o mas bien dicho las tablas que 
usara nuestro programa se tiene que definir con las columnas que usaremos de cada tabla
o en caso de que se necesiten todas se tienen que definir"""
from wtforms import SelectField
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Tip_ing(db.Model):
    __tablename__ = 'cat_tipo_ingreso'
   
    id = db.Column(db.Integer, primary_key=True)
    tipo_ingreso = db.Column(db.String(255))
    
    def __init__(self,id,tipo_ingreso):
        self.id = id
        self.tipo_ingreso = tipo_ingreso

class Asunto(db.Model):
    __tablename__ = 'cat_tipo_asunto'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(255))
    
    def __init__(self,id,tipo):
        self.id = id
        self.tipo = tipo

class Materia(db.Model): #------------------Materia----------------------
    __tablename__ = 'cat_materia'

    id = db.Column(db.Integer, primary_key=True)
    materia = db.Column(db.String(255))
    
    def __init__(self,id,materia):
        self.id = id
        self.materia = materia

class Tramite(db.Model): #------------------Tramite----------------------
    __tablename__ = 'cat_tramites'

    idtram = db.Column(db.Integer, primary_key=True)
    cvetramite = db.Column(db.String(255))
    cofemer = db.Column(db.String(255))
    
    def __init__(self,idtram,cvetramite,cofemer):
        self.idtram = idtram
        self.cvetramite = cvetramite
        self.cofemer = cofemer



