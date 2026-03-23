import json
import os
import time
import requests
from bs4 import BeautifulSoup
from src.agent_program import user_agent_switcher

_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_config():
    """Load job_program_config.json from the config directory."""
    config_path = os.path.join(_project_root, 'config', 'job_program_config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Config file not found: {config_path}\n"
            f"Create config/job_program_config.json in the project root."
        )


def _find_elements(soup, selector_config):
    """Find elements using primary selector first, then fallbacks.

    Returns:
        (elements, selector_label) tuple.
    """
    primary = selector_config['primary']
    elements = soup.find_all(primary['tag'], class_=primary.get('class'))

    if elements:
        return elements, f"{primary['tag']}.{primary.get('class', '')}"

    for fallback in selector_config.get('fallbacks', []):
        tag = fallback['tag']
        css_class = fallback.get('class')
        attrs = fallback.get('attrs', {})

        if css_class:
            elements = soup.find_all(tag, class_=css_class)
        elif attrs:
            elements = soup.find_all(tag, attrs=attrs)
        else:
            elements = soup.find_all(tag)

        if elements:
            label = f"{tag}.{css_class or attrs}"
            print(f"  info: Primary selector failed, fallback matched: {label}")
            return elements, label

    return [], None


def _find_element(parent, selector_config):
    """Find a single element using the primary -> fallback chain."""
    primary = selector_config['primary']
    elem = parent.find(primary['tag'], class_=primary.get('class'))

    if elem:
        return elem

    for fallback in selector_config.get('fallbacks', []):
        tag = fallback['tag']
        css_class = fallback.get('class')
        attrs = fallback.get('attrs', {})

        if css_class:
            elem = parent.find(tag, class_=css_class)
        elif attrs:
            elem = parent.find(tag, attrs=attrs)

        if elem:
            return elem

    return None


def _validate_page(soup, config):
    """Check if the page is a valid search results page.

    Returns:
        'ok'           - page looks good
        'blocked'      - captcha or bot detection
        'cookie_wall'  - cookie consent blocking content
        'wrong_page'   - doesn't look like duunitori search results
        'empty_page'   - page content is too short
    """
    validation = config['validation']
    page_text = soup.get_text().lower()

    # Is the page too short?
    if len(page_text) < validation['min_page_length']:
        return 'empty_page'

    # Is there a captcha or block?
    for marker in validation['block_markers']:
        if marker in page_text and len(page_text) < 3000:
            return 'blocked'

    # Is it a cookie wall without real content?
    for marker in validation['cookie_markers']:
        if marker in page_text and len(page_text) < 2000:
            return 'cookie_wall'

    # Are we on the right site?
    has_marker = any(m in page_text for m in validation['expected_page_markers'])
    if not has_marker:
        return 'wrong_page'

    return 'ok'


def _clean_text(text: str) -> str:
    """Remove unwanted characters from text."""
    if text:
        return text.replace('–', '').strip()
    return text


def finder(search_term: str, area: str, type_of_work: str):
    """Scrape job listings from duunitori.fi.

    Args:
        search_term: keyword to search for (e.g. 'python')
        area: location filter (e.g. 'helsinki', 'pääkaupunkiseutu')
        type_of_work: 'full_time' or 'part_time'

    Returns:
        List of [title, company, url] lists.
    """
    config = _load_config()
    selectors = config['selectors']
    req = config['request']
    qp = config['query_params']

    # Build query parameters from config
    params = {
        qp['search']: search_term,
        qp['area']: area,
        qp['work_type']: type_of_work,
        qp['order_by']: config['defaults']['order_by']
    }

    jobs_data = []
    user_agent_gen = user_agent_switcher()

    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': next(user_agent_gen),
            **config['headers']
        })

        # Fetch first page and validate page structure
        response = session.get(
            config['base_url'], params=params, timeout=req['timeout']
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, config['parser'])

        # Validate the page before parsing
        status = _validate_page(soup, config)
        if status != 'ok':
            print(f"  Warning: Page issue detected: {status}")
            if status == 'blocked':
                print("  -> Site may have detected a bot. Try again later.")
            elif status == 'cookie_wall':
                print("  -> Cookie wall is blocking content. Headers may need updating.")
            elif status == 'wrong_page':
                print("  -> Page doesn't look like duunitori search results.")
            elif status == 'empty_page':
                print("  -> Page has insufficient content.")
            return []

        # Determine total number of pages from pagination
        pag_elements, _ = _find_elements(soup, selectors['pagination'])
        last_page = int(pag_elements[-1].text.strip()) if pag_elements else 1
        last_page = min(last_page, req['max_pages'])  # Safety cap

        print(f"Found {last_page} page(s) of results.")

        for page in range(1, last_page + 1):
            retries = 0

            while retries < req['max_retries']:
                try:
                    session.headers.update({'User-Agent': next(user_agent_gen)})
                    page_params = {**params, qp['page']: page}

                    response = session.get(
                        config['base_url'],
                        params=page_params,
                        timeout=req['timeout']
                    )

                    # Retry on specific status codes with backoff
                    if response.status_code in req['retry_status_codes']:
                        retries += 1
                        wait = req['sleep_seconds'] * retries
                        print(f"  Status {response.status_code}, waiting {wait}s... ({retries}/{req['max_retries']})")
                        time.sleep(wait)
                        continue

                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, config['parser'])

                    # Find job elements using the fallback chain
                    jobs, used_selector = _find_elements(soup, selectors['job_container'])

                    if not jobs:
                        print(f"  No listings found on page {page}. Ending search.")
                        return jobs_data

                    # Parse individual job listings
                    page_count = 0
                    for job in jobs:
                        try:
                            title_elem = _find_element(job, selectors['title'])
                            company_elem = _find_element(job, selectors['company'])
                            link_elem = _find_element(job, selectors['link'])

                            title = _clean_text(title_elem.text) if title_elem else None
                            company = _clean_text(company_elem.text) if company_elem else None

                            link_attr = selectors['link'].get('attr', 'href')
                            url = None
                            if link_elem and link_attr in link_elem.attrs:
                                href = link_elem[link_attr]
                                if href.startswith('http'):
                                    url = href
                                else:
                                    url = f"{config['job_url_prefix']}{href}"

                            if title and url:
                                jobs_data.append([title, company or 'Unknown', url])
                                page_count += 1

                        except Exception as e:
                            print(f"  Warning: Failed to parse a listing: {e}")
                            continue

                    print(f"  Page {page}/{last_page} — {page_count} listings")
                    break

                except requests.exceptions.RequestException as e:
                    retries += 1
                    print(f"  Error on page {page} ({retries}/{req['max_retries']}): {e}")
                    if retries >= req['max_retries']:
                        print(f"  -> Skipping page {page}.")

            time.sleep(req['sleep_seconds'])

        print(f"\nTotal: {len(jobs_data)} job listings found.")
        return jobs_data

    except requests.exceptions.RequestException as e:
        print(f"  Error: Network failure on first page: {e}")
        return []
    except Exception as e:
        print(f"  Error: Unexpected failure: {e}")
        return []