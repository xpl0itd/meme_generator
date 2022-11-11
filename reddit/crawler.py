import json
import shutil
import requests
import logging

from random import shuffle
from . import REDDIT_API_ROOT
from reddit.auth import get_access_token


logging.basicConfig(level=logging.INFO)

def acquire_meme(moisture: int) -> None:
    """
    Performs search on r/memes for moist memes and downloads them in project directory

    Parameters:
        moisture (int) : The current humidity % / moistness for a provided location
    """
    access_token = get_access_token()
    headers = {'User-Agent': 'MemeMachine/0.0.1', 'Authorization': f'Bearer: {access_token}'}

    try:
        response = requests.get(f'{REDDIT_API_ROOT}/r/memes/search.json?q=memes&limit=100', headers=headers)
        response.raise_for_status()

        results = response.json()

        shuffle(results['data']['children'])
        for result in results['data']['children']:
            meme_found = False
            result = result['data']
            upvotes = result['ups']
            downvotes = result['downs']

            amount_liked = (upvotes / (upvotes + downvotes)) * 100
            if amount_liked >= moisture:
                meme = result['url']
                for extension in ('png', 'jpg'):
                    if extension in meme:
                        meme_found = True
                        response = requests.get(meme, stream=True)
                        with open(f'meme.{extension}', 'wb') as f:
                            shutil.copyfileobj(response.raw, f)

                    
            if meme_found:
                break

    except requests.exceptions.HTTPError as e:
        error_message = f"failed search request to r/memes: {e}"
        logging.error(error_message)
        raise
