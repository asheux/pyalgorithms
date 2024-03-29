import os
import requests
import pprint

from itertools import permutations
from time import sleep

def make_api_call(payload, cookies):
    host = 'https://hack.ainfosec.com/challenge/submit-answer/'
    try:
        res = requests.post(host, data=payload, cookies=cookies)
        return res
    except Exception as e:
        raise e

def break_alpha_numeric_code():
    alphanum = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz"
    cookies = {
        "csrftoken": os.environ.get('CSRTOKEN'),
        "sessionid": os.environ.get('SESSIONID')
    }
    payload = {
        "csrfmiddlewaretoken": os.environ.get('CSRFMIDDLEWARETOKEN'),
        "challenge_id": "code_breaker"
    }
    count = 0
    previous_score = 0
    result = []
    i = 0
    j = len(alphanum)

    while i < j:
        char = alphanum[i]
        answer = ''.join(result + [char])
        payload['answer'] = answer
        print('Breaking the alphanumeric code.')
        print(f'Trying {answer}')
        response = make_api_call(payload, cookies)
        score = response.json()['hc_challenge']['score']
        print(f'Done with score of {score}')
        print()

        if score > previous_score:
            previous_score = score
            result.append(char)
            count += 1
            if count == 7:
                break

            # reset
            first = alphanum[:i]
            last = alphanum[i:]
            i = 0
            alphanum = last + first
            continue
        i += 1
    print(f'Code breaking complete. Alpha code is: {"".join(result)}')

if __name__ == '__main__':
    break_alpha_numeric_code()
