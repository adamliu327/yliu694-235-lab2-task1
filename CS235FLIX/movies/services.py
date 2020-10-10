from typing import List, Iterable

from CS235FLIX.adapters.repository import AbstractRepository
from CS235FLIX.domain.model import Movie, Genre, Review, Actor, make_review


class NonExistentMovieException(Exception):
    pass

class NonExistentActorException(Exception):
    pass

class UnknownUserException(Exception):
    pass


def get_movie_ids_for_genre(tag_name, repo: AbstractRepository):
    movie_ids = repo.get_movie_ids_for_genre(tag_name)

    return movie_ids


def get_movies_by_id(id_list, repo: AbstractRepository):
    movies = repo.get_movies_by_id(id_list)
    movies_as_dict = movies_to_dict(movies)
    return movies_as_dict


def get_movie(movie_id: int, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)

    if movie is None:
        raise NonExistentMovieException

    return movie_to_dict(movie)


def get_actor(actor_name: str, repo: AbstractRepository):
    actor = repo.get_actor(actor_name)

    if actor is None:
        raise NonExistentActorException

    return actor_to_dict(actor)


def get_first_movie(repo: AbstractRepository):

    movie = repo.get_first_movie()

    return movie_to_dict(movie)


def get_last_movie(repo: AbstractRepository):

    movie = repo.get_last_movie()
    return movie_to_dict(movie)


def get_movies_by_date(date, repo: AbstractRepository):
    # Returns movies for the target date (empty if no matches), the date of the previous article (might be null),
    # the date of the next article (might be null)

    movies = repo.get_movies_by_date(target_date=date)

    movies_dto = list()
    prev_date = next_date = None

    if len(movies) > 0:
        prev_date = repo.get_date_of_previous_movie(movies[0])
        next_date = repo.get_date_of_next_movie(movies[0])

        # Convert Articles to dictionary form.
        movies_dto = movies_to_dict(movies)

    return movies_dto, prev_date, next_date


def add_review(movie_id: int, review_text: str, rating: int, username: str, repo: AbstractRepository):
    # Check that the article exists.
    movie = repo.get_movie(movie_id)
    if movie is None:
        raise NonExistentMovieException

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    # Create comment.
    review = make_review(
        review_text=review_text,
        rating=int(rating),
        movie=movie,
        user=user)

    # Update the repository.
    repo.add_review(review)


def get_reviews_for_movie(movie_id, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)

    if movie is None:
        raise NonExistentMovieException

    return reviews_to_dict(movie.reviews)

# ============================================
# Functions to convert model entities to dicts
# ============================================


def movie_to_dict(movie: Movie):
    movie_dict = {
        'id': movie.movie_id,
        'date': movie.release_year,
        'title': movie.title,
        'description': movie.description,
        'hyperlink': movie.hyperlink,
        'image_hyperlink': movie.image_hyperlink,
        'actors': actors_to_dict(movie.actors),
        'reviews': reviews_to_dict(movie.reviews),
        'genres': genres_to_dict(movie.genres)
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def genre_to_dict(genre: Genre):
    genre_dict = {
        'name': genre.genre_name,
        'movie_with_genre': [movie.movie_id for movie in genre.movie_with_genre]
    }
    return genre_dict


def genres_to_dict(genres: Iterable[Genre]):
    return [genre_to_dict(genre) for genre in genres]


def review_to_dict(review: Review):
    comment_dict = {
        'username': review.user.user_name,
        'movie_id': review.movie.movie_id,
        'rating': review.rating,
        'review_text': review.review_text,
        'timestamp': review.timestamp
    }
    return comment_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]


def actor_to_dict(actor: Actor):
    actor_dict = {
        'full_name': actor.actor_full_name,
        'acted_movies': [movie.movie_id for movie in actor.acted_movies],
        'description': actor.description,
        'hyperlink': actor.hyperlink,
        'image_hyperlink': actor.image_hyperlink,
        'colleagues': actor.actors_this_one_has_worked_with
    }
    return actor_dict


def actors_to_dict(actors: Iterable[Actor]):
    return [actor_to_dict(actor) for actor in actors]