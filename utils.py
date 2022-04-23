import sqlite3
import json
from configure import path

#  show_id, type, title, director, cast, country, date_added, release_year, rating, duration, duration_type,
# listed_in, description


def get_data_from_db(show_id):
    try:
        with sqlite3.connect(path) as connection:
            cursor = connection.cursor()
            film_id = str(show_id)
            print(film_id)

            sqlite_select_query = """
            SELECT title, country, release_year, listed_in, description
            FROM netflix WHERE show_id = '<%film_id%>'
            LIMIT 10
            """
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            for row in records:
                print("ID:", row)
            # print("Всего строк:  ", len(records))

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)


# def get_comments_all():
#     """Получение списка всех комментариев из файла"""
#     with open(path_all_comments_datas, "r", encoding="utf-8") as file:
#         all_comments_datas = json.load(file)
#     print("Полный список комментариев", all_comments_datas)
#     return all_comments_datas


# {
# 		"title": "title",
# 		"country": "country",
# 		"release_year": 2021,
# 		"genre": "listed_in",
# 		"description": "description"
# }


get_data_from_db("s101")
