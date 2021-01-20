# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

from __future__ import print_function  # Use print() instead of print
from flask import url_for


def test_page_urls(client):
    # Visit home page
    response = client.get('/', follow_redirects=True)
    assert response.status_code==200

    # Try to login with wrong email
    # response = client.post(url_for('user.login'), follow_redirects=True,
    #                        data=dict(email='non_member@example.com', password='Password1'))
    # assert response.status_code==200
    # assert b"You have signed in successfully" not in response.data
    # assert b"Sign In to your account" in response.data

    response = client.get(url_for('main.member_page'), follow_redirects=True)
    assert response.status_code==200
