import json
import os
from datetime import date
from src.job_program import finder
from src.file_program import writer, reader

_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_config():
    """Load main_program_config.json with fallback defaults."""
    config_path = os.path.join(_project_root, 'config', 'main_program_config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"  Warning: Config file missing or invalid: {e}")
        print("  Using default settings.")
        return {
            "output_dir": "src/csv_files",
            "defaults": {"area": "pääkaupunkiseutu", "work_type": "full_time"},
            "work_types": {"1": "full_time", "2": "part_time"},
            "filename_template": "{date}_{area}_{work_type}_{search_term}_jobs.csv"
        }


def _ensure_directory(path: str):
    """Create directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)


def _build_filename(config, area, work_type, search_term):
    """Build the output filename from the config template."""
    template = config.get(
        'filename_template',
        '{date}_{area}_{work_type}_{search_term}_jobs.csv'
    )
    today = date.today().isoformat()

    # Sanitize search term for use in filename
    safe_term = search_term.replace(' ', '_').replace('/', '_') if search_term else ''

    filename = template.format(
        date=today,
        area=area,
        work_type=work_type,
        search_term=safe_term
    )

    # Remove double underscores
    while '__' in filename:
        filename = filename.replace('__', '_')

    return filename


def run():
    """Main entry point for the job finder application."""
    config = _load_config()
    defaults = config.get('defaults', {})
    work_types = config.get('work_types', {"1": "full_time", "2": "part_time"})

    print()
    print('Job Finder')
    print('-----------')

    run_again = True

    while run_again:

        # Search term
        search_term = input('Enter a search term (e.g. python): ').strip()

        # Area with default
        default_area = defaults.get('area', 'pääkaupunkiseutu')
        area_input = input(f'Enter an area (default: {default_area}): ').strip()
        area = area_input if area_input else default_area

        # Work type from config mapping
        type_prompt = ', '.join(f'{k} = {v}' for k, v in work_types.items())
        try:
            choice = input(f'Enter type of work ({type_prompt}): ').strip()
            type_of_work = work_types.get(choice)
            if not type_of_work:
                default_wt = defaults.get('work_type', 'full_time')
                print(f'Invalid choice, using default: {default_wt}')
                type_of_work = default_wt
        except (ValueError, EOFError):
            type_of_work = defaults.get('work_type', 'full_time')
            print(f'Using default: {type_of_work}')

        # Prepare output directory and filename
        output_dir = config.get('output_dir', 'src/csv_files')
        _ensure_directory(output_dir)
        filename = _build_filename(config, area, type_of_work, search_term)

        # Run the scraper
        print(f'\nSearching: "{search_term}" / {area} / {type_of_work}...\n')
        found_jobs = finder(search_term, area, type_of_work)

        if not found_jobs:
            print('No jobs found.\n')
        else:
            writer(found_jobs, output_dir, filename)
            reader(output_dir, filename)

        # Ask to search again
        answer = input('Search again? (y/n): ').strip().lower()
        if answer in ('n', 'no'):
            run_again = False

    print('Exiting...\n')