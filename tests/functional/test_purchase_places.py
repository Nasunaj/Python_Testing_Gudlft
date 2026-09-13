import pytest
from server import app
import json

@pytest.fixture
def client():
    """Client Flask pour les tests fonctionnels."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Fixture for a test club
@pytest.fixture
def test_club2():
    return {
        'name': 'Test Club',
        'email': 'test@club.com',
        'points': '5',  # 10 points
        'reservations': {}  # No reservations
    }

# Fixture for a test competition
@pytest.fixture
def test_competition():
    return {
        'name': 'Test Competition',
        'numberOfPlaces': '20'  # 20 available places
    }

def test_user_journey_purchase_without_enough_points(client, mocker,
                                                     test_club2,
                                                     test_competition):
    """Simulates a user journey where a club attempts to purchase
    too many tickets."""
    mocker.patch('server.loadClubs', return_value=[test_club2])
    mocker.patch('server.loadCompetitions', return_value=[test_competition])

    import server
    server.clubs = [test_club2]
    server.competitions = [test_competition]

    # Step 1 : go to the homepage
    response = client.get('/')
    assert response.status_code == 200

    # Step 2 : try to buy places with fewer points than the places the club
    # wants to buy
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
    # Check :
    # 1. the message erreur display
    assert (b"Vous n avez pas assez de points pour acheter ces places" in
            response.data)

    # 2. reservation no validate
    assert b"Reservation validee" not in response.data


def test_user_journey_purchase_with_enough_points(client, mocker,
                                                     test_club2,
                                                     test_competition):
    """Simulates a user journey where a club attempts to purchase
    too many tickets."""
    mocker.patch('server.loadClubs', return_value=[test_club2])
    mocker.patch('server.loadCompetitions', return_value=[test_competition])

    import server
    server.clubs = [test_club2]
    server.competitions = [test_competition]

    # Step 1 : go to the homepage
    response = client.get('/')
    assert response.status_code == 200

    # Step 2 : try to buy places with fewer points than the places the club
    # wants to buy
    places_required = int(test_club2['points']) - 1
    response = client.post(
        '/purchasePlaces',
        data={
            'club': test_club2['name'],
            'competition': test_competition['name'],
            'places': places_required
        },
        follow_redirects=True
    )
    # Check :
    # 1. the message erreur display
    assert (b"Vous n avez pas assez de points pour acheter ces places" not in
            response.data)

    # 2. reservation no validate
    assert b"Reservation validee" in response.data

def test_user_journey_exceed_12_places(client, mocker, test_club2,
                                        test_competition):
    """Simulates a user journey where a club try to book more than 12
    places"""
    import server
    server.clubs = [test_club2]
    server.competitions = [test_competition]

    # Step 1 : go to the homepage
    response = client.get('/')
    assert response.status_code == 200

    # Step 2 : Simulates 10 reservation already for this competition
    test_club2['reservations'] = {test_competition['name']: 10}
    print("gxdfghfhg")
    print(test_club2)

    # Step 3 : try to book 8 places (already 5 places
    response = client.post(
        '/purchasePlaces',
        data={
            'club': test_club2['name'],
            'competition': test_competition['name'],
            'places': 5
        },
        follow_redirects=True
    )

    # Check :
    # 1. Error message disply
    assert b"Vous ne pouvez pas reserver plus de 12 places par competition." in response.data

    # 2. Reservation not validate
    assert b"Reservation validee" not in response.data

    # 3. Reservation not modify
    assert test_club2['reservations'][
               test_competition['name']] == 10  # Toujours 10 places


