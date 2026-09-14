from datetime import datetime, timedelta
import pytest
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_purchase_places_past_competition(client, mocker):
    """Check the route prevents booking for a past competition."""
    test_club = {'name': 'Test club', 'email': 'aaa@club.com', 'points': '10',
                 'reservations': {}}

    past_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    test_competition = {'name': 'Past Competition', 'date': past_date,
                        'numberOfPlaces': '20'}

    mocker.patch('server.loadClubs', return_value=[test_club])
    mocker.patch('server.loadCompetitions', return_value=[test_competition])

    import server
    server.clubs = [test_club]
    server.competitions = [test_competition]

    # Try to book places for past competition
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
    assert b'Reservation validee' not in response.data
    assert (b'Vous ne pouvez pas reserver des places pour une competition '
            b'passee ou fermees dans moins d une heure') in response.data