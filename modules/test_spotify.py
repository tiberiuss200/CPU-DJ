import unittest
from unittest.mock import Mock, patch
from spotify import main, get_token, get_track_reccomendation, get_uri, uri_to_embed

class TestSpotifyFunctions(unittest.TestCase):
    @patch('spotify.post')
    @patch('spotify.get')
    def test_main(self, mock_get, mock_post):
        # Mocking the external API calls
        mock_get.return_value.content = '{"tracks": [{"name": "Test Song", "external_urls": {"spotify": "test_url"}, "uri": "test_uri"}]}'
        mock_post.return_value.content = '{"access_token": "test_token"}'

        # Mocking state values
        state = Mock()
        state.currentGenre = 'test_genre'
        state.spotify_dict = {"energy": 5, "tempo": 120, "valence": 50}

        with patch('spotify.state', state):
            main()

        # Add your assertions here based on expected behavior

    @patch('spotify.get')
    def test_get_track_recommendation(self, mock_get):
        # Mocking the external API call
        mock_get.return_value.content = '{"tracks": [{"name": "Test Song", "external_urls": {"spotify": "test_url"}, "uri": "test_uri"}]}'

        # Mocking the token
        token = 'test_token'
        with patch('spotify.get_token', return_value=token):
            result = get_track_reccomendation(token, 'test_genre', 5, 120, 50)

        # Add your assertions here based on expected behavior

    @patch('spotify.get')
    def test_get_uri(self, mock_get):
        # Mocking the external API call
        mock_get.return_value.content = '{"tracks": [{"uri": "test_uri"}]}'

        # Mocking the token
        token = 'test_token'
        with patch('spotify.get_token', return_value=token):
            result = get_uri(token, 'test_genre', 5, 120, 50)

        # Add your assertions here based on expected behavior

    def test_uri_to_embed(self):
        uri = 'test_uri'
        result = uri_to_embed(uri)

        # Add your assertions here based on expected behavior

if __name__ == '__main__':
    unittest.main()
