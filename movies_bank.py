from tmdbv3api import TMDb, Discover
from tmdbv3api import Movie
from bot_movie import BotMovie
from datetime import date
import random
import requests
from credentials import TMDB_API_KEY

IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"


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
        self.tmdb = TMDb()
        self.tmdb.api_key = TMDB_API_KEY
        self.tmdb.language = 'en'
        self.tmdb.debug = True
        self.movie = Movie()

    def _get_movie(self, movie_id):
        m = self.movie.details(movie_id)
        genres = [genre['name'] for genre in m.genres]
        bot_movie = BotMovie(
            movie_id=m.id,
            title=m.title,
            genre="/".join(genres),
            release_date=m.release_date,
            poster_1=IMAGE_BASE_URL + m.poster_path,
            poster_2=IMAGE_BASE_URL + m.backdrop_path,
            overview=m.overview
        )
        print(bot_movie)
        return bot_movie

    def _get_popular_movies(self):
        popular = self.movie.recommendations(111, page=1)
        bot_movies_ids = []
        for m in popular:
            bot_movies_ids.append(m.id)
        return bot_movies_ids

    def _discover_movies(self):
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
        movies = self._discover_movies()
        m = random.choice(movies)
        genres_ids = m.genre_ids
        genres = [genres_dict[genre] for genre in genres_ids]
        bot_movie = BotMovie(
            movie_id=m.id,
            title=m.title,
            genre="/".join(genres),
            release_date=m.release_date,
            poster_1=IMAGE_BASE_URL + m.poster_path,
            poster_2=IMAGE_BASE_URL + m.backdrop_path,
            overview=m.overview
        )
        return bot_movie
