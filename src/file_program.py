import csv
import json
import os

_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_config():
    """Load main_program_config.json for CSV header settings."""
    config_path = os.path.join(_project_root, 'config', 'main_program_config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"csv_headers": ["Title", "Company", "Link"]}


def writer(data: list, path_to_job_folder: str, filename: str):
    """Write job data to a CSV file."""
    config = _load_config()
    filepath = os.path.join(path_to_job_folder, filename)

    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(config.get('csv_headers', ['Title', 'Company', 'Link']))

            for row in data:
                csv_writer.writerow(row)

        print(f"Saved: {filepath}")

    except OSError as e:
        print(f"  Error: Failed to write file: {e}")


def reader(path_to_job_folder: str, filename: str):
    """Read and print the contents of a CSV file."""
    filepath = os.path.join(path_to_job_folder, filename)

    try:
        with open(filepath, 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            job_count = 0

            for row in csv_reader:
                print(', '.join(row))
                job_count += 1

        job_count -= 1  # Subtract the header row
        print(f'\nTotal jobs: {job_count}')
        print()

    except FileNotFoundError:
        print(f"  Error: File not found: {filepath}")
    except OSError as e:
        print(f"  Error: Failed to read file: {e}")