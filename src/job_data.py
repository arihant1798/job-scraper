#!/usr/bin/env python3

"""Program with functions to retrieve, process, and save a local copy of various data from a website"""

## Libraries

# Standard
import datetime
import random
import pickle

# Third-party
import requests
import bs4

def get_response(url):
    """Download a web page with a URL"""
    response = requests.get(url)
    response.raise_for_status() # check if successful
    return response

def cache_response(response, dir_path='./'):
    """Serialise a response object into a file"""
    filename = 'response-{}'.format(datetime.datetime.now().strftime('%H-%M'))
    with open(dir_path+filename, 'w+b') as res_out:
        pickle.dump(response, res_out)

def save_page(response, file_path='./page.html'):
    """Save a response object as a html file representing a web page.
    Uses include later reference (testing)
    Note that CSS and other documents are not included"""
    with open(file_path, 'wb') as page_out:
        for chunk in response.iter_content(chunk_size=65536): # save in 16-bit chunks
            page_out.write(chunk)

def process(response):
    """Return a data structure containing job data (of 'jobs.ie') from a response object"""
    # depending on the HTML structure of a 'jobs.ie' web page

    to_parse = response.text
    soup = bs4.BeautifulSoup(to_parse, 'html.parser') # get a soup object (represents the HTML)

    # get a list of job items (tags)
    job_tags = soup.select('div#page > div.page > section.job-list > article.job-list-item')

    # For each job item, there are associated selectors containing some piece of data about the job
    # The following are some 'selector strings' using which data will be extracted
    date_s = 'span.date'
    title_s = 'span.job > h2 > a'
    descr_s = 'span.job > span.snippet > a'
    comp_name_s = 'span.company > span.name > h3 > a'
    location_s = 'span.location'
    # alias for the selectors
    attrs = {'Date':date_s, 'Title':title_s, 'Description':descr_s, 'Company':comp_name_s, 'Location':location_s}

    # Use a list structure to get all the jobs, their details (dictionaries are elements)
    jobs = []
    for j in job_tags:

        # Use a dictionary data structure to save details about a particular job
        # detail -> data
        j_data = {}
        try:
            link = j.select(title_s)[0]['href'].strip()
            posting_date = j.select(date_s)[0].text.strip()
            job_title = j.select(title_s)[0].text.strip()
            job_descr_snip = j.select(descr_s)[0].text.strip() # snippet of the job description
            try:
                company = j.select(comp_name_s)[0].text.strip()
            except IndexError:
                company = 'Not disclosed'
            location = j.select(location_s)[0].text.strip()

            j_data['date'] = posting_date
            j_data['job-title'] = job_title
            j_data['link'] = link
            j_data['job-descr-snip'] = job_descr_snip
            j_data['company'] = company
            j_data['location'] = location
            jobs.append(j_data)
        except Exception as exc:
            print(' encountered a problem with a job ')
            print(exc)
            print(j)

    return jobs

def save_processed(data, dir_path='./'):
    """Save the data structure (by serialising with pickle) to a file"""
    filename = 'job-{}-{}.pkl'.format(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M'), random.randint(0, 1000))
    with open(dir_path+filename, 'wb') as data_out:
        pickle.dump(data, data_out)