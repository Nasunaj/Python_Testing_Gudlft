from datetime import datetime, timedelta
import pytest

from server import app

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
        'numberOfPlaces': '20',  # 20 available places
        'date': '2026-09-13 13:15:33'
    }

def test_user_journey_purchase_past_competition(client,mocker,
                                                test_club2,
                                                test_competition):
    """Simulate a user journey for a past competition"""
    mocker.patch('server.loadClubs', return_value=[test_club2])
    mocker.patch('server.loadCompetitions', return_value=[test_competition])

    import server
    server.clubs = [test_club2]
    server.competitions = [test_competition]

    # Step 1 : go to the homepage
    response = client.get('/')
    assert response.status_code == 200

    # Step 2 : Try to book a past competition
    response = client.post(
        '/purchasePlaces',
        data={
            'club': test_club2['name'],
            'competition': test_competition['name'],
            'places': 1
        },
        follow_redirects=True
    )

    # Check :
    # 1. Error message display
    assert (b"Vous ne pouvez pas reserver des places pour une competition "
            b"passee ou fermees dans moins d une heure") in response.data

    # 2. Booking should not validate
    assert b"Reservation validee" not in response.data
