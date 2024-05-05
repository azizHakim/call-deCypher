import unittest
from app import app


class TestFlaskRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_test_health(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)

        
    def test_submit_question_and_documents(self):
        response = self.app.post('/submit_question_and_documents', 
                                 json={"question": "what are the product design decisions",

  "documents": ["https://storage.googleapis.com/cis-658-hw4.appspot.com/call-log1.txt",
"https://storage.googleapis.com/cis-658-hw4.appspot.com/call-log2.txt",
"https://storage.googleapis.com/cis-658-hw4.appspot.com/call-log3.txt"]
})
        self.assertEqual(response.status_code, 200)


    def test_get_question_and_facts(self):
        response = self.app.get('/get_question_and_facts')
        self.assertEqual(response.status_code, 200)
        # Add more assertions to test the response data
