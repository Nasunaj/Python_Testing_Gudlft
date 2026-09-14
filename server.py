import json
from flask import Flask,render_template,request,redirect,flash,url_for
from server_utils import find_club_by_email, can_club_afford_places, \
    can_club_book_places, has_competition_enough_places, save_clubs_to_json, \
    save_competitions_to_json


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
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition_name = request.form['competition']

    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]

    # Check if the competition or club exists.
    if not competition or not club:
        flash("Compétition ou club introuvable.")
        return render_template('welcome.html', club=club,
                               competitions=competitions)
    competition = competitions[0]
    club = clubs[0]
    placesRequired = int(request.form['places'])
    print(placesRequired)

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

    if 'reservations' not in club:
        club['reservations'] = {}
    club['reservations'][competition_name] = (
            club['reservations'].get(competition['name'], 0) + placesRequired)

    # Save changes to the JSON files
    save_clubs_to_json(clubs)
    save_competitions_to_json(competitions)

    flash("Reservation validee.")
    return render_template('welcome.html', club=club,
                           competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)