
from user_agent_filter.tester import filter_user_agents

# # Example usage with a proxy
# proxy = {
#     "https": "scraperapi.retry_404=true.country_code=us.device_type=desktop.session_number=456.keep_headers=true:13b50ee780e25089c9599d234627bc81@proxy-server.scraperapi.com:8001"
# }

# filter_user_agents(
#     user_agents_file='user_agents.txt',
#     output_file='filtered(net).txt',
#     test_url='https://www.net-a-porter.com',
#     proxy=proxy
# )
delay_range = (5, 7)  # Custom delay range in seconds
# Example usage without a proxy
filter_user_agents(
    user_agents_file='user_agents.txt',
    output_file='filtered(swiggy).txt',
    test_url='https://www.swiggy.com/',
    delay_range=delay_range
)

