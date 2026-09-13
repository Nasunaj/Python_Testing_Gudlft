# Aucun flask import et aucune redirection (route)
def find_club_by_email(clubs, email):
    """Find a club by email. Return None if no club is found."""
    club_matching = [club for club in clubs if
                     club['email'] == email]
    # Take the first club (normally, there is only one) Otherwise return None
    return club_matching[0] if club_matching else None

def can_club_afford_places(club, places_required):
    """Check if a club has enough points to buy places."""
    return int(club['points']) >= places_required