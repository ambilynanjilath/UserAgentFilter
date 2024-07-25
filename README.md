# UserAgentFilter

**UserAgentFilter** is a Python package designed for testing user agents on specific websites. It helps in identifying which user agents are effective for web scraping or automated testing by filtering out those that work or fail.

## Key Features
- Tests a list of user agents against a specified website.
- Supports optional proxy configuration.
- Handles errors and retries for transient issues.
- Random delays between requests to mimic human browsing behavior.
- Outputs results in a text file for easy review.


## Installation

You can install **UserAgentFilter** via pip. Run the following command:

```bash
pip install useragentfilter


### 3. **Usage**

Here's a quick example of how to use the `UserAgentTester` class to filter user agents:

```python
from UserAgentFilter import UserAgentTester

# Initialize the tester with a target URL and optional proxy settings
tester = UserAgentTester(
    test_url='https://www.example.com',
    proxy={'http': 'http://your_proxy:port', 'https': 'https://your_proxy:port'},
    timeout=10,
    max_retries=3,
    delay_range=(3, 8)
)

# Filter user agents from a file and save the successful ones to another file
tester.filter_user_agents(
    user_agents_file='tests/user_agents.txt',
    output_file='filtered_user_agents.txt'
)

)


