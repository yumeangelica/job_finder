import csv

def writer(data: list, path_to_job_folder: str, filename: str):
    
    with open(path_to_job_folder + filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Company', 'Link'])

        for row in data:
            writer.writerow(row)


def reader(path_to_job_folder: str, filename: str):
    with open(path_to_job_folder + filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        job_count = 0

        for row in reader:
            print(', '.join(row))
            job_count += 1

    job_count -= 1 # subtract the header row

    print(f'Total jobs available: {job_count}') # print the total number of jobs
    print()

