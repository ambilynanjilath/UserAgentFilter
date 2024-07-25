from setuptools import setup, find_packages

setup(
    name='UserAgentFilter',  # Name of your package
    version='1.0.0',  # Initial release version
    description='A package for testing user agents on specific websites',  # Short description
    long_description=open('README.md').read(),  # Long description read from the README file
    long_description_content_type='text/markdown',  # Type of the long description content
    author='Ambily Biju & Shahana Farvin',  # Author's name
    author_email='ambilybiju2408@gmail.com,shahana50997@gmail.com',  # Author's email
    url='https://github.com/ambilynanjilath/UserAgentFilter.git',  # URL of the project (e.g., GitHub)
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[
        'requests>=2.25.0',
        'urllib3>=1.26.0',
    ],
    python_requires='>=3.7',  # Minimum Python version requirement
    classifiers=[
        'Development Status :: 5 - Production/Stable',  # Development status
        'Intended Audience :: Developers',  # Intended audience
        'License :: OSI Approved :: MIT License',  # License
        'Programming Language :: Python :: 3',  # Supported Python versions
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='user agent testing, web scraping, requests',  # Keywords for your package
    project_urls={
        'Documentation': 'https://github.com/ambilynanjilath/UserAgentFilter/blob/main/README.md',
        'Source': 'https://github.com/ambilynanjilath/UserAgentFilter',
        'Tracker': 'https://github.com/ambilynanjilath/UserAgentFilter/issues',
    },
)
