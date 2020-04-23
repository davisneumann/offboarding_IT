import requests
import csv
from pprint import pprint as pp
from config import BASEURL, CLIENT_ID, CLIENT_SECRET, PASSWORD
def main():
        with requests.Session() as s:
            r = s.post(url='https://api.us.onelogin.com/auth/oauth2/v2/token', json={'grant_type': 'client_credentials'}, auth=(CLIENT_ID, CLIENT_SECRET))
            r.raise_for_status()
            s.headers.update({'Authorization': f"Bearer:{r.json()['access_token']}"})
            r = s.get(f'{BASEURL}/groups')
            r.raise_for_status()
            groups = r.json()['data']
            with open('disable_users.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    print(f'{row["username"]} ...')
                    r = s.get(f"{BASEURL}/users", params={'email': row['email']})
                    r.raise_for_status()
                    pp(r.json())
                    uid = r.json()['data'][0]['id']
                    print('  Setting password ...')
                    r = s.put(f'{BASEURL}/users/set_password_clear_text/{uid}', json={
                        'password': PASSWORD,
                        'password_confirmation': PASSWORD,
                        'validate_policy': False
                    })
                r.raise_for_status()
                payload = {
                    'group_id': 452085 ,
                    'status': 2,
                }
                print(f'  Setting group={row["group"]}, forcing password change ...')
                r = s.put(f'{BASEURL}/users/{uid}', json=payload)
                r.raise_for_status()
            print('Done!')
if __name__ == '__main__':
