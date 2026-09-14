import json
import pytest
from datetime import datetime, timedelta
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_purchase_competition_missing(client, mocker):
    """Check if road handle a club or competition is missing"""
    test_club = {'name': 'Test Club', 'email': 'test@club.com', 'points': '10'}
    test_competition = None  # Compétition manquante

    mocker.patch('server.loadClubs', return_value=[test_club])
    mocker.patch('server.loadCompetitions', return_value=[])  # Aucune compétition

    import server
    server.clubs = [test_club]
    server.competitions = []

    # try to book a missing competition
    response = client.post(
        '/purchasePlaces',
        data={
            'club': test_club['name'],
            'competition': 'No competition',
            'places': 1
        },
        follow_redirects=True
    )
    assert b"Competition ou club introuvable" in response.data

def test_purchase_club_missing(client, mocker):
    """Check if road handle a club or competition is missing"""
    test_club = {'name': 'Test Club', 'email': 'test@club.com', 'points': '10'}
    test_competition = {"name": "Test Competition", "numberOfPlaces": "17"}

    mocker.patch('server.loadClubs', return_value=[test_club])
    mocker.patch('server.loadCompetitions', return_value=[])

    import server
    server.clubs = [test_club]
    server.competitions = []

    # try to book a missing competition
    response = client.post(
        '/purchasePlaces',
        data={
            'club': 'no club',
            'competition': test_competition['name'],
            'places': 1
        },
        follow_redirects=True
    )
    assert b"Competition ou club introuvable" in response.data

def test_purchase_book(client, mocker):
    """Check road book display booking"""
    test_clubs = [
        {'name': 'Test club'},
        {'name': 'Test club2'},
    ]
    test_competitions = [
        {'name': 'Test competition'},
        {'name': 'Test competition2'},
    ]

    mocker.patch('server.loadClubs', return_value=test_clubs)
    mocker.patch('server.loadCompetitions', return_value=test_competitions)

    import server
    server.clubs = test_clubs
    server.competitions = test_competitions

    # Call the road with parameters in URL
    response = client.get(
        f"/book/{test_competitions[0]['name']}/{test_clubs[0]['name']}",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Booking for Test competition" in response.data

def test_purchase_no_book(client, mocker):
    """Check road no book if club name no exist"""
    test_clubs = [
        {'name': 'Test club'},
        {'name': 'Test club2'},
    ]
    test_competitions = [
        {'name': 'Test competition', 'numberOfPlaces': '20'},
        {'name': 'Test competition2', 'numberOfPlaces': '20'},
    ]

    mocker.patch('server.loadClubs', return_value=test_clubs)
    mocker.patch('server.loadCompetitions', return_value=test_competitions)

    import server
    server.clubs = test_clubs
    server.competitions = test_competitions

    # Call the road with parameters in URL
    response = client.get(
        f"/book/{test_competitions[0]['name']}/noclub",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Something went wrong-please try again" in response.data

def test_logout_route(client):
    """Check road logout redirect into homepage (index.html)"""
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome to the GUDLFT Registration Portal' in response.data

if __name__ == '__main__':
    pytest.main()

