from db import db

class MovieModel(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    year = db.Column(db.Integer)
    length = db.Column(db.Integer)
    director = db.Column(db.String(80))

    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))
    genre = db.relationship('GenreModel')

    def __init__(self, name, year, length, director, genre_id):
        self.name = name
        self.year = year
        self.length = length
        self.director = director
        self.genre_id = genre_id

    def json(self):
        return {'name': self.name, 'year': self.year, 'length': self.length, 'director': self.director}
    
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()