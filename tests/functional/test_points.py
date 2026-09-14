import pytest
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def test_clubs():
    """Fixture for clubs list"""
    return [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "7"},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "15"},
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "8"}
    ]

def test_user_journey_view_points(client, mocker, test_clubs):
    """Simulate a user journey to see points table."""
    mocker.patch('server.loadClubs', return_value=test_clubs)
    import server
    server.clubs = test_clubs

    # Step & : go to homepage
    response = client.get('/')
    assert response.status_code == 200

    # Step 2 : click link "Voir le tableau des points"
    response = client.get('/points', follow_redirects=True)
    assert response.status_code == 200
    assert b'Tableau des Points' in response.data