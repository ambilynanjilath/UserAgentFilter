from setuptools import setup, find_packages

setup(
    name='user_agent_filter',  # Package name
    version='0.1.0',           # Version number
    description='A package to test and filter user agents for specific websites.',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/user_agent_filter',  # GitHub or project URL
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[
        'requests>=2.0.0',     # Specify the dependencies
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',   # Specify the Python version requirement
)