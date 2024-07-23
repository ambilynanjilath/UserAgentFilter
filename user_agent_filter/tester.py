# user_agent_tester/tester.py

import requests
import time
import random

def check_user_agent(user_agent, test_url, headers, timeout=10):
    try:
        response = requests.get(test_url, headers=headers, timeout=timeout)
        if response.status_code == 200:
            print(f"User-Agent '{user_agent}' is working for {test_url}.")
            return True
        elif response.status_code == 403:
            print(f"User-Agent '{user_agent}' is blocked with status code 403 Forbidden for {test_url}.")
            return False
        else:
            print(f"User-Agent '{user_agent}' is not working. Status code: {response.status_code} for {test_url}.")
            return False
    except requests.RequestException as e:
        print(f"User-Agent '{user_agent}' failed with exception: {e} for {test_url}.")
        return False

def filter_user_agents(user_agents_file, output_file, test_url, delay_range=(10, 30)):
    # Define common headers
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

    print(f"Reading user agents from: {user_agents_file}")
    print(f"Saving filtered user agents to: {output_file}")
    print(f"Testing user agents with URL: {test_url}")

    with open(user_agents_file, 'r') as file:
        user_agents = file.readlines()
    
    print(f"User agents loaded: {len(user_agents)}")  # Debug print

    for user_agent in user_agents:
        user_agent = user_agent.strip()
        if not user_agent:  # Skip empty lines
            continue
        
        common_headers['User-Agent'] = user_agent
        success = check_user_agent(user_agent, test_url=test_url, headers=common_headers)
        
        if success:
            successful_user_agents.append(user_agent)
        
        delay = random.uniform(*delay_range)
        time.sleep(delay)

    print(f"Successful user agents: {len(successful_user_agents)}")  # Debug print

    with open(output_file, 'w') as f:
        for agent in successful_user_agents:
            f.write(agent + '\n')

    return successful_user_agents
