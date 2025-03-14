from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite_planet = db.relationship('FavoritePlanet', back_populates="user", lazy=True)
    favorite_people = db.relationship('FavoritePeople', back_populates="user", lazy=True)


    def __repr__(self):
        return '<Usuario %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    


    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    climate = db.Column(db.String(80), unique=False, nullable=False)
    population = db.Column(db.Integer, unique=False, nullable=False)
    favorite_planet = db.relationship('FavoritePlanet', back_populates="planet", lazy=True)
    

    def __repr__(self):
        return '<Planeta %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate
            # do not serialize the password, its a security breach
        }    
    

class FavoritePlanet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_planet = db.Column(db.Integer, db.ForeignKey('planet.id'))
    user = db.relationship('User')
    planet = db.relationship('Planet')

    def __repr__(self):
        return '<FavoritePlanet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.planet.name

            # do not serialize the password, its a security breach
        }        
    
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    hair_color = db.Column(db.String(80), unique=False, nullable=False)
    gender = db.Column(db.String(20), unique=False, nullable=False)
    favorite_people = db.relationship('FavoritePeople', back_populates="people", lazy=True)
    
    

    def __repr__(self):
        return '<People%r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender
            # do not serialize the password, its a security breach
        }        
    
class FavoritePeople(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_people = db.Column(db.Integer, db.ForeignKey('people.id'))
    user= db.relationship('User')
    people= db.relationship('People')
    

    def __repr__(self):
        return '<FavoritePeople %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.people.name
            # do not serialize the password, its a security breach
        }          