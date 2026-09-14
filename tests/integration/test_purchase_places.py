import json
import pytest
from flask import Flask
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

@pytest.fixture
def test_club2():
    return {
        'name': 'Test Club',
        'email': 'test@club.com',
        'points': '10',  # 10 points
        'reservations': {}  # No reservations
    }

# Fixture for a test competition
@pytest.fixture
def test_competition():
    return {
        'name': 'Test Competition',
        'numberOfPlaces': '20'  # 20 available places
    }

@pytest.fixture
def test_competition2():
    return {
        'name': 'Test Competition',
        'numberOfPlaces': '5'  # 20 available places
    }


def test_purchase_places_without_enough_point(client, mocker, test_club2,
                                              test_competition):

    mocker.patch('server.loadClubs', return_value=[test_club2])
    mocker.patch('server.loadCompetitions', return_value=[test_competition])

    import server
    server.clubs = [test_club2]
    server.competitions = [test_competition]

    places_required = int(test_club2['points']) + 1
    response = client.post(
        '/purchasePlaces',
        data={
            'club': test_club2['name'],
            'competition': test_competition['name'],
            'places': places_required
        },
        follow_redirects=True
    )
    assert int(server.clubs[0]['points']) >=0
    assert response.status_code == 200
    assert (b"Vous n avez pas assez de points pour acheter ces places." in
            response.data)

def test_purchase_places_exceed_12_places(client, mocker, test_club,
                                            test_competition):
    """Test that a club cannot exceed 12 places per competition."""

    mocker.patch('server.loadClubs', return_value=[test_club])
    mocker.patch('server.loadCompetitions',
                    return_value=[test_competition])

    import server
    server.clubs = [test_club]
    server.competitions = [test_competition]

    # Simulate 0 existing reservations
    # test_club['reservations'] = {test_competition['name'] : 0}
    response = client.post(
        '/purchasePlaces',
        data={
            'club': test_club['name'],
            'competition': test_competition['name'],
            'places': 13
        },
        follow_redirects=True
    )
    assert b"Great-booking complete!" not in response.data
    assert response.status_code == 200
    assert (b"Vous ne pouvez pas reserver plus de 12 places par competition."
            in response.data)

def test_purchase_places_exceed_cumulative_12_places(client, mocker,
                                                        test_club,
                                                        test_competition):
    """Test that a club cannot exceed a cumulative total of 12 places."""
    mocker.patch('server.loadClubs', return_value=[test_club])
    mocker.patch('server.loadCompetitions',
                    return_value=[test_competition])

    import server
    server.clubs = [test_club]
    server.competitions = [test_competition]

    test_club['reservations'] = {test_competition['name']: 5}
    response = client.post(
        '/purchasePlaces',
        data={
            'club': test_club['name'],
            'competition': test_competition['name'],
            'places': 8
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert (b"Vous ne pouvez pas reserver plus de 12 places par competition."
            in response.data)

def test_purchase_places_without_enough_competition_places(client, mocker,
                                                           test_club2,
                                                           test_competition2):
    mocker.patch('server.loadClubs', return_value=[test_club2])
    mocker.patch('server.loadCompetitions', return_value=[test_competition2])

    import server
    server.clubs = [test_club2]
    server.competitions = [test_competition2]

    places_required = int(test_competition2['numberOfPlaces']) + 1

    response = client.post(
        '/purchasePlaces',
        data={
            'club': test_club2['name'],
            'competition': test_competition2['name'],
            'places': places_required
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert (b"Il n y a pas assez de places pour cette competition" in
            response.data)
    assert b"Reservation validee" not in response.data

def test_purchase_places_with_enough_competition_places(client, mocker,
                                                           test_club2,
                                                           test_competition2):
    mocker.patch('server.loadClubs', return_value=[test_club2])
    mocker.patch('server.loadCompetitions', return_value=[test_competition2])

    import server
    server.clubs = [test_club2]
    server.competitions = [test_competition2]

    places_required = int(test_competition2['numberOfPlaces']) - 1

    response = client.post(
        '/purchasePlaces',
        data={
            'club': test_club2['name'],
            'competition': test_competition2['name'],
            'places': places_required
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Reservation validee" in response.data

def test_purchase_places_with_valid_data(client, mocker, test_club,
                                         test_competition):
    """Test purchasing tickets with valid data."""

    # Mock les fonctions loadClubs et loadCompetitions
    mocker.patch('server.loadClubs', return_value=[test_club])
    mocker.patch('server.loadCompetitions', return_value=[test_competition])

    # Reload global data within the test context.
    import server
    server.clubs = [test_club]
    server.competitions = [test_competition]

    response = client.post(
        '/purchasePlaces',
        data={
            'club': test_club['name'],
            'competition': test_competition['name'],
            'places': 1
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Reservation validee." in response.data

def test_purchase_places_saves_club_points(client, mocker, test_club2,
                                           test_competition):
    """Check club's points are saved after a reservation."""
    mocker.patch('server.loadClubs', return_value=[test_club2])
    mocker.patch('server.loadCompetitions', return_value=[test_competition])

    import server
    server.clubs = [test_club2]
    server.competitions = [test_competition]

    # Initial points
    initial_points = int(test_club2['points'])

    # Make a reservation 3 places
    response = client.post(
        '/purchasePlaces',
        data={
            'club': test_club2['name'],
            'competition': test_competition['name'],
            'places': 3
        },
        follow_redirects=True
    )

    # Check booking is validated
    assert b"Reservation validee" in response.data

    # Check points are update
    with open('clubs.json', 'r') as f:
        updated_clubs = json.load(f)
        updated_club = next(c for c in updated_clubs['clubs'] if
                            c['email'] == test_club2['email'])
        # print(updated_club)
        assert int(updated_club['points']) == initial_points - 3  # 10 - 3 = 7

if __name__ == '__main__':
    pytest.main()