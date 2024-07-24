# tests/test_tester.py

import unittest
from unittest.mock import patch, mock_open
from user_agent_filter.tester import filter_user_agents, UserAgentTester
import os

class TestUserAgentTester(unittest.TestCase):

    @patch('user_agent_filter.tester.requests.Session.get')
    def test_check_user_agent_success(self, mock_get):
        mock_get.return_value.status_code = 200
        tester = UserAgentTester(test_url="https://www.example.com")
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        headers = {'User-Agent': user_agent}
        result = tester.check_user_agent(user_agent, headers)
        self.assertTrue(result)

    @patch('user_agent_filter.tester.requests.Session.get')
    def test_check_user_agent_failure(self, mock_get):
        mock_get.return_value.status_code = 403
        tester = UserAgentTester(test_url="https://www.example.com")
        user_agent = "InvalidUserAgent/0.0"
        headers = {'User-Agent': user_agent}
        result = tester.check_user_agent(user_agent, headers)
        self.assertFalse(result)

    @patch('user_agent_filter.tester.load_user_agents')
    @patch('builtins.open', new_callable=mock_open)
    def test_filter_user_agents(self, mock_open_file, mock_load_user_agents):
        mock_load_user_agents.return_value = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
            "InvalidUserAgent/0.0"
        ]
        
        # Patch the 'check_user_agent' method to control its output
        with patch.object(UserAgentTester, 'check_user_agent', side_effect=[True, False, True]) as mock_check_user_agent:
            filter_user_agents("user_agents.txt", "output.txt", "https://www.example.com")

        # Check if file was written correctly
        mock_open_file.assert_called_with("output.txt", 'w')
        mock_open_file().write.assert_any_call("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3\n")
        mock_open_file().write.assert_any_call("InvalidUserAgent/0.0\n")

    @patch('user_agent_filter.tester.load_user_agents', return_value=[])
    @patch('builtins.open', new_callable=mock_open)
    def test_filter_user_agents_no_user_agents(self, mock_open_file, mock_load_user_agents):
        with self.assertRaises(FileNotFoundError):
            filter_user_agents("non_existent_file.txt", "output.txt", "https://www.example.com")
        # Ensure output file was not written to
        mock_open_file.assert_not_called()

if __name__ == '__main__':
    unittest.main()
