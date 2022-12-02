from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def test_index(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Let's play Boggle!</h1>", html)

    def test_play_game(self):
        with app.test_client() as client:
            resp = client.get('/boggle')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h2>Submit a guess</h2>", html)
            self.assertIn('board', session)

    def test_check_word(self):
        with app.test_client() as client:
            with client.session_transaction() as new_session:
                new_session['board'] = [["D", "O", "G", "D", "O"],
                                        ["D", "O", "G", "D", "O"],
                                        ["D", "O", "G", "D", "O"],
                                        ["D", "O", "G", "D", "O"],
                                        ["D", "O", "G", "D", "O"]]
        resp = client.get('/check?word=dog')
        self.assertEqual(resp.json['answer'], "ok")

    def test_not_a_word(self):
        with app.test_client() as client:
            with client.session_transaction() as new_session:
                new_session['board'] = [["D", "O", "G", "D", "O"],
                                        ["D", "O", "G", "D", "O"],
                                        ["D", "O", "G", "D", "O"],
                                        ["D", "O", "G", "D", "O"],
                                        ["D", "O", "G", "D", "O"]]

        resp = client.get('/check?word=sfkjhfkjkcnknk')
        self.assertEqual(resp.json['answer'], "not-word")

    def test_not_on_board(self):
        with app.test_client() as client:
            with client.session_transaction() as new_session:
                new_session['board'] = [["D", "O", "G", "D", "O"],
                                        ["D", "O", "G", "D", "O"],
                                        ["D", "O", "G", "D", "O"],
                                        ["D", "O", "G", "D", "O"],
                                        ["D", "O", "G", "D", "O"]]

        resp = client.get('/check?word=cat')
        self.assertEqual(resp.json['answer'], "not-on-board")
