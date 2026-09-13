from serveur_utils import find_club_by_email

def test_club_found_by_email():
    """Verifies that a club is found using a valid email address."""
    clubs = [{'email': 'john@simplylift.co', 'name': 'John Club'}]
    email = 'john@simplylift.co'
    club = find_club_by_email(clubs, email)
    assert club is not None
    assert club['email'] == email

def test_club_not_found_by_email():
    """Test that no club is found with an invalid email."""
    clubs = [{'email': 'john@simplylift.co', 'name': 'John Club'}]
    email = 'unknow@gmail.com'
    club = find_club_by_email(clubs, email)
    assert club is None


