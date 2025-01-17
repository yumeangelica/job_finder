from src.agent_program import user_agent_switcher
from bs4 import BeautifulSoup
import requests
import time

def clean_text(text: str) -> str:
    """Remove unwanted characters from text."""
    if text:
        return text.replace('–', '').strip()
    return text

def finder(search_term: str, area: str, type_of_work: str):
    """Find jobs from job board"""
    base_url = f'https://duunitori.fi/tyopaikat?haku={search_term}&alue={area}&filter_work_type={type_of_work}&order_by=date_posted'
    jobs_data = []
    time_for_sleep = 5
    max_retries = 3
    user_agent_generator = user_agent_switcher() # Initialize user agent generator

    try:
        session = requests.Session()
        session.headers.update({ # Set headers
            'User-Agent': next(user_agent_generator),
            'Referer': 'https://duunitori.fi',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
        })

        response = session.get(base_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser') # Parse the HTML

        pagination = soup.find_all('a', class_='pagination__pagenum') # Find the pagination element
        last_page = int(pagination[-1].text.strip()) if pagination else 1 # Get the last page number

        for page in range(1, last_page + 1): # Loop through the pages
            page_url = f"{base_url}&sivu={page}"
            retries = 0

            while retries < max_retries:
                try:
                    session.headers.update({'User-Agent': next(user_agent_generator)}) # Update the user agent for each request
                    response = session.get(page_url, timeout=10)
                    response.raise_for_status()

                    soup = BeautifulSoup(response.text, 'html.parser') # Parse the HTML
                    jobs = soup.find_all('div', class_='job-box') # Find the job boxes on the page

                    if not jobs:
                        print(f"No jobs found on page {page}. Ending search.")
                        return jobs_data

                    for job in jobs: # Loop through the job boxes
                        try:
                            link_elem = job.find('a', class_='job-box__hover')
                            title_elem = job.find('h3', class_='job-box__title')
                            company_elem = job.find('span', class_='job-box__job-location')

                            title = clean_text(title_elem.text) if title_elem else None
                            company = clean_text(company_elem.text) if company_elem else None
                            url = f"https://duunitori.fi{link_elem['href']}" if link_elem and 'href' in link_elem.attrs else None

                            if title and company and url:
                                jobs_data.append([title, company, url])

                        except Exception as e:
                            print(f"Error extracting job data: {e}")
                            continue

                    print(f"Page {page} processed successfully.")
                    break

                except requests.exceptions.RequestException as e:
                    print(f"Error on page {page}: {e}")
                    retries += 1
                    if retries == max_retries:
                        print(f"Max retries reached for page {page}. Skipping.")

            time.sleep(time_for_sleep)

        return jobs_data # Return the list of jobs

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []
