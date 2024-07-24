import unittest
import os
from UserAgentFilter import UserAgentTester

class TestUserAgentTester(unittest.TestCase):
    def setUp(self):
        self.test_url = 'https://www.net-a-porter.com/'  # Replace with a test URL
        self.delay_range = (3, 5)
        self.user_agents_file = 'tests/user_agents.txt'
        self.output_file = 'tests/filtered_test.txt'
        self.proxy = {
            "https": "scraperapi.retry_404=true.country_code=us.device_type=desktop.session_number=456.keep_headers=true:13b50ee780e25089c9599d234627bc81@proxy-server.scraperapi.com:8001"
        }

        # Ensure the user agents file exists
        if not os.path.isfile(self.user_agents_file):
            raise FileNotFoundError(f"User agents file '{self.user_agents_file}' does not exist.")

    def test_filter_user_agents_with_proxy(self):
        tester = UserAgentTester(
            test_url=self.test_url,
            proxy=self.proxy,  # Pass the proxy as a dictionary
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
