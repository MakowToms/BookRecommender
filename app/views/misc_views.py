# Copyright 2017 Twin Tech Labs. All rights reserved

from flask import Blueprint, redirect, render_template
from flask import url_for

# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
main_blueprint = Blueprint('main', __name__, template_folder='templates')

# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/')
def member_page():
    # if not current_user.is_authenticated:
    #     return redirect(url_for('user.login'))
    return render_template('pages/member_base.html')

# The Admin page is accessible to users with the 'admin' role
# @main_blueprint.route('/admin')
# def admin_page():
#     return redirect(url_for('main.user_admin_page'))

