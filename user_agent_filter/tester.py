import requests
import time
import random

def check_user_agent(user_agent, test_url, headers, proxy=None, timeout=10, max_retries=3):
    """
    Test if a user agent is valid for a given website with enhanced error handling.

    Args:
        user_agent (str): The user agent string to test.
        test_url (str): The URL to test the user agent against.
        headers (dict): HTTP headers to include in the request. Must include the user agent.
        proxy (dict, optional): A dictionary containing proxy settings. Default is None.
        timeout (int, optional): Timeout for the request in seconds. Default is 10.
        max_retries (int, optional): Maximum number of retries for transient errors. Default is 3.

    Returns:
        bool: True if the user agent is accepted (HTTP status 200), False otherwise.
    """
    # Create a new requests session for making HTTP requests
    session = requests.Session()

    # If a proxy is provided, update the session's proxy settings
    if proxy:
        session.proxies.update(proxy)

    retries = 0
    while retries < max_retries:
        try:
            # Send an HTTP GET request to the test URL with the specified headers and proxy
            response = session.get(test_url, headers=headers, timeout=timeout, verify=False)

            # Check the HTTP status code to determine if the user agent is accepted
            if response.status_code == 200:
                print(f"User-Agent '{user_agent}' is working for {test_url}.")
                return True  # User agent is accepted
            elif response.status_code == 403:
                print(f"Warning: User-Agent '{user_agent}' is blocked with status code 403 Forbidden for {test_url}.")
                return False  # User agent is blocked
            elif 300 <= response.status_code < 400:
                print(f"Redirected: User-Agent '{user_agent}' received a redirect status code {response.status_code} for {test_url}.")
                return False  # User agent caused a redirect
            elif 400 <= response.status_code < 500:
                print(f"Client error: User-Agent '{user_agent}' received a client error status code {response.status_code} for {test_url}.")
                return False  # User agent caused a client error
            elif 500 <= response.status_code < 600:
                print(f"Server error: User-Agent '{user_agent}' received a server error status code {response.status_code} for {test_url}.")
                return False  # User agent caused a server error
            else:
                print(f"Warning: User-Agent '{user_agent}' is not working. Status code: {response.status_code} for {test_url}.")
                return False  # User agent is not working
        except requests.exceptions.Timeout:
            print(f"Timeout: Request for User-Agent '{user_agent}' timed out for {test_url}. Retrying...")
            retries += 1
            if retries >= max_retries:
                print(f"Failed: User-Agent '{user_agent}' failed due to repeated timeouts for {test_url}.")
                return False
        except requests.exceptions.ConnectionError:
            print(f"Connection error: Failed to connect to {test_url} with User-Agent '{user_agent}'.")
            return False
        except requests.exceptions.ProxyError:
            print(f"Proxy error: Failed to connect using the proxy for User-Agent '{user_agent}'.")
            return False
        except requests.exceptions.InvalidURL:
            print(f"Invalid URL: The URL '{test_url}' is invalid.")
            return False
        except requests.RequestException as e:
            # Handle any other request exceptions, such as network errors
            print(f"Error: User-Agent '{user_agent}' failed with exception: {e} for {test_url}.")
            return False  # Request failed

def filter_user_agents(user_agents_file, output_file, test_url, proxy=None, delay_range=(3, 8)):
    """
    Filter user agents by testing them against a specific website with enhanced error handling.

    Args:
        user_agents_file (str): Path to the file containing user agents to test.
        output_file (str): Path to the file where successful user agents will be saved.
        test_url (str): The URL to test each user agent against.
        proxy (dict, optional): A dictionary containing proxy settings. Default is None.
        delay_range (tuple, optional): A tuple specifying the min and max delay (in seconds)
                                       between requests. Default is (3, 8).

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

    try:
        print(f"Reading user agents from: {user_agents_file}")
        with open(user_agents_file, 'r') as file:
            user_agents = file.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{user_agents_file}' was not found.")
        return []
    except IOError:
        print(f"Error: Unable to read the file '{user_agents_file}'. Check file permissions.")
        return []

    print(f"User agents loaded: {len(user_agents)}")  # Print the number of user agents loaded

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
        print(f"Delaying for {delay:.2f} seconds before the next request")
        time.sleep(delay)

    print(f"Successful user agents: {len(successful_user_agents)}")  # Print the number of successful user agents

    # Write the successful user agents to the output file
    try:
        with open(output_file, 'w') as f:
            for agent in successful_user_agents:
                f.write(agent + '\n')
    except IOError:
        print(f"Error: Unable to write to the file '{output_file}'. Check file permissions.")
        return []

    # If no successful user agents are found, suggest using a proxy
    if len(successful_user_agents) == 0:
        print("Warning: No successful user agents found. Consider using a proxy if not already used.")

    # Return the list of successful user agents
    return successful_user_agents