import unittest
import json
from app import app, db, User, Task

class BasicTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        cls.client = app.test_client()
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()

    def test_signup(self):
        response = self.client.post('/api/signup', json={
            'username': 'testuser',
            'password': 'testpass',
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Signup successful', response.json['message'])

    def test_signin(self):
        self.client.post('/api/signup', json={
            'username': 'testuser',
            'password': 'testpass',
            'email': 'test@example.com'
        })
        response = self.client.post('/api/signin', json={
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Signin successful', response.json['message'])

    def test_add_task(self):
        self.client.post('/api/signup', json={
            'username': 'testuser',
            'password': 'testpass',
            'email': 'test@example.com'
        })
        self.client.post('/api/signin', json={
            'username': 'testuser',
            'password': 'testpass'
        })
        response = self.client.post('/api/todo', json={'task': 'Test task'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Task added successfully', response.json['message'])

    def test_get_tasks(self):
        self.client.post('/api/signup', json={
            'username': 'testuser',
            'password': 'testpass',
            'email': 'test@example.com'
        })
        self.client.post('/api/signin', json={
            'username': 'testuser',
            'password': 'testpass'
        })
        self.client.post('/api/todo', json={'task': 'Test task'})
        response = self.client.get('/api/todo')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['tasks']), 1)
        self.assertEqual(response.json['tasks'][0]['task'], 'Test task')

if __name__ == "__main__":
    unittest.main()