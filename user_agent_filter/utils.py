# user_agent_filter/utils.py

def load_user_agents(file_path):
    """
    Load user agents from a file.

    Args:
        file_path (str): Path to the file containing user agents.

    Returns:
        list: A list of user agents.
    """
    try:
        with open(file_path, 'r') as file:
            user_agents = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return []
    except IOError:
        print(f"Error: Unable to read the file '{file_path}'. Check file permissions.")
        return []

    print(f"User agents loaded: {len(user_agents)}")
    return user_agents
