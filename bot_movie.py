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
