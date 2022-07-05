from cgitb import html
from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def test_root(self):
        with app.test_client() as client:
            res = client.get('/')
            html=res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIsNotNone(session["board"])
            self.assertIn("<h1>BOGGLE</h1>",html)

        #     import pdb;
        #     pdb.set_trace()

    def test_check_word(self):
        with app.test_client() as client:
            res = client.get('/check-word?word=outer')
            html=res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<p>Added:outer</p>",html)
            self.assertIn("num_play",res.data)
            self.assertEqual(res.json['result'], 'ok')


    def test_None_valid_word(self):
        with app.test_client() as client:
            res = client.get('/check-word?word=chipchipsipsip')
            self.assertEqual(res.json['result'], 'not-word')



    def test_show_score(self):
        with app.test_client() as client:
            res = client.post('/show-score', data={'word': 'outer'})
            html=res.get_data(as_text=True)

            self.assertIn("highscore",res.data)


