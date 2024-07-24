# user_agent_filter/tester.py

import requests
import random
import time
from .utils import load_user_agents

class UserAgentTester:
    def __init__(self, test_url, proxy=None, delay_range=(3, 8)):
        """
        Initialize the UserAgentTester with a URL, proxy, and delay range.

        Args:
            test_url (str): The URL to test user agents against.
            proxy (dict, optional): A dictionary containing proxy settings. Default is None.
            delay_range (tuple, optional): A tuple specifying the min and max delay (in seconds)
                                           between requests. Default is (3, 8).
        """
        self.test_url = test_url
        self.proxy = proxy
        self.delay_range = delay_range

    def check_user_agent(self, user_agent, headers, timeout=10, max_retries=3):
        """
        Test if a user agent is valid for the given website with enhanced error handling.

        Args:
            user_agent (str): The user agent string to test.
            headers (dict): HTTP headers to include in the request. Must include the user agent.
            timeout (int, optional): Timeout for the request in seconds. Default is 10.
            max_retries (int, optional): Maximum number of retries for transient errors. Default is 3.

        Returns:
            bool: True if the user agent is accepted (HTTP status 200), False otherwise.
        """
        session = requests.Session()

        if self.proxy:
            session.proxies.update(self.proxy)

        retries = 0
        while retries < max_retries:
            try:
                response = session.get(self.test_url, headers=headers, timeout=timeout, verify=False)

                if response.status_code == 200:
                    print(f"User-Agent '{user_agent}' is working for {self.test_url}.")
                    return True
                elif response.status_code == 403:
                    print(f"Warning: User-Agent '{user_agent}' is blocked with status code 403 Forbidden for {self.test_url}.")
                    return False
                elif 300 <= response.status_code < 400:
                    print(f"Redirected: User-Agent '{user_agent}' received a redirect status code {response.status_code} for {self.test_url}.")
                    return False
                elif 400 <= response.status_code < 500:
                    print(f"Client error: User-Agent '{user_agent}' received a client error status code {response.status_code} for {self.test_url}.")
                    return False
                elif 500 <= response.status_code < 600:
                    print(f"Server error: User-Agent '{user_agent}' received a server error status code {response.status_code} for {self.test_url}.")
                    return False
                else:
                    print(f"Warning: User-Agent '{user_agent}' is not working. Status code: {response.status_code} for {self.test_url}.")
                    return False
            except requests.exceptions.Timeout:
                print(f"Timeout: Request for User-Agent '{user_agent}' timed out for {self.test_url}. Retrying...")
                retries += 1
                if retries >= max_retries:
                    print(f"Failed: User-Agent '{user_agent}' failed due to repeated timeouts for {self.test_url}.")
                    return False
            except requests.exceptions.ConnectionError:
                print(f"Connection error: Failed to connect to {self.test_url} with User-Agent '{user_agent}'.")
                return False
            except requests.exceptions.ProxyError:
                print(f"Proxy error: Failed to connect using the proxy for User-Agent '{user_agent}'.")
                return False
            except requests.exceptions.InvalidURL:
                print(f"Invalid URL: The URL '{self.test_url}' is invalid.")
                return False
            except requests.RequestException as e:
                print(f"Error: User-Agent '{user_agent}' failed with exception: {e} for {self.test_url}.")
                return False

    def filter_user_agents(self, user_agents):
        """
        Filter user agents by testing them against a specific website.

        Args:
            user_agents (list): A list of user agents to test.

        Returns:
            list: A list of successful user agents that were accepted by the website.
        """
        common_headers = {
            'User-Agent': '',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,ml;q=0.6',
            'Cache-Control': 'no-cache',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Requested-With': 'XMLHttpRequest'
        }

        successful_user_agents = []

        for user_agent in user_agents:
            common_headers['User-Agent'] = user_agent
            success = self.check_user_agent(user_agent, headers=common_headers)

            if success:
                successful_user_agents.append(user_agent)

            delay = random.uniform(*self.delay_range)
            print(f"Delaying for {delay:.2f} seconds before the next request")
 
