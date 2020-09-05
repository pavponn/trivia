import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['categories']))

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
    
    def test_get_questions_invalid_page_404_error(self):
        res = self.client().get('/questions?page=11013')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Not Found")
    
    def test_delete_question(self):
        question = Question('test', 'test',  1, 1)
        question.insert()
        res = self.client().delete(f'/questions/{question.id}')
        data = json.loads(res.data)
        question_deleted = Question.query.filter(Question.id == question.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted_question'], question.id)
        self.assertIsNone(question_deleted)
    
    def test_delete_question_invalid_question_422_error(self):
        res = self.client().delete('/questions/9999999999')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Unprocessable Entity")
    
    def test_post_question(self):
        question = {
            'question': 'test',
            'answer': 'test',
            'category' : 1,
            'difficulty': 1
        }
        size = Question.query.count()
        res = self.client().post('/questions', json=question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(size + 1, Question.query.count())
    
    def test_post_question_invalid_question_422_error(self):
        question = {}
        size = Question.query.count()
        res = self.client().post('/questions', json=question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Unprocessable Entity")
        self.assertEqual(size, Question.query.count())

    def test_get_questions_by_category(self):
        category_id = 1
        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['current_category'], category_id)

    def test_get_questions_by_category_invalid_category_404_error(self):
        category_id = "category"
        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Not Found")
    
    def test_play_game(self):
        game_state = {
            'quiz_category': {'type': 'click', 'id': 0}, 
            'previous_questions': []
        }
        res = self.client().post('/quizzes', json=game_state)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
    
    def test_play_game_invalid_quiz_category_422_error(self):
        game_state = {}
        res = self.client().post('/quizzes', json=game_state)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Unprocessable Entity")

    def test_search_questions(self):
        search = { 'searchTerm': 'world'}
        res = self.client().post('/questions/search', json=search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']))
        self.assertIsNotNone((data['total_questions']))
    
    def test_search_questions_invalid_search_400_error(self):
        search = {}
        res = self.client().post('/questions/search', json=search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Unprocessable Entity")



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()