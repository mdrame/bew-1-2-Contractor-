from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.exceptions import NotFound
import os

client = MongoClient() # assigning Mongo Connector Class an instance.
db = client.Playlister #? what is the Playlists
playlists = db.playlists #? what does .playlists do?

app = Flask(__name__)

# OUR MOCK ARRAY OF PROJECTS
playlists = [
    { 'title': 'Cat Videos', 'description': 'Cats acting weird' },
    { 'title': '80\'s Music', 'description': 'Don\'t stop believing!' }
]


# dash bord / home route
@app.route('/')
def index():


    return render_template("playlists_index.html", playlists=playlists)


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
        'videos': request.form.get('videos').split()
    }
    playlists.insert_one(playlist)
    return redirect(url_for('playlists_index'))


if __name__ == "__main__":
    app.run(debug=True)
