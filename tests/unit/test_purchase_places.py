import os
import json
from server_utils import can_club_afford_places, can_club_book_places, \
    has_competition_enough_places, save_clubs_to_json, \
    save_competitions_to_json


def test_club_has_enough_points():
    """Test that a club has enough points."""
    club = {"name": "Simply Lift", "email": "john@simplylift.co",
            "points": "7", "reservations": {"Spring Festival": 10}}
    places_required = 5
    assert can_club_afford_places(club, places_required) is True

def test_club_not_enough_points():
    """Test that a club does not have enough points."""
    # club = clubs[0]
    club = {"name": "Simply Lift", "email": "john@simplylift.co",
            "points": "3", "reservations": {"Spring Festival": 10}}
    places_required = int(club['points']) + 1
    assert can_club_afford_places(club, places_required) is False

def test_club_reservations_under_limit():
    """Check that a club can reserve up to 12 places per competition."""
    club = {"name": "Simply Lift", "email": "john@simplylift.co",
            "points": "15", "reservations": {"Spring Festival": 5}}
    competition_name = 'Spring Festival'
    places_required = 7 # 5 + 7 = 12
    assert (can_club_book_places(club, competition_name, places_required) is
            True)

def test_club_reservations_exceed_limit():
    """Test that a club cannot exceed 12 places per competition."""
    club = {"name": "Simply Lift", "email": "john@simplylift.co",
            "points": "15", "reservations": {"Spring Festival": 10}}
    competition_name = 'Spring Festival'
    places_required = 3
    assert (can_club_book_places(club, competition_name, places_required) is
            False)

def test_competition_not_enough_places():
    """Competition has not enough places."""
    competition = {'numberOfPlaces': '5'}
    places_required = 10
    assert has_competition_enough_places(competition, places_required) is False

def test_competition_has_enough_places():
    """Competition has enough places."""
    competition = {'numberOfPlaces': '5'}
    places_required = 4
    assert has_competition_enough_places(competition, places_required) is True

def test_save_clubs_to_json():
    """Ckeck clubs are saved in clubs.json."""

    test_clubs = [{'name': 'Test_club', 'email': 'aaa@club.com', 'points': '6'}]

    # Sauvegarder in a temporary file for test
    test_filename = 'test_clubs.json'
    save_clubs_to_json(test_clubs, test_filename)

    # check if the file exists and has the data
    assert os.path.exists(test_filename)
    with open(test_filename, 'r') as f:
        saved_data = json.load(f)
    assert saved_data['clubs'] == test_clubs
    # print(saved_data)

    # delete temporary file
    os.remove(test_filename)

def test_save_competitions_to_json():
    """Ckeck competitions are saved in competitions.json."""

    test_competitions = [{'name': 'Test_competition',
                          'date': '2020-03-27 10:00:00','numberOfPlaces': '6'}]

    # Sauvegarder in a temporary file for test
    test_filename = 'test_clubs.json'
    save_competitions_to_json(test_competitions, test_filename)

    # check if the file exists and has the data
    assert os.path.exists(test_filename)
    with open(test_filename, 'r') as f:
        saved_data = json.load(f)
    assert saved_data['competitions'] == test_competitions
    # print(saved_data)

    # delete temporary file
    os.remove(test_filename)


