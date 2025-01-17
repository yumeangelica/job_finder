from src.job_program import finder
from src.file_program import writer, reader
import os

# Check if the directory exists, if not create it
def job_directory_checker(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

def run():

    print()
    print('Job Finder')
    print('-----------')

    run_again = True


    while run_again:

        # Search_term to search for
        search_term = input('Enter a search term (for example python): ')

        # Area to search for, currently only pääkaupunkiseutu
        area = input('Enter an area (for example pääkaupunkiseutu or helsinki): ')

        # Full_time or part_time
        try:
            type_of_work_choice = int(input('Enter type of work (1 = full_time, 2 = part_time): '))

            match type_of_work_choice:
                case 1:
                    type_of_work = 'full_time'
                case 2:
                    type_of_work = 'part_time'
                case _:
                    print('Invalid choice, defaulting to full_time')
                    type_of_work = 'full_time'

        except ValueError:
            print('Invalid choice, defaulting to full_time')
            print()
            type_of_work = 'full_time'

        # Create the path and filename
        path_to_job_folder = 'src/csv_files/'

        filename = f'{area}_{type_of_work}_{search_term}{'_' if search_term else ''}jobs.csv'

        job_directory_checker(path_to_job_folder)

        # Run the job finder function and save the data to a CSV file
        found_jobs = finder(search_term, area, type_of_work)

        if found_jobs is None or len(found_jobs) == 0:
            print('No jobs found\n')
        else:
            writer(found_jobs, path_to_job_folder, filename)
            reader(path_to_job_folder, filename)

        # Ask the user if they want to search again
        answer = input('Search again? (y/n): ')

        if answer.lower() == 'n':
            run_again = False


    print('Exiting...')
    print()