import requests
import pytz
from datetime import datetime

def get_amount_pages():
    url = 'https://devman.org/api/challenges/solution_attempts/'
    response = requests.get(
        url=url,
        params={
            'page': 1
        }
    )
    return response.json()['number_of_pages']


def load_attempts():
    pages = get_amount_pages()
    url = 'https://devman.org/api/challenges/solution_attempts/'
    for page in range(1, pages + 1):
        response = requests.get(
            url=url,
            params={
                'page': page
            }
        ).json()
        attempts_list = response['records']
        for attempt in attempts_list:
            yield attempt


def is_user_midnighter(attempt):
    timezone = pytz.timezone(attempt['timezone'])
    time = datetime.fromtimestamp(attempt['timestamp'], tz=timezone)
    end_of_night = 8
    return time.hour <= end_of_night


def get_midnighters(attempts):
    midnighters = set()
    for attempt in attempts:
        if is_user_midnighter(attempt):
            midnighters.add(attempt['username'])
    return midnighters


if __name__ == '__main__':
    midnighters = get_midnighters(load_attempts())
    if len(midnighters) == 0:
        print('There is no midnighters')
    else:
        print('List of midnighters:')
        for midnighter in midnighters:
            print(midnighter)
