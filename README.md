# Job Finder

## Overview

A Python application that scrapes job listings from [Duunitori](https://duunitori.fi), organizes the data, and saves results as CSV files. Currently targets the Finnish job market but can be adapted for other sites by modifying the config files.

## Features

- Config-driven scraping — selectors, parameters, and settings live in JSON files, not in code
- Fallback selectors — if the site changes its HTML structure, the scraper tries alternative selectors automatically
- Page validation — detects captchas, cookie walls, and structural changes instead of silently failing
- Automatic retry with backoff on 429/5xx responses
- Rotating user agents from a plain text file
- Results saved as timestamped CSV files

## Project Structure

```
job_finder/
├── main.py                          # Entry point
├── requirements.txt
├── config/
│   ├── agents.txt                   # User agent strings (one per line)
│   ├── job_program_config.json      # Scraper selectors, URLs, request settings
│   └── main_program_config.json     # Output settings, filename template, defaults
└── src/
    ├── __init__.py
    ├── main_program.py              # CLI input loop
    ├── job_program.py               # Scraper logic
    ├── file_program.py              # CSV read/write
    └── agent_program.py             # User agent rotation
```

## Prerequisites

- Python 3.12+
- pip

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd job_finder
```

2. Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### User Agents (`config/agents.txt`)

The file ships with a default set of user agents. To add your own, visit a site like [whatismybrowser.com](https://www.whatismybrowser.com/) on different devices and paste the strings into the file, one per line.

### Scraper Settings (`config/job_program_config.json`)

Controls selectors, request timeouts, retry logic, and page validation. If Duunitori changes its HTML structure, update the selectors here — no code changes needed. Each selector has a `primary` and a list of `fallbacks` that are tried in order.

### App Settings (`config/main_program_config.json`)

Controls the output directory, filename template, default search values, and CSV headers.

## Usage

```bash
python3 main.py
```

You will be prompted for:

- **Search term** — e.g. `python`, `react`, `data engineer`. Leave blank to search all jobs.
- **Area** — e.g. `helsinki`, `pääkaupunkiseutu`. Leave blank to use the default from config.
- **Type of work** — `1` for full-time, `2` for part-time.

Results are saved to `src/csv_files/` with the format `2026-03-23_helsinki_full_time_python_jobs.csv`.

> **Note:** Leaving both search term and area blank will scrape all available listings. This can mean thousands of pages — use with caution. The config has a `max_pages` safety cap (default: 50).

## Disclaimer

Use this application at your own risk. Ensure you understand the legal implications of web scraping in your jurisdiction. The developer is not responsible for any bans or consequences arising from the use of this application.

## License

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.

Copyright (c) 2024 – present, [yumeangelica](https://github.com/yumeangelica)