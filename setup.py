# setup.py

from setuptools import setup, find_packages

setup(
    name='user_agent_filter',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'user-agent-filter=user_agent_filter.tester:filter_user_agents',
        ],
    },
    python_requires='>=3.6',
)
