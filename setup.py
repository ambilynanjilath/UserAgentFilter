from setuptools import setup, find_packages

setup(
    name='UserAgentFilter',  
    version='1.0.0',  
    description='A package for testing user agents on specific websites',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown', 
    author='Ambily Biju & Shahana Farvin', 
    author_email='ambilybiju2408@gmail.com,shahana50997@gmail.com',  
    url='https://github.com/ambilynanjilath/UserAgentFilter.git',  
    packages=find_packages(), 
    install_requires=[
        'requests>=2.25.0',
        'urllib3>=1.26.0',
    ],
    python_requires='>=3.7',  
    classifiers=[
        'Development Status :: 5 - Production/Stable',  
        'Intended Audience :: Developers',  
        'License :: OSI Approved :: MIT License',  
        'Programming Language :: Python :: 3', 
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='user agent testing, web scraping, requests',  # Keywords for your package
    project_urls={
        'Documentation': 'https://github.com/ambilynanjilath/UserAgentFilter/blob/main/README.md',
        'Source': 'https://github.com/ambilynanjilath/UserAgentFilter',
        'Tracker': 'https://github.com/ambilynanjilath/UserAgentFilter/issues',
    },
)
