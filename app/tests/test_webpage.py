import unittest
from app import app


class TestFlaskRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_test_health(self):
        response = self.app.get('/')
        
        page_text = b'Call Decypher: Powered by GPT-4 and RAG' in response.data
        self.assertEqual(page_text, True)

        
    def test_submit_question_and_documents(self):
        response = self.app.post('/response', 
                                 data={"question": "what are the product design decisions",

  "url1": "https://storage.googleapis.com/cis-658-hw4.appspot.com/call-log1.txt",
"url2": "https://storage.googleapis.com/cis-658-hw4.appspot.com/call-log2.txt",
"url3": "https://storage.googleapis.com/cis-658-hw4.appspot.com/call-log3.txt"
})
        self.assertEqual(response.status_code, 200)

