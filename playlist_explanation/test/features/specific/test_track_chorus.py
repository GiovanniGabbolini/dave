import unittest
from src.features.specific.track_chorus import track_chorus


class TestTrackChorus(unittest.TestCase):

    def test_track_chorus(self):
        c = "[chorus]\naa\nbbbb\naa\nbbbb\naa\nbbb\n[somethingelse]\naa\naa\n[aachorusverynice   ]\nbbbb"
        self.assertEqual(track_chorus(c, recreate=True), "bbbb")

        c = "[choruses]"
        self.assertEqual(track_chorus(c, recreate=True), None)

        c = "aaa\naaa\naaaa"
        self.assertEqual(track_chorus(c, recreate=True), None)

        c = "[chorus]\naa\nbbbb\naa\nbbbb\naa\nbbb\n[somethingelse]\naa\n[aachorusverynice   ]\nbbbb\naa\n  [hook]\naa"
        self.assertEqual(track_chorus(c, recreate=True), "aa")
