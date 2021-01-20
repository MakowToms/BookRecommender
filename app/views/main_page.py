# Copyright 2017 Twin Tech Labs. All rights reserved

from flask import request, url_for, flash, send_from_directory, jsonify, render_template_string
from flask import Blueprint, render_template

from wordnet import bag_words, detect_language, rank_categories
from ..models.forms import BookForm

# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
main_blueprint = Blueprint('main', __name__, template_folder='templates')


@main_blueprint.route('/', methods=['GET', 'POST'])
def main_page():
    form = BookForm(request.form)

    if request.method == 'POST':
        x = bag_words(form.query.data)
        categories = rank_categories(x)
        langs = detect_language(x)
        print(f'Data: {form.query.data}')
        print(f'Categories ranked: {categories}')
        print(f'Languages found: {langs}')
        return render_template('pages/book_recommender.html', query="", details="", result=[1, 2, 3])
        # return redirect(url_for('main.example_page'))

    return render_template('pages/book_recommender.html', query="Red turtle swims fast", details="Details", result=None)


@main_blueprint.route('/example')
def example_page():
    return render_template('pages/example.html')
