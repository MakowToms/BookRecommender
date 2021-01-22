# Copyright 2017 Twin Tech Labs. All rights reserved

from flask import request, url_for, flash, send_from_directory, jsonify, render_template_string
from flask import Blueprint, render_template

from book_collector import BookCollector
from wordnet import bag_words, detect_language, rank_categories, detect_genre
from ..models.forms import BookForm
from requests.exceptions import HTTPError

# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
main_blueprint = Blueprint('main', __name__, template_folder='templates')


@main_blueprint.route('/', methods=['GET', 'POST'])
def main_page():
    form = BookForm(request.form)

    if request.method == 'POST':
        try:
            scores = BookCollector(form.query.data).collect()
            for score in scores:
                print(score.book[1])
                print(score.scores, "\n")
            return render_template('pages/book_recommender.html', query=form.query.data,
                                   result=scores)
        except HTTPError as e:
            print(e)
            error = str(e)
            error_list = error.split(" ")
            return render_template('pages/errors.html', error_code=error_list[0], message=e, url=error_list[-1])

        # return redirect(url_for('main.example_page'))

    return render_template('pages/book_recommender.html', query="Red turtle swims fast", result=None)


@main_blueprint.route('/example')
def example_page():
    return render_template('pages/example.html')
