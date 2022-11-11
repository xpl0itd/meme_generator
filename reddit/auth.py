import requests
import logging

from . import REDDIT_API_ROOT
from getpass import getpass

logging.basicConfig(level=logging.INFO)


def get_access_token() -> str:
    """
    Gets temp access token for use with reddit API

    Returns:
        (str) : reddit API access token 
    """
    reddit_username = getpass("Reddit username: ")
    reddit_password = getpass("Reddit password : ")

    data = {
        'grant_type': 'password',
        'username': reddit_username,
        'password': reddit_password
    }

    client_id = getpass('Reddit client ID')
    client_secret = getpass('Reddit client secret')
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    headers = {
        'User-Agent': 'MemeMachine/0.0.1'
    }

    try:
        response = requests.post(f'{REDDIT_API_ROOT}/api/v1/access_token', headers=headers, data=data, auth=auth)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        error_message = f"request for access token failed: {e}"
        logging.error(error_message)
        raise

    access_token = response.json().get('access_token')
    if not access_token:
        error_message = f"no access token in response: {response.text}"
        logging.error(error_message)
        raise requests.exceptions.HTTPError(error_message)

    return access_token