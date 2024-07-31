import requests
from bs4 import BeautifulSoup


def get_job_info(job_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(job_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    job_title = soup.find('h1', {'class': 'topcard__title'}).get_text(strip=True)
    company_name = soup.find('a', {'class': 'topcard__org-name-link'}).get_text(strip=True)
    job_location = soup.find('span', {'class': 'topcard__flavor topcard__flavor--bullet'}).get_text(strip=True)
    job_description = soup.find('div', {'class': 'description__text description__text--rich'}).get_text(strip=True)
    job_description = job_description[:200] #limit to 200 characters 
    # Job types could be multiple (fulltime, hybrid, etc)
    job_types = []
    job_type_element = soup.find('li', {'class': 'job-details-jobs-unified-top-card__job-insight job-details-jobs-unified-top-card__job-insight--highlight'})
    if job_type_element:
        spans = job_type_element.find_all('span')
        for span in spans:
            text = span.get_text(strip=True)
            if text:  # Ensure that empty text is not added
                job_types.append(text)

    job_info = {
        'Job Title': job_title,
        'Company Name': company_name,
        'Location': job_location,
        'Job Description': job_description,
        'Job Types': job_types if job_types else ['Not specified']
    }
    return job_info

#Example
link = "https://www.linkedin.com/jobs/view/3977530761/"
job_info = get_job_info(link)

if job_info:
    for key, value in job_info.items():
        if isinstance(value, list):
            print(f"{key}: {', '.join(value)}")
        else:
            print(f"{key}: {value}")
