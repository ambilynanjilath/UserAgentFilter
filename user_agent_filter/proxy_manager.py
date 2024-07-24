# user_agent_filter/proxy_manager.py

class ProxyManager:
    def __init__(self, proxy_file=None):
        """
        Initialize the ProxyManager with an optional proxy file.

        Args:
            proxy_file (str, optional): Path to the file containing proxy settings.
        """
        self.proxies = self.load_proxies(proxy_file) if proxy_file else None

    def load_proxies(self, proxy_file):
        """
        Load proxy settings from a file.

        Args:
            proxy_file (str): Path to the file containing proxy settings.

        Returns:
            dict: A dictionary containing proxy settings.
        """
        try:
            with open(proxy_file, 'r') as file:
                proxy = file.read().strip()
            return {"https": proxy}
        except FileNotFoundError:
            print(f"Error: The file '{proxy_file}' was not found.")
            return None
        except IOError:
            print(f"Error: Unable to read the file '{proxy_file}'. Check file permissions.")
            return None
