import unittest
import os
from user_agent_filter import UserAgentTester

class TestUserAgentTester(unittest.TestCase):
    def setUp(self):
        self.test_url = 'https://www.swiggy.com/'  # Replace with a test URL that does not require a proxy
        self.delay_range = (3,5)
        self.user_agents_file = 'tests/user_agents.txt'
        self.output_file = 'tests/filtered_test.txt'

        # Ensure the user agents file exists
        if not os.path.isfile(self.user_agents_file):
            raise FileNotFoundError(f"User agents file '{self.user_agents_file}' does not exist.")

    def test_filter_user_agents_without_proxy(self):
        tester = UserAgentTester(
            test_url=self.test_url,
            proxy=None,  # No proxy for this test
            delay_range=self.delay_range
        )
        successful_agents = tester.filter_user_agents(
            user_agents_file=self.user_agents_file,
            output_file=self.output_file
        )
        self.assertGreater(len(successful_agents), 0, "No successful user agents found.")

    def tearDown(self):
        # Clean up the output file after the test
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

if __name__ == '__main__':
    unittest.main()
