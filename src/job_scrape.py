#!/usr/bin/env python3

"""Short-cut program for scraping job listings, using the 'job_data' and 'job_analysis' programs"""

# Program structure so far:
# 1. Get a page URL of job listings
# 2. Download that page's source code
# 3. Retrieve each job listing from the page
# 4. Do processing on each listing of the page

## Libraries

# Standard
import os

# Own
import job_data
import job_analysis

# Website to be scraped: 'jobs.ie'

def get_recent():
    """Use the most recent pickled list of jobs that also is 'not too old'"""
    path = '.'
    modification_time = datetime.datetime.fromtimestamp(os.stat(path).st_mtime)

def main():
    url_global = 'https://www.jobs.ie/Jobs.aspx' # 'front-page' of all the job listings
    print('Getting {}...'.format(url_global))

    response = job_data.get_response(url_global) # retrieve the page
    job_data.cache_response(response, dir_path='./../page_cache/') # save the retrieved
    job_data.save_page(response, file_path='./../test_data/front_page.html') # save page

    # extract a list of jobs with associated information
    print('Processing...')
    jobs = job_data.process(response)

    print('Saving...')
    # save the data extracted
    job_data.save_processed(jobs, dir_path='./../data/')
    print(jobs)

    print('Analysis...')
    print('Filtering jobs just for you...')
    keyword = 'office'
    matching_jobs = [job for job in jobs if job_analysis.keyword_present(keyword, job)]
    print(matching_jobs)

    print('Finished')

if __name__ == '__main__':
    main()