# Job Finder

## Overview
This is a Python-based application designed to automate the process of finding job listings. It efficiently gathers job data, organizes it, and saves it for easy access. Currently, the application works in Finland, but it can be easily modified to work in other countries.

## Features
- Automated finding of job listings with specified criteria
- Efficient data organization
- Save results in CSV format for easy access

## Prerequisites
- Python 3.12.0
- pip 23.2.1

## Installation

### Python and pip
Ensure you have the correct versions of Python and pip installed. You can download Python [here](https://www.python.org/downloads/) which includes pip.

To check your Python version:
```bash
python3 --version
```


To check your pip version:
```bash
pip3 --version
```

### Installing dependencies
1. Navigate to the project directory
2. Run the following command:
```bash
pip3 install -r requirements.txt
```


## Setting up the project
1. Clone the repository
2. Navigate to the project directory
3. Setup your .env file to root directory of the project (.env file should include USER_AGENTS in the following format)
-> If you don't have user agents, go to Google on your own device and type 'my user agent'. To acquire more agents, repeat this process on each device you own. Each device has its own unique user agent.


<pre>
USER_AGENTS="agent1
agent2
agent3
..."
</pre>

##### Disclaimer: Use this information at your own risk, and ensure you understand what you are doing. As a developer, I am not responsible for any possible bans from websites or consequences that arise from the use of this application.

## Running the application
1. Navigate to the project directory
2. Run the following command:
```bash
python3 main.py
```

## Usage
After starting the application, it will begin finding job listings based on the specified criteria and configurations. The results will be saved in the src/csv_files/ directory.

When running the application, you will be prompted to enter the following information:
- Search term (e.g. 'software engineer, or python etc.') If you leave this blank it will search for all jobs
- Area (e.g. 'Pääkaupunkiseutu' or 'Helsinki' etc.) If you leave this blank it will search for all areas
**Notice! If you leave both search term and area blank, it will search for all jobs in all areas. In January 2024 there were 1464 pages and almost 30 000 jobs available. 
Use with caution!**

- Type of job (e.g. 'full_time' or 'part_time' etc.) If you leave this blank it will default to 'full_time'


## License

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License

Copyright (c) 2024 - present, [yumeangelica](https://github.com/yumeangelica)

Remember to give credit if you use this project in your own work.