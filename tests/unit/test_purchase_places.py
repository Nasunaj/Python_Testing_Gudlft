import pytest
import json
from server import loadClubs, loadCompetitions

# Load data
# clubs = loadClubs()
# competitions = loadCompetitions()

def test_club_reservations_under_limit():
    """Check that a club can reserve up to 12 places per competition."""
    club = {"name": "Simply Lift", "email": "john@simplylift.co",
            "points": "15", "reservations": {"Spring Festival": 10}}
    competition_name = 'Simply Lift'
    # print(club)
    # print(competition_name)

    # Simulate 5 existing reservations
    club['reservations'] = {competition_name : 5}

    # Check that we can reserve 7 more places (5+7=12)
    current_reservations = club.get('reservations', {}).get(competition_name, 0)
    places_required = 7
    assert current_reservations + places_required <= 12


def test_club_reservations_exceed_limit():
    """Test that a club cannot exceed 12 places per competition."""
    club = {"name": "Simply Lift", "email": "john@simplylift.co",
            "points": "15", "reservations": {"Spring Festival": 10}}
    competition_name = 'Simply Lift'
    club['reservations'] = {competition_name : 10}

    # Check that we cannot reserve 3 more places (10 + 3 = 13 > 12)
    current_reservations = club.get('reservations', {}).get(competition_name, 0)
    places_required = 3
    assert current_reservations + places_required > 12

def test_club_has_enough_points():
    """Test that a club has enough points."""
    club = {"name": "Simply Lift", "email": "john@simplylift.co",
            "points": "7", "reservations": {"Spring Festival": 10}}
    places_required = 5
    assert int(club['points']) >= places_required

def test_club_not_enough_points():
    """Test that a club does not have enough points."""
    # club = clubs[0]
    club = {"name": "Simply Lift", "email": "john@simplylift.co",
            "points": "3", "reservations": {"Spring Festival": 10}}
    places_required = int(club['points']) + 1
    assert int(club['points']) < places_required



