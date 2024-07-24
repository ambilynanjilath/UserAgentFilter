import requests   #Used to make HTTP requests to websites, allowing you to send and receive data over the web easily.
import time   #Provides functions to handle time-related tasks, such as pausing the program for a specified duration.
import random  #generates random numbers, useful for creating random delays or selecting random elements.
import logging  #Allows you to record log messages to track the program's execution and troubleshoot issues.

# Configure logging to display information about the script's execution
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_user_agent(user_agent, test_url, headers, proxy=None, timeout=10):
    """
    Test if a user agent is valid for a given website.

    This function sends an HTTP GET request to a specified URL using a provided
    user agent and optional proxy settings. It checks if the user agent is accepted
    by the website, based on the HTTP status code returned. The function can also
    handle scenarios where a proxy is needed, which can be useful for bypassing 
    geo-restrictions or IP-based blocking.

    Here's how the function works step-by-step:

    1. **Create a Requests Session**:
       - A new `requests.Session()` is created, which allows the function to persist 
         certain parameters across requests. This is useful for maintaining headers, 
         cookies, or session-related data.

    2. **Proxy Configuration**:
       - If a `proxy` is provided, it is used to update the session's proxy settings.
       - The proxy parameter should be a dictionary containing keys like `'http'` and 
         `'https'` with corresponding proxy URLs, for example:
         ```
         proxy = {
             'http': 'http://proxy.example.com:8080',
             'https': 'https://proxy.example.com:8080'
         }
         ```
       - This step allows the request to be routed through the specified proxy server.

    3. **Make the HTTP GET Request**:
       - The function attempts to send an HTTP GET request to the `test_url` using the
         specified headers and proxy. The `timeout` parameter specifies the maximum time 
         in seconds to wait for a response before aborting the request.

       - The `headers` argument should include at least the `User-Agent`, which is 
         critical for simulating the desired browser environment:
         
         headers = {
             'User-Agent': user_agent,
             'Accept': 'application/json, text/javascript, */*; q=0.01',
             'Accept-Encoding': 'gzip, deflate, br, zstd',
             'Accept-Language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,ml;q=0.6',
             ...
         }
        

       - The `verify=False` argument is used to disable SSL certificate verification, 
         which can be useful for testing against sites with self-signed certificates. 
         However, it's generally advisable to handle SSL verification appropriately 
         in production environments.

    4. **Evaluate the HTTP Response**:
       - **Status Code 200 (Success)**:
         - If the response status code is 200, it indicates that the user agent 
           was accepted by the website and the content was retrieved successfully.
         - The function logs this information at the INFO level and returns `True`.

       - **Status Code 403 (Forbidden)**:
         - A 403 status code indicates that access to the resource is forbidden, 
           typically due to the user agent being blocked.
         - The function logs a warning at the WARNING level and returns `False`.

       - **Other Status Codes**:
         - For any other status codes, the function logs a warning and returns `False`,
           indicating that the user agent was not successful.

    5. **Exception Handling**:
       - If an exception occurs during the request (e.g., connection issues, timeouts, 
         invalid URL), it is caught as a `requests.RequestException`.
       - The function logs the exception details at the ERROR level and returns `False`,
         signaling that the request failed due to an error.

    Args:
        user_agent (str): The user agent string to test.
        test_url (str): The URL to test the user agent against.
        headers (dict): HTTP headers to include in the request. Must include the user agent.
        proxy (dict, optional): A dictionary containing proxy settings. Default is None.
        timeout (int, optional): Timeout for the request in seconds. Default is 10.

    Returns:
        bool: True if the user agent is accepted (HTTP status 200), False otherwise.
    """
    # Create a new requests session for making HTTP requests
    session = requests.Session()

    # If a proxy is provided, update the session's proxy settings
    if proxy:
        session.proxies.update(proxy)

    try:
        # Send an HTTP GET request to the test URL with the specified headers and proxy
        response = session.get(test_url, headers=headers, timeout=timeout, verify=False)

        # Check the HTTP status code to determine if the user agent is accepted
        if response.status_code == 200:
            logging.info(f"User-Agent '{user_agent}' is working for {test_url}.")
            return True  # User agent is accepted
        elif response.status_code == 403:
            logging.warning(f"User-Agent '{user_agent}' is blocked with status code 403 Forbidden for {test_url}.")
            return False  # User agent is blocked
        else:
            logging.warning(f"User-Agent '{user_agent}' is not working. Status code: {response.status_code} for {test_url}.")
            return False  # User agent is not working
    except requests.RequestException as e:
        # Handle any request exceptions, such as network errors
        logging.error(f"User-Agent '{user_agent}' failed with exception: {e} for {test_url}.")
        return False  # Request failed

def filter_user_agents(user_agents_file, output_file, test_url, proxy=None, delay_range=(10, 30)):
    """
    Filter user agents by testing them against a specific website.

    This function reads user agents from a file, tests each one against a specified
    website URL, and writes the successful user agents to an output file. Optionally,
    a proxy can be used for testing, and a delay between requests can be specified.

    Args:
        user_agents_file (str): Path to the file containing user agents to test.
        output_file (str): Path to the file where successful user agents will be saved.
        test_url (str): The URL to test each user agent against.
        proxy (dict, optional): A dictionary containing proxy settings. Default is None.
        delay_range (tuple, optional): A tuple specifying the min and max delay (in seconds)
                                       between requests. Default is (10, 30).

    Returns:
        list: A list of successful user agents that were accepted by the website.
    """
    # Define common headers for HTTP requests, excluding the user agent
    common_headers = {
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

    # Initialize a list to store successful user agents
    successful_user_agents = []

    logging.info(f"Reading user agents from: {user_agents_file}")
    logging.info(f"Saving filtered user agents to: {output_file}")
    logging.info(f"Testing user agents with URL: {test_url}")

    # Read user agents from the input file
    with open(user_agents_file, 'r') as file:
        user_agents = file.readlines()

    logging.info(f"User agents loaded: {len(user_agents)}")  # Log the number of user agents loaded

    # Test each user agent
    for user_agent in user_agents:
        user_agent = user_agent.strip()  # Remove leading/trailing whitespace
        if not user_agent:  # Skip empty lines
            continue
        
        # Set the User-Agent header for the current request
        common_headers['User-Agent'] = user_agent

        # Test the user agent against the specified URL
        success = check_user_agent(user_agent, test_url=test_url, headers=common_headers, proxy=proxy)
        
        # If the user agent is successful, add it to the list of successful agents
        if success:
            successful_user_agents.append(user_agent)

        # Add a random delay between requests to mimic human behavior
        delay = random.uniform(*delay_range)
        logging.info(f"Delaying for {delay:.2f} seconds before the next request")
        time.sleep(delay)

    logging.info(f"Successful user agents: {len(successful_user_agents)}")  # Log the number of successful user agents

    # Write the successful user agents to the output file
    with open(output_file, 'w') as f:
        for agent in successful_user_agents:
            f.write(agent + '\n')

    # If no successful user agents are found, suggest using a proxy
    if len(successful_user_agents) == 0:
        logging.warning("No successful user agents found. Consider using a proxy if not already used.")

    # Return the list of successful user agents
    return successful_user_agents
