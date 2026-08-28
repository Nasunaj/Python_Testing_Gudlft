import json
from flask import Flask,render_template,request,redirect,flash,url_for


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
    # club = [club for club in clubs if club['email'] == request.form['email']][0]
    # Remove [0], as the list type is being retained.
    club_matching = [club for club in clubs if club['email'] == request.form['email']]
    print(club_matching)

    # If no club matches
    if not club_matching:
        flash('Email inconnu.')
        return redirect(url_for('index'))

    # Otherwise, take the first club (normally, there is only one).
    club = club_matching[0]
    return render_template('welcome.html',club=club,competitions=competitions)


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
    if int(club['points']) < placesRequired:
        flash("Vous n avez pas assez de points pour acheter ces places.")
        return render_template('welcome.html', club=club,
                               competitions=competitions)
    # check if competition has enough place
    if int(competition['numberOfPlaces']) < placesRequired:
        flash("Il n y a pas assez de places pour cette competition.")
        return render_template('welcome.html', club=club,
                               competitions=competitions)
    # Check if placeRiquered <= 12
    current_reservations = club.get('reservations',{}).get(competition_name, 0)
    if current_reservations + placesRequired > 12:
        flash("Vous ne pouvez pas reserver plus de 12 places par competition.")
        return render_template('welcome.html', club=club,
                               competitions=competitions)

    # Update club points and competition standings
    club['points'] = f"{int(club['points']) - placesRequired}"
    competition['numberOfPlaces'] = f"{int(competition['numberOfPlaces']) - placesRequired}"

    if 'reservations' not in club:
        club['reservations'] = {}
    club['reservations'][competition_name] = current_reservations + placesRequired

    # Save changes to the JSON files
    with open('clubs.json', 'w') as c:
        json.dump({'clubs': clubs}, c)
    with open('competitions.json', 'w') as comps:
        json.dump({'competitions': competitions}, comps)

    flash("Reservation validee.")
    return render_template('welcome.html', club=club,
                           competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)