import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.movie import MovieModel

class Movie(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('year',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('length',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('director',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('genre_id',
        type=int,
        required=True,
        help="All movies need a genre id."
    )

    @jwt_required()
    def get(self, title):
        movie = MovieModel.find_by_title(title)
        if movie:
            return movie.json()
        return {'message': 'Movie not found'}, 404

    def post(self, title):
        if MovieModel.find_by_title(title):
            return {'message': "A movie with title '{}' already exists.".format(title)}

        data = Movie.parser.parse_args()
        movie = MovieModel(title, **data)

        try:
            movie.save_to_db()
        except:
            return {"message": "An error occurred inserting the movie."}

        return movie.json(), 201

    def delete(self, title):
        movie = MovieModel.find_by_title(title)
        if movie:
            movie.delete_from_db()
        return {'message': 'Movie deleted'}

    def put(self, title):
        data = Movie.parser.parse_args()

        movie = MovieModel.find_by_title(title)
        
        if movie is None:
            movie = MovieModel(title, **data) 
        else:
            movie.year = data['year']
            movie.length = data['length']
            movie.director = data['director']

        movie.save_to_db()
        return movie.json()


class MovieList(Resource):
    def get(self):
        return {'movies': [movie.json() for movie in MovieModel.query.all()]}