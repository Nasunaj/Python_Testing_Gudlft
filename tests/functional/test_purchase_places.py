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
    mocker.patch('server.loadClubs', return_value=[test_club2])
    mocker.patch('server.loadCompetitions', return_value=[test_competition])
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

def test_user_journey_purchase_without_enough_competition_places(client,
                                                                 mocker,
                                                                 test_club2,
                                                                 test_competition):
    """Simulate a user journey where a competition has not enough places."""
    mocker.patch('server.loadClubs', return_value=[test_club2])
    mocker.patch('server.loadCompetitions', return_value=[test_competition])

    import server
    server.clubs = [test_club2]
    server.competitions = [test_competition]
    test_competition['numberOfPlaces'] = 3
    test_club2['points'] = 4
    required_places = int(test_competition['numberOfPlaces'])+1

    # Step 1 : go to the homepage
    response = client.get('/')
    assert response.status_code == 200

    # Step 2 : try to book more places than available in the competition
    response = client.post(
        '/purchasePlaces',
        data={
            'club': test_club2['name'],
            'competition': test_competition['name'],
            'places': required_places
        },
        follow_redirects=True
    )

    # Check :
    # 1. Error message display
    assert b"Il n y a pas assez de places pour cette competition" in response.data

    # 2. the booking not validate
    assert b"Reservation validee" not in response.data

    # 3. the number of competiton available places not modify (always 3)
    assert int(test_competition['numberOfPlaces']) == 3

def test_user_journey_purchase_with_enough_competition_places(client,
                                                                 mocker,
                                                                 test_club2,
                                                                 test_competition):
    """Simulate a user journey where a competition has not enough places."""
    mocker.patch('server.loadClubs', return_value=[test_club2])
    mocker.patch('server.loadCompetitions', return_value=[test_competition])

    import server
    server.clubs = [test_club2]
    server.competitions = [test_competition]
    test_competition['numberOfPlaces'] = 3
    test_club2['points'] = 4
    required_places = int(test_competition['numberOfPlaces'])-1
    available_places = int(test_competition['numberOfPlaces']) - required_places

    # Step 1 : go to the homepage
    response = client.get('/')
    assert response.status_code == 200

    # Step 2 : try to book more places than available in the competition
    response = client.post(
        '/purchasePlaces',
        data={
            'club': test_club2['name'],
            'competition': test_competition['name'],
            'places': required_places
        },
        follow_redirects=True
    )

    # Check :
    # 2. the booking not validate
    assert b"Reservation validee" in response.data

    # 3. the number of competiton available places is modified
    assert int(test_competition['numberOfPlaces']) == available_places

def test_user_journey_purchase_saves_points(client, mocker, test_club2,
                                            test_competition):
    """Simulate a user journey and check the points are saved"""
    mocker.patch('server.loadClubs', return_value=[test_club2])
    mocker.patch('server.loadCompetitions', return_value=[test_competition])

    import server
    server.clubs = [test_club2]
    server.competitions = [test_competition]
    initial_points = int(test_club2['points'])

    # Step 1 : go to the homepage
    response = client.get('/')
    assert response.status_code == 200

    # step 2 : make a reservation 3 places
    response = client.post(
        '/purchasePlaces',
        data={
            'club': test_club2['name'],
            'competition': test_competition['name'],
            'places': 3
        },
        follow_redirects=True
    )

    # Check :
    # 1. booking should be validate
    assert b"Reservation validee" in response.data

    # 2. points should be update in clubs.json
    with open('clubs.json', 'r') as f:
        updated_clubs = json.load(f)
    updated_club = next(c for c in updated_clubs['clubs'] if c['name'] == test_club2['name'])
    assert int(updated_club['points']) == initial_points - 3