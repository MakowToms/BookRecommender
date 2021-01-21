# Copyright 2017 Twin Tech Labs. All rights reserved

from flask import request, url_for, flash, send_from_directory, jsonify, render_template_string
from flask import Blueprint, render_template

from book_collector import BookCollector
from wordnet import bag_words, detect_language, rank_categories, detect_genre
from ..models.forms import BookForm

# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
main_blueprint = Blueprint('main', __name__, template_folder='templates')


@main_blueprint.route('/', methods=['GET', 'POST'])
def main_page():
    form = BookForm(request.form)

    if request.method == 'POST':
        scores = BookCollector(form.query.data).collect()
        return render_template('pages/book_recommender.html', query="", details="",
                               result=[(score.book, score.final_score) for score in scores])
        # return redirect(url_for('main.example_page'))

    return render_template('pages/book_recommender.html', query="Red turtle swims fast", details="Details", result=None)


@main_blueprint.route('/example')
def example_page():
    return render_template('pages/example.html')
