# UserAgentFilter
![UserAgentFilter Logo](https://github.com/ambilynanjilath/UserAgentFilter/blob/main/logo.png)

**UserAgentFilter** is a Python package designed for testing user agents on specific websites. It helps in identifying which user agents are effective for web scraping or automated testing by filtering out those that work or fail.

## Key Features
- Tests a list of user agents against a specified website.
- Supports optional proxy configuration.
- Handles errors and retries for transient issues.
- Random delays between requests to mimic human browsing behavior.
- Outputs results in a text file for easy review.

## Prerequisites

- Python 3.6 or higher
- `requests` library
- `beautifulsoup4` library

## Installation

You can install **UserAgentFilter** via pip. Run the following command:

```
pip install useragentfilter
```

## Usage

To use **UserAgentFilter**, follow these steps:

1. Import the Package
First, import the **UserAgentTester** class from the package.

```
from UserAgentFilter import UserAgentTester
```

2. Initialize the UserAgentTester
Create an instance of the UserAgentTester class. You need to specify the URL of the website you want to test the user agents against. Optionally, you can provide proxy settings, a timeout period, the number of retries, and a range for random delays between requests to mimic human behavior.

```
tester = UserAgentTester(
    test_url='https://www.example.com',  # The URL to test user agents against
    proxy={'http': 'http://your_proxy:port', 'https': 'https://your_proxy:port'},  # Optional proxy settings
    timeout=10,  # Timeout for each request in seconds
    max_retries=3,  # Number of retries for each request
    delay_range=(3, 8)  # Random delay range between requests in seconds
)

```
3. Prepare a List of User Agents
Prepare a text file containing a list of user agents, with each user agent on a new line. For example, save the following content to tests/user_agents.txt:

```
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.64
```
4. Filter User Agents
Call the filter_user_agents method to filter the user agents. This method takes two arguments: the path to the input file containing user agents and the path to the output file where the filtered user agents will be saved.

```
tester.filter_user_agents(
    user_agents_file='tests/user_agents.txt',  # Path to the input file with user agents
    output_file='filtered_user_agents.txt'  # Path to the output file to save the filtered user agents
)
```
5. Review the Results
After the filtering process is complete, the successful user agents will be saved to the specified output file (filtered_user_agents.txt). You can review this file to see which user agents passed the test.

## Example Workflow
Here’s a complete example of the entire workflow:

```
from UserAgentFilter import UserAgentTester

# Define the target URL and proxy settings (if needed)
test_url = 'https://www.example.com'
proxy = {'http': 'http://your_proxy:port', 'https': 'https://your_proxy:port'}

# Create an instance of UserAgentTester
tester = UserAgentTester(
    test_url=test_url,
    proxy=proxy,
    timeout=10,
    max_retries=3,
    delay_range=(3, 8)
)

# Filter user agents from the input file and save the successful ones to the output file
tester.filter_user_agents(
    user_agents_file='tests/user_agents.txt',
    output_file='filtered_user_agents.txt'
)

print("User agents have been filtered and saved to 'filtered_user_agents.txt'")
```
### Additional Tips
- **Error Handling**: The UserAgentTester handles various errors such as connection timeouts and HTTP errors. It retries requests up to the specified max_retries before giving up on a user agent.
- **Random Delays**: The delay_range parameter introduces random delays between requests to help mimic human browsing behavior, which can help avoid detection when testing multiple user agents.
- **Proxy Configuration**: If you need to use a proxy, make sure to provide the correct proxy settings in the proxy dictionary. The dictionary should include keys for http and https proxies.

## Configuration Options

- test_url: The URL of the website to test user agents against.
- proxy: A dictionary containing proxy settings (optional).Use importantly in case of any 403 forbidden error.
- timeout: The maximum amount of time to wait for a response (in seconds).Default value is 10.
- max_retries: The number of times to retry a request in case of transient errors.Default value is 3.
- delay_range: A tuple specifying the range (in seconds) for random delays between requests.Default value is (3,8).

## Contributing

Contributions are welcome! If you would like to contribute to **UserAgentFilter**, please follow these steps:

- Fork the repository.
- Create a new branch for your feature or bugfix.
- Commit your changes.
- Push your branch and create a pull request.

## License
**UserAgentFilter** is licensed under the MIT License. See the LICENSE file for more information.

## Contact
If you have any questions, suggestions, or issues, please feel free to contact us at [shahana50997@gmail.com][ambilybiju2408@gmail.com].



