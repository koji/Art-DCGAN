import os

import time
import traceback

import flickrapi
from urllib.request import urlretrieve

import sys
from retry import retry

flickr_api_key = "api_key"
secret_key = "secret_key"

keyword = sys.argv[1]
print(keyword)


@retry()
def get_photos(url, filepath):
    urlretrieve(url, filepath)
    time.sleep(1)


if __name__ == '__main__':

    flicker = flickrapi.FlickrAPI(
        flickr_api_key, secret_key, format='parsed-json')
    response = flicker.photos.search(
        text=keyword,
        per_page=1000,
        media='photos',
        sort='relevance',
        safe_search=1,
        extras='url_q,url_c,license'
    )
    photos = response['photos']

    try:
        if not os.path.exists('./image-data/' + keyword):
            os.mkdir('./image-data/' + keyword)

        for photo in photos['photo']:
            #url_q = photo['url_q']
            url_c = photo['url_c']
            filepath = './image-data/' + keyword + '/' + photo['id'] + '.jpg'
            #get_photos(url_q, filepath)
            get_photos(url_c, filepath)

    except Exception as e:
        traceback.print_exc()
