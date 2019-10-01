
# tests.py

from unittest import TestCase, main as unittest_main
from bson.objectid import ObjectId

sample_playlist_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_playlist = {
    'title': 'Cat Videos',
    'description': 'Cats acting weird',
    'videos': [
        'https://youtube.com/embed/hY7m5jjJ9mM',
        'https://www.youtube.com/embed/CQ85sUNBK7w'
    ]
}
sample_form_data = {
    'title': sample_playlist['title'],
    'description': sample_playlist['description'],
    'videos': '\n'.join(sample_playlist['videos'])
}

class PlaylistsTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_new(self):
        """Test the new playlist creation page."""
        result = self.client.get('/playlists/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'New Playlist', result.data)

     @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_playlist(self, mock_find):
        """Test editing a single playlist."""
        mock_find.return_value = sample_playlist

        result = self.client.get(f'/playlists/{sample_playlist_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Cat Videos', result.data)

    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_playlist(self, mock_insert):
        """Test submitting a new playlist."""
        result = self.client.post('/playlists', data=sample_form_data)

        # After submitting, should redirect to that playlist's page
        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_playlist)

    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_playlist(self, mock_update):
        result = self.client.post(f'/playlists/{sample_playlist_id}', data=sample_form_data)

        self.assertEqual(result.status, '302 FOUND')
        mock_update.assert_called_with({'_id': sample_playlist_id}, {'$set': sample_playlist})

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_playlist(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/playlists/{sample_playlist_id}/delete', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_playlist_id})
    

if __name__ == '__main__':
    unittest_main()

if __name__ == '__main__':
    unittest_main()