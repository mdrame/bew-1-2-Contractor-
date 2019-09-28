from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient() # assigning Mongo Connector Class an instance.
db = client.Playlister # client. is creating a database or using an existing database .
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


# create new documents route ( take you to a html from site)
@app.route('/playlists/new')
def playlists_new():

    return render_template('playlists_new.html', playlist={}, title='New playlist')


# create playlist and diret user to index page.
@app.route('/playlists', methods=['POST'])
def playlists_submit():
    """Submit a new playlist."""
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }
    playlist_id = playlists.insert_one(playlist).inserted_id
    return redirect(url_for('playlists_show', playlist_id=playlist_id))


# showing individual collection by adding _id in parameter.
@app.route('/playlists/<playlist_id>')
def playlists_show(playlist_id):

    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_show.html', playlist=playlist)


@app.route('/Playlists/<playlist_id>/edit')
def playlists_edit(playlist_id):

    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_edit.html', playlist=playlist, title="Edit Playlist")

@app.route('/playlists/<playlist_id>', methods=['POST'])
def playlists_update(playlist_id):

    update_playlist = {
                        'title': request.form.get('title'),
                        'description': request.form.get('description'),
                        'videos': request.form.get('videos').split(),
                        'stars': request.form.get('stars')
    }

    playlists.update_one(   {'_id': ObjectId(playlist_id)},
                            {'$set': updated_playlist})
    return redirect(url_for('playlists_show', playlist_id=playlist_id))


if __name__ == "__main__":
    app.run(debug=True)
