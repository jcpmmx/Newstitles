# -*- coding: utf-8 -*-

"""
Newstitles
---

The task is to write a function that produces a list of article titles from The NY Times (www.nytimes.com) and then
sorts them by the sum of each title's tokens frequency (let's call this sum `weight` -a token is just a word separated
by whitespace) among all titles. The output should be this sorted list along with the score for each article title.

For example, if the titles are:
- Trump goes to Japan
- Shooting in Texas
- Japan and North Korea in talks
- Trump offends Australian people
- Judges visit Trump

Let's calculate each title's weight, starting with the first one.
In this case, token `Trump` appears 3 times among all titles. `goes`, 1 time. `to`, 1 time. `Japan`, 2 times.
Adding up all token frequencies gives us: 3 + 1 + 1 + 2 = 7.

The sorted list would be:
- Japan and North Korea in talks (8)
- Trump goes to Japan (7)
- Trump offends Australian people (6)
- Judges visit Trump (5)
- Shooting in Texas (4)

########################################################################################################################

Implementation details
---

Requires:
- Python 2.7.10
- requests 2.18.4
- lxml 4.1.1

This script has some settings hardcoded to run use the base case: titles from The NY Times.
To run it, just do:
```
$ python newtitles.py
```
In case you want to run it with different settings, modify these 2 vars:
 - `TARGET_URL`: URL of the site to analyze (e.g. `https://www.nytimes.com`)
 - `TARGET_SELECTOR`: XPath selector of the expected location of each title (e.g. `/html/body//article@title`)

Notes:
- We're assuming English as language
- For simplicity, all chars other than alphanumeric ones are stripped and we will ignore single chars
"""


from __future__ import print_function, unicode_literals

import re
from collections import Counter

import requests
from lxml import html


TARGET_URL = 'https://www.nytimes.com'
TARGET_SELECTOR = '/html/body//article/*[@class="story-heading"]/a/text()'


def get_html_data(url):
    """
    Returns the HTML data of the given URL, if any and if request is successful.

    :param url: The site to retrieve the HTML from
    :return: The HTML data of the given URL
    """
    response = requests.get(url)
    if response.ok:
        return response.text
    return ''


def get_all_titles(html_data, selector=TARGET_SELECTOR):
    """
    Returns a list of all titles found as specified by the XPath `selector`, if any.

    :param html: The HTML data to analyze
    :param selector: The XPath selector of the titles
    :return: A list of all titles found in the given HTML data using the given selector
    """
    try:
        html_tree = html.fromstring(html_data)  # WARNING: Potentially heavy operation if input data is large enough
        return [unicode(x).strip() for x in html_tree.xpath(selector)]
    except Exception:
        return []


def create_frequency_table(titles):
    """
    Returns a sorted dict containing all tokens inside the given titles and their frequency among all titles.

    To make the table smaller, it will remove those words with frequency = 1. Why? When we're doing a lookup in the
    frequency table and some word is missing, we will know it's the first time we analyze it.

    e.g. if `titles` = ['Trump goes to Japan', 'Trump offends Australian people'], the frequency table will look like:
    {
        'trump': 2,
    }

    :param html: The HTML data to analyze
    :param selector: The XPath selector of the titles
    :return: A list of all titles found in the given HTML data using the given selector
    """
    frequency_table = Counter()
    for title in titles:
        # Calculating the frequency of words in the current title and adding it to the main table
        frequency_table.update(Counter(_get_all_words(title)))
    # Removing words with frequency = 1 to make the table smaller
    frequency_table = {k: v for k, v in frequency_table.items() if v > 1}
    return frequency_table


def get_titles_by_weight(titles, frequency_table=None, sort=False):
    """
    Returns a list of all titles and their weight as determined by the given frequency table.

    :param titles: All titles to analyze
    :param frequency_table: The frequency of all token's occurrences among all titles
    :param sort: Whether to sort the final list of titles or not (in descending order)
    :return: A list of all titles and their weight
    """
    if not frequency_table:
        frequency_table = {}

    weights_data = []  # A list of tuples of (weight, title)
    for title in titles:
        title_weight = _get_title_weight(title, frequency_table=frequency_table)
        weights_data.append((title_weight, title))

    if sort:
        weights_data = sorted(weights_data, key=lambda x: x[0], reverse=True)
    return weights_data


def _get_all_words(text):
    """
    Internal method that uses regex to return all words found in a given text.

    It doesn't include single chars found after regex operation runs (e.g. like when `it's` becomes `it s`).
    All returned words will be in lowercase.

    :param text: The text to find words in
    :return: All words found in text
    """
    return [word.lower() for word in re.findall(r'\b([a-zA-Z]+)\b', text) if len(word) > 1]


def _get_title_weight(title, frequency_table=None):
    """
    Internal method that returns the weight of the given title, using the given frequency table as base to calculate
    each token's frequency.

    :param title: The title to calculate the weight for
    :param frecuency_table: The frequency of all token's occurrences among all titles
    :return: The weight of the title (i.e. the sum of each title's tokens frequency)
    """
    if not frequency_table:
        frequency_table = {}
    return sum(map(lambda word: frequency_table.get(word, 1), _get_all_words(title)))


# Main script execution flow
if __name__ == '__main__':

    def _pretty_titles(titles, limit=0):
        # Small helper just to pretty print the results of `get_titles_by_weight`
        if limit:
            titles = titles[:limit]
        return '\n'.join('{title} ({weight})'.format(title=title, weight=weight) for weight, title in titles)

    # Getting the HTML, then finding all titles in it and building the frequency table
    site_html = get_html_data(TARGET_URL)
    all_titles = get_all_titles(site_html)
    frequency_table = create_frequency_table(all_titles)

    # Calculating the weight of each title and returning a list of all titles and their weight
    titles = get_titles_by_weight(all_titles, frequency_table=frequency_table)
    print('-------')
    # Without sort, to check the original order
    print(_pretty_titles(titles, limit=10))
    print('-------')
    sorted_titles = get_titles_by_weight(all_titles, frequency_table=frequency_table, sort=True)
    # Sorted this time
    print(_pretty_titles(sorted_titles, limit=10))
    print('-------')
