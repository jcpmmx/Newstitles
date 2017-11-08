# NYTimes Titles

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

---

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
