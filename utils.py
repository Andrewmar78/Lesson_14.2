import sqlite3
from configure import path


def db_connection(qwery):
    """Соединение с базой данных"""
    try:
        with sqlite3.connect(path) as connection:
            cursor = connection.cursor()
            cursor.execute(qwery)
            result = cursor.fetchall()
            return result
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)


def search_by_title(title):
    """Поиск по названию"""
    qwery = f"""
    SELECT title, country, release_year, listed_in AS genre, description
    FROM netflix WHERE title = '{title}'
    ORDER BY release_year DESC
    LIMIT 1
    """
    response = db_connection(qwery)[0]
    response_json = {
        "title": response[0],
        "country": response[1],
        "release_year": response[2],
        "genre": response[3],
        "description": response[4],
    }
    return response_json


def search_by_years(from_year, to_year):
    """Поиск по годам"""
    qwery = f"""
        SELECT title, release_year
        FROM netflix WHERE release_year BETWEEN {from_year} AND {to_year}
        ORDER BY title
        LIMIT 100
        """
    response = db_connection(qwery)
    response_json = []
    for film in response:
        response_json.append({
            "title": film[0],
            "release_year": film[1],
        })
    return response_json


def search_by_rating(group):
    """Поиск по рейтингу"""
    levels = {
        "children": ["G"],
        "family": ["G", "PG", "PR-13"],
        "adult": ["R", "NC-17"]
    }
    if group in levels:
        level = '\", \"'.join(levels[group])
        level = f'\"{level}"'
    else:
        return f"Такой группы нет"

    qwery = f"""  
           SELECT title, rating, description
           FROM netflix WHERE rating IN ({level})
           ORDER BY title
           LIMIT 100
           """

    response = db_connection(qwery)
    response_json = []
    for film in response:
        response_json.append({
            "title": film[0],
            "rating": film[1],
            "description": film[2],
        })
    return response_json


def search_by_genre(genre):
    """Поиск по жанру"""
    qwery = f"""        
          SELECT title, description
          FROM netflix WHERE listed_in LIKE '%{genre}%'
          ORDER BY rating DESC
          LIMIT 10
          """
    response = db_connection(qwery)
    response_json = []
    for film in response:
        response_json.append({
            "title": film[0],
            "description": film[1],
        })
    if response_json:
        return response_json
    else:
        return f"Нет такого жанра"


def get_by_actor(actor1, actor2):
    """Поиск актеров из фильмов с двумя другими"""
    qwery = f"""    
          SELECT "cast"
          FROM netflix WHERE "cast" LIKE '%{actor1}%'
          OR "cast" LIKE '%{actor2}%'
          ORDER BY rating DESC
          LIMIT 10
          """
    response = db_connection(qwery)
    actors = []
    for cast in response:
        actors.extend(cast[0].split(', '))
    response_json = []
    for i in actors:
        if i not in [actor1, actor2]:
            if actors.count(i) > 2:
                response_json.append(i)
    response_json = set(response_json)
    if response_json:
        return list(response_json)
    else:
        return f"Нет таких актеров"


def get_by_type(film_type, release_year, genre):
    """Поиск по типу, жанру и году"""
    qwery = f"""    
          SELECT title, description, type
          FROM netflix WHERE type LIKE '%{film_type}%'
          AND release_year = '{release_year}'
          AND listed_in LIKE '%{genre}%'
          ORDER BY rating DESC
          """
    response = db_connection(qwery)
    response_json = []
    for film in response:
        response_json.append({
            "title": film[0],
            "description": film[1],
            "type": film[2],
        })
    if response_json:
        return response_json
    else:
        return f"Нет таких фильмов или в этом году кина не было"
