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

def test_show_points_route(client, mocker, test_clubs):
    """Check if the road display the table points of clubs"""
    mocker.patch('server.loadClubs', return_value=test_clubs)
    import server
    server.clubs = test_clubs

    response = client.get('/points')
    assert response.status_code == 200
    assert b'Tableau des Points' in response.data