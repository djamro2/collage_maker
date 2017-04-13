
"""
Gets the top 12 images from /r/uiuc in the last year
Done for testing now, later can be used in actual code
"""


import os
import sys
import praw
import json

from time import time
from imgur_helper import get_image_link

def convert_days(days):
    return {
        'seconds': days * 24 * 60 * 60,
        'minutes': days * 24 * 60,
        'hours': days * 24,
        'days': days
    }

def convert_seconds(seconds):
    return {
        'seconds': seconds,
        'minutes': seconds * 60,
        'hours': seconds * 60 * 60,
        'days': seconds * 60 * 60 * 24
    }

def create_reddit_instance():
    return praw.Reddit(client_id=api_client_id,
                     client_secret=api_key_secret,
                     user_agent='Image collage by /u/donovan28')

def dict_to_file(obj, filename):
    with open(filename, 'w') as fp:
        json.dump(obj, fp)

def get_all_submissions(subreddit):
    submissions = []
    time_upper_bound = current_time
    time_lower_bound = current_time - convert_days(1)['seconds']
    time_lower_limit = current_time - max_past_seconds
    current_day = 0
    while(time_upper_bound > time_lower_limit):
        try:
            for submission in subreddit.submissions(time_lower_bound, time_upper_bound):
                submissions.append(submission)
            time_upper_bound = time_lower_bound
            time_lower_bound -= convert_days(1)['seconds']
            time_lower_bound = max(time_lower_bound, time_lower_limit)
            current_day += 1
            print('Saved a day of posts, day {0}'.format(current_day))
        except Exception as e:
            print('Exception in submissions, continuing')
    return submissions

def get_images(subreddit_name='uiuc', num_images=12):
    reddit = create_reddit_instance()
    subreddit = reddit.subreddit(subreddit_name)
    submissions = get_all_submissions(subreddit)
    img_submissions = get_img_submissions(submissions)
    submissions_dict = submissions_to_dict(img_submissions)
    return submissions_dict

def get_img_submissions(submissions):
    img_submissions = []
    for submission in submissions:
        url = submission.url
        if is_regular_image(url) or is_imgur_image(url):
            img_submissions.append(submission)
    return img_submissions

def is_imgur_image(url):
    return 'imgur' in url

def is_regular_image(url):
    if not url:
        return False
    return '.png' in url or '.jpg' in url or '.jpeg' in url

def submissions_to_dict(submissions):
    results = []
    for submission in submissions:
        post = {}
        url = submission.url

        if is_regular_image(url):
            post['is_regular'] = True
            post['raw_url'] = submission.url
        elif is_imgur_image(url):
            post['is_regular'] = False
            post['raw_url'] = get_image_link(url)

        # at this point 'raw_url' should be an image link
        if not is_regular_image(url):
            continue

        post['url'] = submission.url,
        post['score'] = submission.score,
        post['title'] = submission.title,
        post['created'] = submission.created

        results.append(post)

    return results

# set the current time and max time offset
current_time = round(time())   
max_past_days = 5
max_past_seconds = convert_days(max_past_days)['seconds']

# get the api key from the secret folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from secret.secret import api_key_secret, api_client_id

if __name__ == '__main__':
    posts = get_images()
    print('Found {0} image posts'.format(len(posts)))
    dict_to_file(posts, 'img_submissions.json')