import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.movie import Movie, MovieList
from resources.genre import Genre, GenreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'tiia'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Genre, '/genre/<string:name>')
api.add_resource(Movie, '/movie/<string:name>')
api.add_resource(MovieList, '/movies')
api.add_resource(GenreList, '/genres')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)