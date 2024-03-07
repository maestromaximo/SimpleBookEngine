import unittest
from main import query_openai_with_tools

class TestQueryOpenAIWithTools(unittest.TestCase):
    def test_no_context(self):
        query = "Hello, how are you?"
        expected_response = {
            "role": "assistant",
            "content": "I'm doing well, thank you!"
        }
        expected_context = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query},
            expected_response
        ]
        
        response, context = query_openai_with_tools(query)
        
        self.assertEqual(response, expected_response)
        self.assertEqual(context, expected_context)
    
    def test_with_context(self):
        query = "What's the weather like today?"
        context = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, how are you?"},
            {"role": "assistant", "content": "I'm doing well, thank you!"}
        ]
        expected_response = {
            "role": "assistant",
            "content": "I'm sorry, I don't have access to weather information."
        }
        expected_context = context + [
            {"role": "user", "content": query},
            expected_response
        ]
        
        response, context = query_openai_with_tools(query, context=context)
        
        self.assertEqual(response, expected_response)
        self.assertEqual(context, expected_context)

if __name__ == '__main__':
    unittest.main()