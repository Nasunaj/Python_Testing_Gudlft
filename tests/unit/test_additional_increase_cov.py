from server_utils import is_missing_club_or_competition, \
    ensure_reservations_exists


def test_is_missing_club_or_competition_none():
    """Club or compétition is None."""
    assert is_missing_club_or_competition(None, {'name': 'Test'}) is True
    assert is_missing_club_or_competition({'name': 'Test'}, None) is True

def test_is_missing_club_or_competition_empty():
    """TClub or compétition is empty."""
    assert is_missing_club_or_competition({}, {'name': 'Test'}) is True
    assert is_missing_club_or_competition({'name': 'Test'}, {}) is True

def test_is_missing_club_or_competition_valid():
    """Club and compétition are validated."""
    club = {'name': 'Test Club'}
    competition = {'name': 'Test Competition'}
    assert is_missing_club_or_competition(club, competition) is False

def test_ensure_reservations_exists():
    """Test unitaire : Vérifie que 'reservations' est initialisé si absent."""
    test_club = {'name': 'Test Club', 'email': 'test@club.com', 'points': '15'}
    ensure_reservations_exists(test_club)
    assert 'reservations' in test_club
    assert test_club['reservations'] == {}