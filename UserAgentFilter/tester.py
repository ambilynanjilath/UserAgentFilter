import requests
import time
import random
import urllib3
import logging
from typing import Optional, Dict, List, Union

# Configure logging to display the time, log level, and message
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class UserAgentTester:
    """
    A class for testing user agents against a specific website to determine their effectiveness.

    This class provides functionality to test user agents by sending HTTP requests to a specified URL.
    It handles errors, retries requests for transient issues, and applies random delays to mimic human behavior.
    """

    def __init__(
        self,
        test_url: str,
        proxy: Optional[Union[Dict[str, str], List[str]]] = None,
        timeout: int = 10,
        max_retries: int = 3,
        delay_range: tuple = (3, 8)
    ):
        """
        Initialize the UserAgentTester class.

        Args:
            test_url (str): The URL to test each user agent against.
            proxy (dict or list, optional): A dictionary containing a single proxy setting or a list of proxy strings. Default is None.
            timeout (int, optional): Timeout for the request in seconds. Default is 10.
            max_retries (int, optional): Maximum number of retries for transient errors. Default is 3.
            delay_range (tuple, optional): A tuple specifying the min and max delay (in seconds)
                                           between requests. Default is (3, 8).
        """
        # Disable InsecureRequestWarnings from urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self.test_url = test_url
        self.proxy = proxy
        self.timeout = timeout
        self.max_retries = max_retries
        self.delay_range = delay_range
        self.common_headers = {
            'User-Agent': '',  # User-Agent will be set for each request
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,ml;q=0.6',
            'Cache-Control': 'no-cache',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Requested-With': 'XMLHttpRequest'
        }

    def get_proxy(self) -> Optional[Dict[str, str]]:
        """
        Retrieve the proxy setting for the request.

        This method handles both single proxy settings as a dictionary or choosing a random proxy from a list.

        Returns:
            dict or None: A dictionary containing the proxy setting, or None if no proxy is set.
        """
        if isinstance(self.proxy, dict):
            # If the proxy is a single dictionary, use it directly
            return self.proxy
        elif isinstance(self.proxy, list) and self.proxy:
            # If the proxy is a list, choose a random proxy string and format it as a dictionary
            proxy_string = random.choice(self.proxy)
            return {"https": proxy_string}
        else:
            # No proxy setting
            return None

    def check_user_agent(self, user_agent: str) -> bool:
        """
        Test if a user agent is valid for the given website with enhanced error handling.

        This method sends an HTTP GET request to the specified URL using the provided user agent.
        It includes robust error handling for various HTTP responses and exceptions that might occur
        during the request. The method also attempts to retry requests for transient errors like timeouts.

        Args:
            user_agent (str): The user agent string to test.

        Returns:
            bool: True if the user agent is accepted (HTTP status 200), False otherwise.

        Method Details:
        ---------------
        - A new requests session is created to maintain certain settings across requests, such as headers
          and proxies.
        
        - If a proxy is specified during the initialization of the UserAgentTester class, the session's
          proxy settings are updated accordingly to route requests through the given proxy.
        
        - A retry counter is initialized to keep track of the number of attempts made to send the request.
          The method will retry sending the request up to a maximum number of retries specified during
          initialization (`self.max_retries`).
        
        - A loop is employed to allow for multiple attempts to send the request, particularly in cases
          where transient errors like timeouts are encountered.
        
        - Inside the loop:
            - The 'User-Agent' header in `self.common_headers` is updated to the current `user_agent`
              being tested.
            
            - An HTTP GET request is sent to the `self.test_url` using the specified headers, timeout
              setting (`self.timeout`), and with SSL verification disabled (`verify=False`).
            
            - The HTTP response status code is checked to determine the outcome:
                - **Status Code 200**: Indicates that the user agent is accepted. A success message is
                  logged and the method returns True.
                
                - **Status Code 403 (Forbidden)**: Indicates that the user agent is blocked by the server.
                  A warning message is logged and the method returns False.
                
                - **Status Code 300 to <400 (Redirection)**: Indicates a redirect response. A message is
                  logged indicating the redirection, and the method returns False.
                
                - **Status Code 400 to <500 (Client Error)**: Indicates a client error occurred, possibly
                  due to the user agent. A message is logged and the method returns False.
                
                - **Status Code 500 to <600 (Server Error)**: Indicates a server error occurred. A message
                  is logged and the method returns False.
                
                - **Other Status Codes**: For any other unexpected status codes, a warning message is
                  logged and the method returns False.
        
        - If a request exception occurs, it is handled using multiple `except` blocks:
            - **Timeout Exception**: If a timeout occurs, a message is logged and the retry counter is
              incremented. If the retry limit is reached, a failure message is logged and the method
              returns False.
            
            - **ConnectionError Exception**: If a connection error occurs, a message is logged and the
              method returns False.
            
            - **ProxyError Exception**: If a proxy error occurs, a message is logged indicating the
              failure to connect using the proxy, and the method returns False.
            
            - **InvalidURL Exception**: If the URL is invalid, an error message is logged and the method
              returns False.
            
            - **General RequestException**: Handles any other exceptions related to the request. A message
              is logged with the exception details and the method returns False.
        
        This method effectively manages and tests user agents by handling a wide range of response
        scenarios and exceptions, making it a robust solution for testing user agents in web scraping
        applications.
        """
        # Create a new requests session for making HTTP requests
        session = requests.Session()

        # Get the current proxy settings
        current_proxy = self.get_proxy()

        # If a proxy is provided, update the session's proxy settings
        if current_proxy:
            session.proxies.update(current_proxy)

        retries = 0  # Initialize the retry counter
        while retries < self.max_retries:
            try:
                # Set the User-Agent header for the current request
                self.common_headers['User-Agent'] = user_agent

                # Send an HTTP GET request to the test URL with the specified headers and proxy
                response = session.get(
                    self.test_url, headers=self.common_headers, timeout=self.timeout, verify=False)

                # Check the HTTP status code to determine if the user agent is accepted
                if response.status_code == 200:
                    logging.info(f"User-Agent '{user_agent}' is working for {self.test_url}.")
                    return True  # User agent is accepted
                elif response.status_code == 403:
                    logging.warning(f"Warning: User-Agent '{user_agent}' is blocked with status code 403 Forbidden for {self.test_url}.")
                    return False  # User agent is blocked
                elif 300 <= response.status_code < 400:
                    logging.info(f"Redirected: User-Agent '{user_agent}' received a redirect status code {response.status_code} for {self.test_url}.")
                    return False  # User agent caused a redirect
                elif 400 <= response.status_code < 500:
                    logging.info(f"Client error: User-Agent '{user_agent}' received a client error status code {response.status_code} for {self.test_url}.")
                    return False  # User agent caused a client error
                elif 500 <= response.status_code < 600:
                    logging.info(f"Server error: User-Agent '{user_agent}' received a server error status code {response.status_code} for {self.test_url}.")
                    return False  # User agent caused a server error
                else:
                    logging.warning(f"Warning: User-Agent '{user_agent}' is not working. Status code: {response.status_code} for {self.test_url}.")
                    return False  # User agent is not working
            except requests.exceptions.Timeout:
                # If a timeout exception occurs, increment the retry counter and try again
                retries += 1
                logging.warning(f"Timeout: Request for User-Agent '{user_agent}' timed out for {self.test_url}. Retrying {retries}/{self.max_retries}...")
                if retries >= self.max_retries:
                    # If the maximum number of retries is reached, return False
                    logging.error(f"Failed: User-Agent '{user_agent}' failed due to repeated timeouts for {self.test_url}.")
                    return False
            except requests.exceptions.ConnectionError:
                # If a connection error occurs, log an error message and return False
                logging.error(f"Connection error: Failed to connect to {self.test_url} with User-Agent '{user_agent}'.")
                return False
            except requests.exceptions.ProxyError:
                # If a proxy error occurs, log an error message and return False
                logging.error(f"Proxy error: Failed to connect using the proxy for User-Agent '{user_agent}'.")
                return False
            except requests.exceptions.InvalidURL:
                # If an invalid URL error occurs, log an error message and return False
                logging.error(f"Invalid URL: The URL '{self.test_url}' is invalid.")
                return False
            except requests.RequestException as e:
                # Handle any other request exceptions, such as network errors
                logging.error(f"Error: User-Agent '{user_agent}' failed with exception: {e} for {self.test_url}.")
                return False  # Request failed

    def filter_user_agents(self, user_agents_file: str, output_file: str) -> List[str]:
        """
        Filter user agents by testing them against a specific website with enhanced error handling.

        This method reads a list of user agents from a specified input file, tests each user agent 
        against a given website, and writes the successful user agents to an output file. The testing 
        involves sending HTTP requests with each user agent and checking the server's response. It also 
        incorporates error handling for file operations and network issues, along with delays between 
        requests to mimic human browsing behavior.

        Args:
            user_agents_file (str): Path to the file containing user agents to test.
            output_file (str): Path to the file where successful user agents will be saved.

        Returns:
            list: A list of successful user agents that were accepted by the website.

        Method Details:
        ---------------
        - **Initialization**:
            - A list named `successful_user_agents` is initialized to store user agents that successfully 
              pass the test (i.e., receive a status code 200 from the server).
        
        - **Reading User Agents**:
            - The method attempts to open and read the `user_agents_file` using a `with` statement to 
              ensure proper file handling.
            - If the file is not found (`FileNotFoundError`), an error message is logged, and the method 
              returns an empty list.
            - If an I/O error occurs (e.g., permission issues), an error message is logged, and the method 
              returns an empty list.
            - Upon successful reading, the number of user agents loaded is logged for user reference.
        
        - **Testing User Agents**:
            - The method iterates over each user agent in the list `user_agents`.
            - Each user agent is stripped of leading/trailing whitespace using `strip()`.
            - If a user agent is an empty string (e.g., due to empty lines in the file), it is skipped.
            - The `check_user_agent` method is called for each user agent to test its validity against the 
              specified URL (`self.test_url`).
            - If a user agent is successful (i.e., `check_user_agent` returns `True`), it is appended to 
              `successful_user_agents`.
            - A random delay between requests is introduced using `random.uniform(*self.delay_range)` to 
              mimic human-like browsing behavior. The delay duration is logged for user reference.
        
        - **Writing Successful User Agents**:
            - After testing all user agents, the method attempts to write the successful user agents to the 
              `output_file`.
            - A `with` statement is used to open the file in write mode, ensuring proper file handling.
            - Each successful user agent is written to the file, one per line.
            - If an I/O error occurs during writing (e.g., permission issues), an error message is logged, 
              and the method returns an empty list.
            - A success message is logged, indicating the number of user agents written to the output file.
        
        - **Final Checks**:
            - If no successful user agents are found, a warning message is logged suggesting the use of a 
              proxy, as the lack of success may indicate server restrictions or blocks.
        
        - **Return Value**:
            - The method returns the list `successful_user_agents`, containing all user agents that 
              successfully received a status code 200 from the server.

            Overall, this method provides a complete and robust mechanism for filtering user agents by testing 
            them against a specified website, ensuring that only effective user agents are retained. It handles 
            file and network errors gracefully, provides informative output messages, and incorporates random 
            delays to reduce detection risks.
        """
        # Initialize a list to store successful user agents
        successful_user_agents = []

        # Attempt to read user agents from the specified file
        try:
            logging.info(f"Reading user agents from: {user_agents_file}")
            with open(user_agents_file, 'r') as file:
                user_agents = file.readlines()
        except FileNotFoundError:
            # If the file is not found, log an error message and return an empty list
            logging.error(f"Error: The file '{user_agents_file}' was not found.")
            return []
        except IOError:
            # If there is an I/O error (e.g., permission issue), log an error message and return an empty list
            logging.error(f"Error: Unable to read the file '{user_agents_file}'. Check file permissions.")
            return []

        # Print the number of user agents loaded
        total_agents = len(user_agents)
        logging.info(f"User agents loaded: {total_agents}")

        # Test each user agent
        for index, user_agent in enumerate(user_agents):
            user_agent = user_agent.strip()  # Remove leading/trailing whitespace
            if not user_agent:  # Skip empty lines
                continue

            # Display progress indicator
            logging.info(f"Testing user agent {index + 1}/{total_agents}")

            # Test the user agent against the specified URL
            success = self.check_user_agent(user_agent)

            # If the user agent is successful, add it to the list of successful agents
            if success:
                successful_user_agents.append(user_agent)

            # Add a random delay between requests to mimic human behavior
            delay = random.uniform(*self.delay_range)
            logging.info(f"Delaying for {delay:.2f} seconds before the next request")
            time.sleep(delay)

        # Log the number of successful user agents
        logging.info(f"Successful user agents: {len(successful_user_agents)}")

        # Attempt to write the successful user agents to the output file
        try:
            logging.info(f"Writing successful user agents to: {output_file}")
            with open(output_file, 'w') as f:
                for agent in successful_user_agents:
                    f.write(agent + '\n')
            logging.info(f"Successfully wrote {len(successful_user_agents)} user agents to {output_file}.")
        except IOError:
            # If there is an I/O error (e.g., permission issue), log an error message and return an empty list
            logging.error(f"Error: Unable to write to the file '{output_file}'. Check file permissions.")
            return []

        # If no successful user agents are found, suggest using a proxy
        if len(successful_user_agents) == 0:
            logging.warning("Warning: No successful user agents found. Consider using a proxy if not already used.")

        # Return the list of successful user agents
        return successful_user_agents
