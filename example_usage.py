# examples/example_usage.py

from user_agent_filter.tester import filter_user_agents

filter_user_agents('user_agents.txt', 'filtered(amazon).txt', 'https://www.amazon.in/')
