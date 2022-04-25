from flask import Flask, jsonify
from utils import search_by_title, search_by_years, search_by_rating, get_by_actor, search_by_genre,\
    get_by_type

import logging
logging.basicConfig(filename="basic.log", level=logging.INFO)


def main():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config['DEBUG'] = True

    @app.route("/movie/<title>")
    def search_by_film_title(title):
        """Вьюшка страницы поиска по названию"""
        response_json = search_by_title(title)
        return jsonify(response_json)

    @app.route("/movie/<int:from_year>/to/<int:to_year>")
    def search_by_film_years(from_year, to_year):
        """Вьюшка страницы поиска по годам"""
        response_json = search_by_years(from_year, to_year)
        return jsonify(response_json)

    @app.route("/rating/<group>")
    def search_by_film_rating(group):
        """Вьюшка страницы поиска по рейтингу"""
        response_json = search_by_rating(group)
        return jsonify(response_json)

    @app.route("/genre/<genre>")
    def search_film_by_genre(genre):
        """Вьюшка страницы поиска по жанру"""
        response_json = search_by_genre(genre)
        return jsonify(response_json)

    @app.route("/search/<actor1>/<actor2>")
    def get_film_by_actor(actor1, actor2):
        """Вьюшка поиска актеров из фильмов с двумя другими"""
        response_json = get_by_actor(actor1, actor2)
        return jsonify(response_json)

    @app.route("/search/<genre>/<int:release_year>/<film_type>")
    def get_film_by_type(film_type, release_year, genre):
        """Вьюшка поиска по типу, жанру и году"""
        response_json = get_by_type(film_type, release_year, genre)
        return jsonify(response_json)

    app.run(debug=True)


if __name__ == '__main__':
    main()
