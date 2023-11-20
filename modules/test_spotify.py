# run this code:
# on linux:
# venv/bin/activate

# on windows:
# venv/Scripts/activate

# on mac:
# source .venv/bin/activate


# cd ./modules
# python3 -m unittest test_spotify.py

import unittest
from unittest.mock import Mock, patch
from spotify import main, get_token, get_track_reccomendation, get_uri, uri_to_embed

class TestSpotifyFunctions(unittest.TestCase):

    @patch('spotify.get_uri')
    @patch('spotify.get_track_reccomendation')
    def test_main(self, mock_get_track_reccommendation, mock_get_uri):
        print("\ntesting MAIN....")
        # Mocking the external API calls
        mock_get_track_reccommendation.return_value = "test_uri1"
        mock_get_uri.return_value.content = '{"access_token": "Balls"}'

        # Mocking state values
        state = Mock()
        state.currentGenre = 'test_genre'
        state.spotify_dict = {"energy": 5, "tempo": 120, "valence": 50}
        songs = "empty"

        with patch('spotify.state', state):
            songs = main()

        print(songs)

        self.assertIs(songs, "test_uri1")
        self.assertTrue(mock_get_uri.called)

        # Add your assertions here based on expected behavior
        print("\ntest MAIN complete!")

    """
        def test_main(self):
        print("\ntesting MAIN....")

        # Mocking the external API calls
        mock_get.return_value.content = '{"tracks": [{"name": "Test Song1", "external_urls": {"spotify": "test_url1"}, "uri": "test_uri1"},{"name": "Test Song 2", "external_urls": {"spotify": "test_url2"}, "uri": "test_uri2"}]}'
        mock_post.return_value.content = '{"access_token": "test_token"}'
        mock_get_uri.return_value.content = '{"access_token": "Balls"}'

        # Mocking state values
        state = Mock()
        state.currentGenre = 'test_genre'
        state.spotify_dict = {"energy": 5, "tempo": 120, "valence": 50}

        with patch('spotify.state', state):
            with patch('spotify.get_uri', return_value='test_uri'):
                main()

        # Add assertions to check the expected behavior
        self.assertTrue(mock_get.called)
        self.assertTrue(mock_post.called)
        self.assertTrue(mock_get_uri.called)
        # Add more assertions based on the expected behavior of the main function

        print("\ntest MAIN complete!")
    """


    @patch('spotify.get')
    def test_get_track_recommendation(self, mock_get):
        print("\ntesting GET TRACK RECCOMMENDATION...")

        # Mocking the external API call
        mock_get.return_value.content = '{"tracks": [{"name": "Test Song1", "external_urls": {"spotify": "test_url1"}, "uri": "test_uri1"}]}'

        # Mocking the token
        token = 'test_token'
        with patch('spotify.get_token', return_value=token):
            result = get_track_reccomendation(token, 'test_genre', 5, 120, 50)
        
        expected_song_result = "test_uri1"
        self.assertEqual(result, expected_song_result)
        # Add your assertions here based on expected behavior

        print("\ntest GET TRACK RECCOMMENDATION complete!")

    @patch('spotify.get')
    def test_get_uri(self, mock_get):
        # Mocking the external API call
        print("\ntesting GET URI...")
        mock_get.return_value.content = '{"tracks": [{"uri": "test_uri"}]}'

        # Mocking the token
        token = 'test_token'
        with patch('spotify.get_token', return_value=token):
            result = get_uri(token, 'test_genre', 5, 120, 50)

        # Add your assertions here based on expected behavior
        
        print("\ntest GET URI complete!")
        

    def test_uri_to_embed(self):
        print("\ntesting URI TO EMBED...")

        uri = 'test_uri'
        result = uri_to_embed(uri)

        # Add your assertions here based on expected behavior
        self.assertTrue(result.endswith("embed.html"))

        print("\ntest URI TO EMBED complete!")

if __name__ == '__main__':
    unittest.main()
