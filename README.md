# Movies Twitter Bot
Your Random Movies Generator Bot is here, and can be implemented and deployed in a matter of minutes!

## Features

- Integration with TMDB Open Source API.
- Scheduling the Bot Tasks
- Direct tweeting on Twitter

### Implementation Steps:
- Creating a TMDB Account
- Creating a PythonAnywhere Account
- Creating a Twitter Developer Account
- Installing the TMDB package
- Installing the Tweepy package
- Implementing the Logic
- Scheduling the Code to Run at any preferred time


**Now after you've created your python project. Let us start creating our BOT.**

#### Creating a TMDB Account
The Movie Database (TMDB) is a community built movie and TV database. Every piece of data has been added by their amazing community dating back to 2008.
Since it is for personal and non commercial use, we can join TMDB freely, to do that head to [TMDB Signup](https://www.themoviedb.org/signup "TMDB Signup") and fill the necessary info and that's it. (Check [this ](https://koditips.com/create-tmdb-api-key/ "this ")for the APIs Key Creation)

#### Creating a PythonAnywhere Account
Our main purpose for our bot is to be able to tweet random movies on Twitter on a predefined schedule, and to do that first we need to have a PythonAnywhere account which also can grant us what we need freely.
Now in order to Signup Header to the [Pricing & signup](https://www.pythonanywhere.com/pricing/ "Pricing & signup") screen and click on the ** Create a Beginner account ** and fill all the necessary information.

#### Creating a Twitter Developer Account
Now the final account creation step.
In order to have a Twitter developer account, you need to have a personal twitter account in the first place.
And then you can simply create your are account as per the steps [here](https://www.jcchouinard.com/apply-for-a-twitter-developer-account/ "here") and do not forget to save your generated keys because we will need them in later stages.
And Twitter will review your request and approve it in a matter of a day or two.

#### Installing the TMDB package
After being done with all the accounts creation and setup we need to install the packages needed by our bot.
First package is **TMDBV3 API** which can be installed easily from the terminal.

`$ pip install tmdbv3api`

#### Installing the Tweepy package
Also another package needed by our bot to be able to tweet the generated movies to twitter is the **Tweepy** package, which can also be installed from the terminal.

`$ pip install tweepy`

#### Implementing the Logic
Now the fun part. Lets start coding!

##### credentials file:
first create a credentials.py file which will serve as a safe for the API Keys for both Twitter and TMDB.

    API_KEY = "XXXXXXXXXXXXXXX"
    API_KEY_SECRET = "XXXXXXXXXXXXXXX"
    BEARER_TOKEN = "XXXXXXXXXXXXXXX"
    CLIENT_ID = "XXXXXXXXXXXXXXX"
    CLIENT_SECRET = "XXXXXXXXXXXXXXX"
    TMDB_API_KEY = "XXXXXXXXXXXXXXX"
    TMDB_READ_ACCESS_TOKEN = "XXXXXXXXXXXXXXX"

##### BotMovie class:
Create a bot_movie.py file and inside it decalre the BotMovie class with all the necessary attributes, as below:

    class BotMovie:

    def __init__(self, movie_id, title, genre, release_date, poster_1, poster_2, overview=""):
        self.movie_id = movie_id
        self.title = title
        self.genre = genre
        self.overview = overview
        self.year = "(" + release_date.split("-")[0] + ")"
        self.poster_1 = poster_1
        self.poster_2 = poster_2

    def __str__(self) -> str:
        return f"title={self.title}\ngenre={self.genre}\nyear={self.year}" \
               f"\nposter_1={self.poster_1}\nposter_2={self.poster_2}"

    def get_tweet_text(self):
        # Define the tweet text
        return self.title + " " + self.year + "\n" + "Genre: " + self.genre + "\n\n" + "" + self.overview

##### MovieBank class:
Create a movies_bank.py file and inside it import the necessary packages, and create the MovieBank class with all the necessary attributes, as below:

```python
from tmdbv3api import TMDb, Discover
from tmdbv3api import Movie
from bot_movie import BotMovie
from datetime import date
import random
import requests
from credentials import *


def get_random_year():
    current_year = date.today().year
    random_year = random.randint(1985, current_year)
    return random_year


def get_genres():
    url = "https://api.themoviedb.org/3/genre/movie/list?api_key=" + TMDB_API_KEY + "&language=en-US"
    genres_list = requests.get(url).json()['genres']
    return {genre['id']: genre['name'] for genre in genres_list}


class MovieBank:

    def __init__(self):
        self.IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
        self.tmdb = TMDb()
        self.tmdb.api_key = TMDB_API_KEY
        self.tmdb.language = 'en'
        self.tmdb.debug = True
        self.movie = Movie()

    def __get_movie(self, movie_id):
        m = self.movie.details(movie_id)
        genres = [genre['name'] for genre in m.genres]
        bot_movie = BotMovie(
            movie_id=m.id,
            title=m.title,
            genre="/".join(genres),
            release_date=m.release_date,
            poster_1=self.IMAGE_BASE_URL + m.poster_path,
            poster_2=self.IMAGE_BASE_URL + m.backdrop_path,
            overview=m.overview
        )
        print(bot_movie)
        return bot_movie

    def __get_popular_movies(self):
        popular = self.movie.recommendations(111, page=1)
        bot_movies_ids = []
        for m in popular:
            bot_movies_ids.append(m.id)
        return bot_movies_ids

    def __discover_movies(self):
        discover = Discover()
        return discover.discover_movies({
            'sort_by': 'popularity.desc',
            'include_video': False,
            'primary_release_year': get_random_year(),
            'with_original_language': 'en',
            'language': 'en'
        })

    # get random movie
    def get_random_movie(self):
        genres_dict = get_genres()
        movies = self.__discover_movies()
        m = random.choice(movies)
        genres_ids = m.genre_ids
        genres = [genres_dict[genre] for genre in genres_ids]
        bot_movie = BotMovie(
            movie_id=m.id,
            title=m.title,
            genre="/".join(genres),
            release_date=m.release_date,
            poster_1=self.IMAGE_BASE_URL + m.poster_path,
            poster_2=self.IMAGE_BASE_URL + m.backdrop_path,
            overview=m.overview
        )
        return bot_movie

```

##### Main
Now that all the setup is done all we need is connecting all the dots in the main.py file.

First we authenticate with twitter using the **Twitter API Keys** we declared in the credentials.py file.

```python
# Authenticate to Twitter
auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(CLIENT_ID, CLIENT_SECRET)
api = tweepy.API(auth)
```

Then we declare our final bot functions:

```python
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


def write_media_tweet(movie, tweet_text):
    # Upload images and get media_ids
    image_urls = [movie.poster_1]#, movie.poster_2]
    media_ids = []
    for image_url in image_urls:
        file_name = "temp"+str(image_urls.index(image_url))
        media_ids.append(upload_image(image_url, file_name))
        os.remove(file_name)

    # Tweet with multiple images
    api.update_status(status=tweet_text.ljust(280)[:280].strip(), media_ids=media_ids)


def tweet_random_movie():
    movies_bank = MovieBank()
    movie = movies_bank.get_random_movie()
    tweet_text = movie.get_tweet_text()
    print(tweet_text)
    write_media_tweet(movie, tweet_text)
```

Now, what remains is verifying the twitter api credentials.
If verified successfully, then all set (but don't forget to call the tweet_random_movie function like i did the first time 😂)

```python
try:
    api.verify_credentials()
    print("Authentication Successful")
    tweet_random_movie()
except Exception as e:
    print(e)
```

#### Scheduling the Code to Run at any preferred time
Now the final part.

Head to your pythonAnywhere account that you created earlier and in the Consoles Section start a new console and install in it the packages above you installed in PyCharm.

Then head to the Tasks section and type the following **command**:
`python3 main.py`

And Schedule the process to run at anytime you prefer.

N.B on the Free-tier only 2 tasks can be scheduled on Python Anywhere.

Thanks for reading!


----
