import pytest
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
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

def test_user_journey_with_unknown_email(client):
    """Functional test: simulates a user journey with an unknown email address."""
    # Step 1 : go to the homepage
    response = client.get('/')
    assert response.status_code == 200

    # Step 2 : submit an unknown email address
    response = client.post('/showSummary',
                           data={'email': 'unknown@test.com'},
                           follow_redirects=True
                           )
    assert response.status_code == 200
    assert b'Email inconnu' in response.data
    # print(response.data)

    # Step 3 : check if user stay in homepage
    assert b'Welcome to the GUDLFT Registration Portal!' in response.data


def test_user_journey_with_known_email(client, mocker, test_club):
    """Functional test: simulates a user journey with an known email address."""
    mocker.patch('server.loadClubs', return_value=[test_club])
    import server
    server.clubs = [test_club]
    # Step 1 : go to the homepage
    response = client.get('/')
    assert response.status_code == 200

    # Step 2 : submit an known email address
    response = client.post('/showSummary',
                           data= {'email': test_club['email']},
                           follow_redirects=True
                           )
    assert response.status_code == 200

    # Step 3 : check if user go to the welcome.html
    assert b'Welcome, test@club.com' in response.data
