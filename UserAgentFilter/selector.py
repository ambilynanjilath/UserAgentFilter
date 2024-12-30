import random
import logging
from tester import UserAgentTester

class GetUserAgent:
    """
    A class to manage and test user agents for web scraping tasks. It allows 
    testing a specified number of user agents against a website and provides 
    successful user agents for subsequent requests.

    Attributes:
        file_path (str): Path to the user agent text file.
        successful_agents (list): List of user agents that passed the tests.
    """
    
    def __init__(self, file_path: str):
        """
        Initialize the GetUserAgent class.

        Args:
            file_path (str): The path to the file containing user agents.
        """
        self.file_path = file_path
        self.successful_agents = []

    def test_user_agents(self, number: int, test_url: str):
        """
        Test a given number of user agents from the file against a website.

        Args:
            number (int): Number of user agents to test.
            test_url (str): URL of the website to test user agents against.

        Returns:
            None
        """
        logging.info(f"Testing up to {number} user agents from {self.file_path} against {test_url}.")
        
        tester = UserAgentTester(test_url=test_url)
        
        try:
            # Load user agents from the file
            with open(self.file_path, "r") as f:
                user_agents = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            logging.error(f"File not found: {self.file_path}")
            return
        
        if len(user_agents) < number:
            logging.warning(f"Requested {number} user agents, but only {len(user_agents)} available.")
            number = len(user_agents)

        sampled_agents = random.sample(user_agents, number)

        for user_agent in sampled_agents:
            if tester.check_user_agent(user_agent):
                self.successful_agents.append(user_agent)

        logging.info(f"Total successful user agents: {len(self.successful_agents)}")

    def get_random_user_agent(self):
        """
        Get a random user agent from the list of successful user agents.

        Returns:
            str: A random successful user agent.
        """
        if not self.successful_agents:
            logging.error("No successful user agents available. Run `test_user_agents` first.")
            return None
        return random.choice(self.successful_agents)
