import json
from flask import Flask,render_template,request,redirect,flash,url_for
from server_utils import find_club_by_email, can_club_afford_places, \
    can_club_book_places, has_competition_enough_places, save_clubs_to_json, \
    save_competitions_to_json, is_competition_open, get_clubs_sorted_by_points, \
    is_missing_club_or_competition, find_competition_by_name, \
    find_club_by_name, ensure_reservations_exists


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    email = request.form['email']
    club = find_club_by_email(clubs, email)
    if not club:
        flash('Email inconnu.')
        return redirect(url_for('index'))
    return render_template('welcome.html',
                           club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = find_club_by_name(clubs, club)
    foundCompetition = find_competition_by_name(competitions, competition)
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,
                               competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html',
                               club={'name': club, 'email': '', 'points': '0'},
                               competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition_name = request.form['competition']
    club_name = request.form['club']

    competition = find_competition_by_name(competitions, competition_name)
    club = find_club_by_name(clubs, club_name)

    # (Additional for coverage) Check if the competition or club exists.
    if is_missing_club_or_competition(club, competition):
        flash("Competition ou club introuvable.")
        return render_template('welcome.html', club=club,
                               competitions=competitions)
    # competition = competitions[0]
    # club = clubs[0]
    placesRequired = int(request.form['places'])
    print(placesRequired)

    # Check if the competition is open (with a hour lead time beforehand)
    if not is_competition_open(competition):
        flash("Vous ne pouvez pas reserver des places pour une competition "
              "passee ou fermees dans moins d une heure.")
        return render_template('welcome.html', club=club,
                                       competitions=competitions)

    # check if club has enough points
    if can_club_afford_places(club, placesRequired) is False:
        flash("Vous n avez pas assez de points pour acheter ces places.")
        return render_template('welcome.html', club=club,
                               competitions=competitions)

    # Check if placeRiquered <= 12
    if not can_club_book_places(club, competition['name'], placesRequired):
        flash("Vous ne pouvez pas reserver plus de 12 places par competition.")
        return render_template('welcome.html', club=club,
                               competitions=competitions)

    # check if competition has enough place
    if not has_competition_enough_places(competition, placesRequired):
        flash("Il n y a pas assez de places pour cette competition.")
        return render_template('welcome.html', club=club,
                               competitions=competitions)

    # Update club points and competition standings
    club['points'] = f"{int(club['points']) - placesRequired}"
    competition['numberOfPlaces'] = f"{int(competition['numberOfPlaces']) - placesRequired}"

    # if 'reservations' not in club:
    #     club['reservations'] = {}
    ensure_reservations_exists(club)
    club['reservations'][competition_name] = (
            club['reservations'].get(competition['name'], 0) + placesRequired)

    # Save changes to the JSON files
    save_clubs_to_json(clubs)
    save_competitions_to_json(competitions)

    flash("Reservation validee.")
    return render_template('welcome.html', club=club,
                           competitions=competitions)


# TODO: Add route for points display
@app.route('/points')
def show_points():
    """Display public board points of clubs"""
    sorted_clubs = get_clubs_sorted_by_points(clubs)
    return render_template('points.html', clubs=sorted_clubs)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)