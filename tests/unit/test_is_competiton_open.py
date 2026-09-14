from server_utils import is_competition_open
from datetime import datetime, timedelta

def test_competition_is_open():
    """Test competiton open in the future."""
    future_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    competition_date = {'date': future_date}
    assert is_competition_open(competition_date) is True

def test_competition_is_closed():
    """Test competiton closed in the past"""
    past_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    competition_date = {'date': past_date}
    assert is_competition_open(competition_date) is False