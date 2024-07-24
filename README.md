# UserAgentFilter

**UserAgentFilter** is a Python package designed for testing user agents on specific websites. It helps in identifying which user agents are effective for web scraping or automated testing by filtering out those that work or fail.

## Key Features
- Tests a list of user agents against a specified website.
- Supports optional proxy configuration.
- Outputs results in a text file for easy review.

## Installation

You can install **UserAgentFilter** via pip. Run the following command:

```bash
pip install useragentfilter


### 3. **Usage**

Here's a quick example of how to use the `UserAgentTester` class to filter user agents:

```python
from UserAgentFilter import UserAgentTester

# Create an instance of UserAgentFilter with a proxy
filter = UserAgentTester(
    test_url='https://www.swiggy.com/',
    delay_range=(5, 7)
)
filter.filter_user_agents(
    user_agents_file='user_agents.txt',
    output_file='filtered.txt'
)
