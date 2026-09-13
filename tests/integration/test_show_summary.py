import pytest
from flask import Flask
# app : Flask application
# loadClubs et loadCompetitions : fonctions to load from Json files
from server import app, loadClubs, loadCompetitions

# It's a decorator that allows code to be reused across multiple tests.
@pytest.fixture
def client():
    """Configure a Flask test client with the application context."""
    # Enable Flask's test mode.
    # Why :
    # 1) Disables certains features (e.g., session cookies)
    # 2) Allows capturing exceptions (instead of displaying them in the terminal)
    app.config['TESTING'] = True
    # app.test_client() : creates http client to send requests to your
    # application without launching a real server
    # with ... as client : ensures that the client is closed cleanly after the test
    with app.test_client() as client:
        # yield client : returns the client to the test using it.
        yield client

# Fixture for a test club
@pytest.fixture
def test_club():
    return {
        'name': 'Test Club',
        'email': 'test@club.com',
        'points': '15',  # 10 points
        'reservations': {}  # No reservations
    }

def test_show_summary_with_unknown_client(client):
    """Test that /showSummary redirects to index with an unknown email"""
    # Simulates a POST request to /showSummary with an unknown email.
    # data={'email': 'unknown@test.com'} : Sends the form data (as if a user
    # had submitted the form).
    # Why follow_redirects=True : route /showSummary uses
    # redirect(url_for('index')) if the email is unknown.
    # By default, client.post does not follow redirects (it stops at the first
    # response, which would be a 302 Redirect code).
    # With follow_redirects=True, the client follows the redirect and
    # retrieves the final response (the index.html page).
    response = client.post('/showSummary',
                           data={'email': 'unknown@mail.com'},
                           follow_redirects=True
                           )
    assert response.status_code == 200
    assert b'Email inconnu' in response.data

def test_show_summary_with_valid_email(client, mocker, test_club):
    """Test that /showSummary displays welcome.html with a valid email."""
    mocker.patch('server.loadClubs', return_value=[test_club])

    import server
    server.clubs = [test_club]

    response = client.post('/showSummary',
                           data={'email': test_club['email']},
                           follow_redirects=True
                           )
    assert response.status_code == 200
    assert b'test@club.com' in response.data


