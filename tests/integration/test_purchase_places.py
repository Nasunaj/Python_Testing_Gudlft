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

# def test_purchase_places_saves_points_to_json(client):
#     """Test that club's points and reservations number are saved in clubs.json after reservation and
#     save numberOfPlaces in competitions.json."""
#     # Sauvegarder le chemin du fichier clubs.json original
#     clubs_file_path = 'clubs.json'
#     # competition
#     competitions_file_path = 'competitions.json'
#
#     # Lire le contenu initial du fichier clubs.json
#     with open(clubs_file_path, 'r') as f:
#         initial_clubs = json.load(f)
#
#     # competition
#     with open(competitions_file_path, 'r') as f:
#         initial_competitions_file_path = json.load(f)
#
#     # Trouver un club avec assez de points pour faire une réservation
#     club = initial_clubs['clubs'][0]  # Prenons le premier club
#     initial_points = int(club['points'])
#
#
#     # competition
#     competition = initial_competitions_file_path['competitions'][0]
#     initial_numberOfPlaces = int(competition['numberOfPlaces'])
#
#     initial_reservation = int(club['reservations'][competition['name']])
#
#     # Faire une réservation avec ce club (ex: 1 place)
#     competition = {'name': 'Test Competition', 'numberOfPlaces': '20'}
#     places_required = 1
#
#     # Envoyer une requête POST pour simuler la réservation
#     response = client.post(
#         '/purchasePlaces',
#         data={
#             'club': club['name'],
#             'competition': competition['name'],
#             'places': places_required
#         },
#         follow_redirects=True
#     )
#
#     # Lire à nouveau le fichier clubs.json pour vérifier la mise à jour
#     with open(clubs_file_path, 'r') as f:
#         updated_clubs = json.load(f)
#
#     with open(competitions_file_path, 'r') as f:
#         updated_competitions = json.load(f)
#
#     # Trouver le club mis à jour dans le fichier
#     updated_club = next(c for c in updated_clubs['clubs'] if c['name'] == club['name'])
#
#     # competition
#     updated_competition = next(c for c in updated_competitions['competitions'] if c['name'] == competition['name'])
#     print(f"club : initial_points : {initial_points} - places_required : {places_required} = {updated_club['points']}")
#     print(f"competition : initial_numberOfPlaces : {initial_numberOfPlaces} - places_required : {places_required} = {updated_competition['numberOfPlaces']}")
#
#     #Vérifier que les points ont été décrémentés
#     assert int(updated_club['points']) == initial_points - places_required
#     # competition
#     assert int(updated_competition['numberOfPlaces']) == initial_numberOfPlaces - places_required
#     assert int(updated_club['reservations'][competition['name']]) == initial_reservation + places_required

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

def test_purchase_places_exceed_12_places(client, mocker, test_club,
                                          test_competition):
    """Test that a club cannot exceed 12 places per competition."""

    mocker.patch('server.loadClubs', return_value=[test_club])
    mocker.patch('server.loadCompetitions', return_value=[test_competition])

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

def test_purchase_places_exceed_cumulative_12_places(client, mocker, test_club,
                                                     test_competition):
    """Test that a club cannot exceed a cumulative total of 12 places."""
    mocker.patch('server.loadClubs', return_value=[test_club])
    mocker.patch('server.loadCompetitions', return_value=[test_competition])

    import server
    server.clubs = [test_club]
    server.competitions = [test_competition]

    test_club['reservations'] = {test_competition['name'] : 5}
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
    assert b"Great-booking complete!" not in response.data
    assert response.status_code == 200
    assert (b"Il n y a pas assez de places pour cette competition" in
            response.data)



if __name__ == '__main__':
    pytest.main()