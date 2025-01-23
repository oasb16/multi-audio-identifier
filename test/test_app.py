import unittest
from app import create_app
from flask import url_for

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Multi-Audio Identifier", response.data)

    def test_audio_upload(self):
        with open("tests/sample_audio.wav", "rb") as sample_audio:
            data = {
                'audio': sample_audio,
            }
            response = self.client.post("/", data=data, content_type="multipart/form-data")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Detected Situation", response.data)

if __name__ == "__main__":
    unittest.main()
