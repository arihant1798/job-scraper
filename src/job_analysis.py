#!/usr/bin/env python3

"""Analyse a list of jobs with information about them and give a recommendation"""

import re

def keyword_present(kw, data_item):
    """Return a Boolean indicating if a job item (dictionary) contains the supplied string keyword (not embedded in another word) in its title or description snippet (a filter basically)"""
    # To-do: accept multiple keywords (a list)
    # To-do: case-insensitive matching - re flag 'i'?
    # To-do: get the pattern strings working - need a keyword 'placeholder' inside them
    # temporary solution
    r = r'\b' + '{}'.format(kw) + r'\b' # returns a string with escaped special characters
    title_r = re.findall(r, data_item['job-title'])
    descr_r = re.findall(r, data_item['job-descr-snip'])
    return bool(title_r or descr_r) # there might be a better solution than calling the constructor

def keyword_count(kws_count, data):
    pass

def word_frequencies(data):
    pass

def match(data, person):
    pass