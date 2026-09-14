import json
from datetime import datetime, timedelta

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

def can_club_book_places(club, competition_name, places_required):
    """Check if a club can reserve places without exceeding 12 places by
    competition"""
    current_reservations = club.get('reservations', {}).get(competition_name,
                                                            0)
    return current_reservations + places_required <= 12

def has_competition_enough_places(competition, places_required):
    """Check if a competition has enough available places."""
    return int(competition['numberOfPlaces']) >= places_required

def save_clubs_to_json(clubs, filename='clubs.json'):
    """Saves the list of clubs to a JSON file."""
    with open(filename, 'w') as f:
        json.dump({'clubs': clubs}, f)

def save_competitions_to_json(competitions, filename='competitions.json'):
    """aves the list of competitions to a JSON file"""
    with open(filename, 'w') as f:
        json.dump({'competitions': competitions}, f)

def is_competition_open(competition):
    """Check if a competition is open (date not yet passed and no in 1 hour)."""
    competition_date = datetime.strptime(competition['date'],
                                         '%Y-%m-%d %H:%M:%S')
    return competition_date >= datetime.now() + timedelta(hours=1)

def get_clubs_sorted_by_points(clubs):
    """Returns a list of clubs sorted by points."""
    return sorted(clubs, key=lambda club: int(club['points']), reverse=True)

# Additionnal functional to increase coverage
def find_competition_by_name(competitions, name):
    """Find a compétition par by name. Retourne None if not found."""
    competition_matching = [c for c in competitions if c['name'] == name]
    return competition_matching[0] if competition_matching else None

def find_club_by_name(clubs, name):
    """Find a compétition par by name. Retourne None if not found."""
    club_matching = [c for c in clubs if c['name'] == name]
    return club_matching[0] if club_matching else None

def is_missing_club_or_competition(club, competition):
    """Check if a club or competition missing."""
    return not competition or not club

def ensure_reservations_exists(club):
    """Ensure reservations exists"""
    if 'reservations' not in club:
        club['reservations'] = {}