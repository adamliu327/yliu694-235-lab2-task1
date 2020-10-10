from datetime import date, datetime
from typing import List, Iterable


class Director:

    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    def __repr__(self):
        return f'<Director {self.__director_full_name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.director_full_name == self.director_full_name

    def __lt__(self, other):
        return self.director_full_name < other.director_full_name

    def __hash__(self):
        return hash(self.__director_full_name)


class Actor:

    def __init__(self, actor_full_name: str, description: str, hyperlink: str, image_hyperlink: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_full_name.strip()

        self.__description = description
        self.__hyperlink = hyperlink
        self.__image_hyperlink = image_hyperlink

        self.__acted_movies: List[Movie] = list()
        self.__actors_this_one_has_worked_with = set()

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    @property
    def description(self) -> str:
        return self.__description

    @property
    def hyperlink(self) -> str:
        return self.__hyperlink

    @property
    def image_hyperlink(self) -> str:
        return self.__image_hyperlink

    @property
    def acted_movies(self):
        return self.__acted_movies

    @property
    def actors_this_one_has_worked_with(self):
        return self.__actors_this_one_has_worked_with

    def add_actor_colleague(self, colleague):
        if colleague not in self.__actors_this_one_has_worked_with:
            if isinstance(colleague, self.__class__):
                self.__actors_this_one_has_worked_with.add(colleague)
                colleague.add_actor_colleague(self)

    def check_if_this_actor_worked_with(self, colleague):
        return colleague in self.__actors_this_one_has_worked_with

    def is_applied_to(self, movie) -> bool:
        return movie in self.__acted_movies

    def add_movie(self, movie):
        if isinstance(movie, Movie):
            self.__acted_movies.append(movie)

    def __repr__(self):
        return f'<Actor {self.__actor_full_name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.actor_full_name == self.__actor_full_name

    def __lt__(self, other):
        return self.__actor_full_name < other.actor_full_name

    def __hash__(self):
        return hash(self.__actor_full_name)


class Review:

    def __init__(self, movie, user, review_text: str, rating: int, timestamp: datetime):
        if isinstance(movie, Movie):
            self.__movie = movie
        else:
            self.__movie = None
        if type(review_text) is str:
            self.__review_text = review_text
        else:
            self.__review_text = None
        if type(rating) is int and 1 <= rating <= 10:
            self.__rating = rating
        else:
            self.__rating = None
        self.__timestamp: datetime = timestamp
        self.__user = user


    @property
    def movie(self):
        return self.__movie

    @property
    def review_text(self) -> str:
        return self.__review_text

    @property
    def rating(self) -> int:
        return self.__rating

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    @property
    def user(self):
        return self.__user

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.movie == self.__movie and other.review_text == self.__review_text and other.rating == self.__rating and other.timestamp == self.__timestamp

    def __repr__(self):
        return f'<Review of movie {self.__movie}, rating = {self.__rating}, timestamp = {self.__timestamp}>'


class Movie:

    def __set_title_internal(self, title: str):
        if title.strip() == "" or type(title) is not str:
            self.__title = None
        else:
            self.__title = title.strip()

    def __set_release_year_internal(self, release_year: int):
        if release_year >= 1900 and type(release_year) is int:
            self.__release_year = release_year
        else:
            self.__release_year = None

    def __init__(self, title: str, release_year: int, description: str, hyperlink: str, image_hyperlink: str, movie_id: int = None):

        self.__set_title_internal(title)
        self.__set_release_year_internal(release_year)

        self.__movie_id = movie_id
        self.__description = description
        self.__director = None
        self.__actors = []
        self.__genres = []
        self.__runtime_minutes = None
        self._hyperlink: str = hyperlink
        self._image_hyperlink: str = image_hyperlink
        self._reviews: List[Review] = list()

    # essential attributes

    @property
    def movie_id(self) -> int:
        return self.__movie_id

    @movie_id.setter
    def movie_id(self, movie_id: int):
        self.__movie_id = movie_id

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, title: str):
        self.__set_title_internal(title)

    @property
    def release_year(self) -> int:
        return self.__release_year

    @release_year.setter
    def release_year(self, release_year: int):
        self.__set_release_year_internal(release_year)

    # additional attributes

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str):
        if type(description) is str:
            self.__description = description.strip()
        else:
            self.__description = None

    @property
    def director(self) -> Director:
        return self.__director

    @director.setter
    def director(self, director: Director):
        if isinstance(director, Director):
            self.__director = director
        else:
            self.__director = None

    @property
    def actors(self) -> list:
        return self.__actors

    @property
    def hyperlink(self) -> str:
        return self._hyperlink

    @property
    def image_hyperlink(self) -> str:
        return self._image_hyperlink

    @property
    def reviews(self) -> Iterable[Review]:
        return iter(self._reviews)

    def add_review(self, review: Review):
        self._reviews.append(review)

    def add_actor(self, actor: Actor):
        if not isinstance(actor, Actor) or actor in self.__actors:
            return

        self.__actors.append(actor)

    def remove_actor(self, actor: Actor):
        if not isinstance(actor, Actor):
            return

        try:
            self.__actors.remove(actor)
        except ValueError:
            # print(f"Movie.remove_actor: Could not find {actor} in list of actors.")
            pass

    @property
    def genres(self) -> list:
        return self.__genres

    def add_genre(self, genre):
        if not isinstance(genre, Genre) or genre in self.__genres:
            return

        self.__genres.append(genre)

    def remove_genre(self, genre):
        if not isinstance(genre, Genre):
            return

        try:
            self.__genres.remove(genre)
        except ValueError:
            # print(f"Movie.remove_genre: Could not find {genre} in list of genres.")
            pass

    @property
    def runtime_minutes(self) -> int:
        return self.__runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, val: int):
        if val > 0:
            self.__runtime_minutes = val
        else:
            raise ValueError(f'Movie.runtime_minutes setter: Value out of range {val}')


    def __get_unique_string_rep(self):
        return f"{self.__title}, {self.__release_year}"

    def is_tagged(self):
        return len(self.__genres) > 0

    def is_tagged_by(self, genre):
        return genre in self.__genres

    def __repr__(self):
        return f'<Movie {self.__get_unique_string_rep()}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__get_unique_string_rep() == other.__get_unique_string_rep()

    def __lt__(self, other):
        if self.title == other.title:
            return self.release_year < other.release_year
        return self.title < other.title

    def __hash__(self):
        return hash(self.__get_unique_string_rep())


class Genre:

    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self.__genre_name = None
        else:
            self.__genre_name = genre_name.strip()

        self._movie_with_genre: List[Movie] = list()

    @property
    def genre_name(self) -> str:
        return self.__genre_name

    @property
    def movie_with_genre(self) -> list:
        return self._movie_with_genre

    def is_applied_to(self, movie: Movie) -> bool:
        return movie in self._movie_with_genre

    def add_movie(self, movie: Movie):
        self._movie_with_genre.append(movie)

    @property
    def number_of_tagged_movies(self):
        return len(self._movie_with_genre)

    def __repr__(self):
        return f'<Genre {self.__genre_name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.genre_name == self.__genre_name

    def __lt__(self, other):
        return self.__genre_name < other.genre_name

    def __hash__(self):
        return hash(self.__genre_name)


class User:

    def __init__(self, user_name: str, password: str):
        if user_name == "" or type(user_name) is not str:
            self.__user_name = None
        else:
            self.__user_name = user_name.strip().lower()
        if password == "" or type(password) is not str:
            self.__password = None
        else:
            self.__password = password
        self.__watched_movies = list()
        self.__reviews = list()
        self.__time_spent_watching_movies_minutes = 0

    @property
    def user_name(self) -> str:
        return self.__user_name

    @property
    def password(self) -> str:
        return self.__password

    @property
    def watched_movies(self) -> list:
        return self.__watched_movies

    @property
    def reviews(self) -> list:
        return self.__reviews

    @property
    def time_spent_watching_movies_minutes(self) -> int:
        return self.__time_spent_watching_movies_minutes

    def watch_movie(self, movie: Movie):
        if isinstance(movie, Movie):
            self.__watched_movies.append(movie)
            self.__time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review: Review):
        if isinstance(review, Review):
            self.__reviews.append(review)

    def __repr__(self):
        return f'<User {self.__user_name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.user_name == self.__user_name

    def __lt__(self, other):
        return self.__user_name < other.user_name

    def __hash__(self):
        return hash(self.__user_name)


class WatchList:

    def __init__(self):
        self.WatchList = list()
        pass

    def add_movie(self, movie: Movie):
        if movie not in self.WatchList:
            self.WatchList.append(movie)

    def remove_movie(self, movie: Movie):
        if movie in self.WatchList:
            self.WatchList.remove(movie)

    def select_movie_to_watch(self, index):
        if index <= len(self.WatchList) - 1:
            return self.WatchList[index]
        else:
            return None

    def size(self) -> int:
        return len(self.WatchList)

    def first_movie_in_watchlist(self):
        if len(self.WatchList) > 0:
            return self.WatchList[0]
        else:
            return None

    def __iter__(self):
        self.n = -1
        return self

    def __next__(self):
        if self.n < len(self.WatchList) - 1:
            self.n += 1
            return self.WatchList[self.n]
        else:
            raise StopIteration


class ModelException(Exception):
    pass


def make_genre_association(movie: Movie, genre: Genre):
    if genre.is_applied_to(movie):
        raise ModelException(f'Genre {genre.genre_name} already applied to Article "{movie.title}"')

    movie.add_genre(genre)
    genre.add_movie(movie)


def make_review(review_text: str, rating: int, movie: Movie, user: User, timestamp: datetime = datetime.today()):
    review = Review(movie, user, review_text, rating, timestamp)
    user.add_review(review)
    movie.add_review(review)

    return review


def make_actor_association(movie: Movie, actor: Actor):
    if actor.is_applied_to(movie):
        raise ModelException(f'Genre {actor.actor_full_name} already applied to Article "{movie.title}"')
    for other_actor in movie.actors:
        other_actor.add_actor_colleague(actor)

    movie.add_actor(actor)
    actor.add_movie(movie)
