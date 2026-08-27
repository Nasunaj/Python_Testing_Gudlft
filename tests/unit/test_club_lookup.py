import pytest
from server import loadClubs

# Load the clubs
clubs = loadClubs()

def test_club_found_by_email():
    """Verifies that a club is found using a valid email address."""
    email = 'john@simplylift.co'
    club_matching = [club for club in clubs if club['email'] == email]
    assert len(club_matching) == 1
    assert club_matching[0]['email'] == email

def test_club_not_found_by_email():
    """Test that no club is found with an invalid email."""
    email = 'unknow@gmail.com'
    club_matching = [club for club in clubs if club['email'] == email]
    assert len(club_matching) == 0


