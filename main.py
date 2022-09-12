import os

import tweepy
import requests

from credentials import API_KEY
from credentials import API_KEY_SECRET
from credentials import CLIENT_ID
from credentials import CLIENT_SECRET
from movies_bank import MovieBank


def main():
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(CLIENT_ID, CLIENT_SECRET)
    api = tweepy.API(auth)

    def upload_image(image_url, file_name):
        request = requests.get(image_url, stream=True)
        if request.status_code == 200:
            with open(file_name, 'wb') as image:
                for chunk in request:
                    image.write(chunk)
            res = api.media_upload(file_name).media_id
            return res
        else:
            print("Unable to download image")

    def write_media_tweet(movie, tweet_text, reply_text):
        # Upload images and get media_ids
        image_urls = [movie.poster_1]  # , movie.poster_2]
        media_ids = []
        for image_url in image_urls:
            file_name = "temp" + str(image_urls.index(image_url))
            media_ids.append(upload_image(image_url, file_name))
            os.remove(file_name)

        # Tweet with multiple images
        tweet = api.update_status(status=tweet_text.ljust(280)[:280].strip(), media_ids=media_ids)
        api.update_status(status=reply_text.ljust(280)[:280].strip(), in_reply_to_status_id=tweet.id_str, auto_populate_reply_metadata=True)

    def tweet_random_movie():
        movies_bank = MovieBank()
        movie = movies_bank.get_random_movie()
        tweet_text = movie.get_tweet_text()
        reply_text = movie.get_reply_text()
        write_media_tweet(movie, tweet_text, reply_text)

    try:
        api.verify_credentials()
        print("Authentication Successful")
        tweet_random_movie()
    except Exception as e:
        print(e)
        print("Authentication Error")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
