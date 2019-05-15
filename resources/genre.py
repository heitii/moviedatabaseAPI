from flask_restful import Resource
from models.genre import GenreModel

class Genre(Resource):
    def get(self, name):
        genre = GenreModel.find_by_name(name)
        if genre:
            return genre.json()
        return {'message': 'Genre not found'}, 404

    def post(self, name):
        if GenreModel.find_by_name(name):
            return {'message': "A genre with name '{}' already exists.".format(name)}, 400
        
        genre = GenreModel(name)
        try:
            genre.save_to_db()
        except:
            return {'message': 'An error occured while creating the genre.'}, 500
        
        return genre.json(), 201

    def delete(self, name):
        genre = GenreModel.find_by_name(name)
        if genre:
            genre.delete_from_db()
        
        return {'message': 'Genre deleted.'}


class GenreList(Resource):
    def get(self):
        return {'genres': [genre.json() for genre in GenreModel.query.all()]}