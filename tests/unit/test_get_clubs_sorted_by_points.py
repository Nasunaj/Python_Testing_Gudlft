from server_utils import get_clubs_sorted_by_points

def test_get_clubs_sorted_by_points():
    """Test unitaire : Vérifie que les clubs sont triés par points."""
    clubs = [
        {'name': 'Club A', 'points': '5'},
        {'name': 'Club B', 'points': '15'},
        {'name': 'Club C', 'points': '7'}
    ]
    sorted_clubs = get_clubs_sorted_by_points(clubs)
    assert sorted_clubs[0]['name'] == 'Club B'
    assert sorted_clubs[1]['name'] == 'Club C'
    assert sorted_clubs[2]['name'] == 'Club A'
