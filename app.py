from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient() # assigning Mongo Connector Class an instance.
db = client.Playlister # client. is creating a database.
playlists = db.playlists #? creating a collection with in Playlister database 

app = Flask(__name__)

# OUR MOCK ARRAY OF PROJECTS
# mock_playlist = [
#     { 'title': 'Cat Videos', 'description': 'Cats acting weird' },
#     { 'title': '80\'s Music', 'description': 'Don\'t stop believing!' }
# ]


# dash bord / home route
@app.route('/')
def playlists_index():


    return render_template("playlists_index.html", playlists=playlists.find())


# create new documents route
@app.route('/playlists/new')
def playlists_new():

    return render_template('playlists_new.html')


# diret user to view playlist ( in playlist_new there is a creat new ps link)
@app.route('/playlists', methods=['POST'])
def playlists_submit():
    """Submit a new playlist."""
    playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split(),
        'stars': request.form.get('stars')
        }
    playlists.insert_one(playlist)
    return redirect(url_for('playlists_index')) # url_for looks for a func name instead of an actual route


if __name__ == "__main__":
    app.run(debug=True)
