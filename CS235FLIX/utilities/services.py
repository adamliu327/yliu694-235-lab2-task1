from typing import Iterable
import random

from CS235FLIX.adapters.repository import AbstractRepository
from CS235FLIX.domain.model import Movie


def get_genre_names(repo: AbstractRepository):
    genres = repo.get_genres()
    genre_names = [genre.genre_name for genre in genres]

    return genre_names


def get_actor_names(repo: AbstractRepository):
    actors = repo.get_actors()
    actor_names = [actor.actor_full_name for actor in actors]

    return actor_names

def get_random_movies(quantity, repo: AbstractRepository):
    movie_count = repo.get_number_of_movies()

    if quantity >= movie_count:
        # Reduce the quantity of ids to generate if the repository has an insufficient number of articles.
        quantity = movie_count - 1

    # Pick distinct and random articles.
    random_ids = random.sample(range(1, movie_count), quantity)
    movies = repo.get_movies_by_id(random_ids)

    return movies_to_dict(movies)


# ============================================
# Functions to convert dicts to model entities
# ============================================

def movie_to_dict(movie: Movie):
    movie_dict = {
        'date': movie.release_year,
        'title': movie.title,
        'image_hyperlink': movie.image_hyperlink,
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]
