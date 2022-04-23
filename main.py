from flask import Flask, request, render_template, jsonify
from utils import get_comments_by_post_id

# import logging
# logging.basicConfig(filename="basic.log", level=logging.INFO)

app = Flask(__name__)


@app.route("/")
def all_post_main_page():
    """Вьюшка главной страницы"""
    all_posters_list = get_posts_all()
    return render_template("index.html", all_posters_list=all_posters_list)


if __name__ == '__main__':
    app.run(debug=True)
