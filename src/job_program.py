from src.agent_program import user_agent_switcher
from bs4 import BeautifulSoup
import requests
import time



def finder(search_term: str, area: str, type_of_work: str):

    base_url = f'https://duunitori.fi/tyopaikat?haku={search_term}&alue={area}&filter_work_type={type_of_work}&order_by=date_posted'
    jobs_data = []
    time_for_sleep = 1 # time to sleep between requests. You can change this to whatever you want with caution
    user_agent_generator = user_agent_switcher()

    try:
        session = requests.Session()

        session.headers.update({'User-Agent': next(user_agent_generator)})

        response = session.get(base_url, timeout=10) # timeout after 10 seconds if the request takes too long

        if not response.ok:
            raise Exception(f'An error occurred: {response.status_code}')

        
        soup = BeautifulSoup(response.text, 'lxml')
        page_numbers = soup.find_all('a', class_='pagination__pagenum')

        if len(page_numbers) == 0:
            return jobs_data # return an empty list if there are no jobs
        
        time.sleep(time_for_sleep) # sleep amount of time_for_sleep -variable seconds, so we don't spam the website

        
        last_page_num = int(page_numbers[-1].text.strip())

        for page in range(1, last_page_num + 1):

            session.headers.update({'User-Agent': next(user_agent_generator)}) # update the user agent for each request

            page_url = f'{base_url}&sivu={page}'
            response = session.get(page_url, timeout=10)
            soup_parsed = BeautifulSoup(response.text, 'lxml')

            jobs_found_in_page = soup_parsed.find_all('a', class_='job-box__hover gtm-search-result')

            for job in jobs_found_in_page:
                company = job.get('data-company')
                title = job.text.strip()
                link = 'https://duunitori.fi' + job.get('href')
                jobs_data.append([title, company, link])

            print(f'Page {page} searched')
            time.sleep(time_for_sleep) # sleep amount of time_for_sleep -variable seconds, so we don't spam the website

        return jobs_data

    except Exception as e:
        print(f'An error occurred: {e}')











