import abc
from typing import List

from CS235FLIX.domain.model import Director, Actor, Genre, Movie, Review, User

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        """ Adds a Movie to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        """ Adds a Genre to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        """ Adds an User to the repository. """
        return NotImplementedError

    @abc.abstractmethod
    def add_actor(self, actor: Actor):
        """ Adds a Actor to the repository. """
        return NotImplementedError

    @abc.abstractmethod
    def add_director(self, director: Director):
        """ Adds a Director to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a Review to the repository.

        If the Review doesn't have bidirectional links with a Movie and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Comment not correctly attached to a User')
        if review.movie is None or review not in review.movie.reviews:
            raise RepositoryException('Comment not correctly attached to an Movie')

    @abc.abstractmethod
    def get_movies(self) -> list:
        """ Returns the Movies stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, title: str) -> Movie:
        """ Returns Movie with name from the repository.

        If there is no Movie with the given name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_movies(self) -> int:
        """ Returns the number of Movies in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_director(self, director_full_name: str) -> Director:
        """ Returns the Director named director_full_name from the repository.

        If there is no Director with the given director_full_name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> list:
        """ Returns the Genres stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username: str) -> User:
        """ Returns the User named username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_actor(self, actor_name) -> User:
        """ Returns the Actor named actor_name from the repository.

        If there is no Actor with the given actor_name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews(self):
        """ Returns the Reviews stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_actors(self):
        """ Returns the Actors stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_date(self, target_date: int) -> List[Movie]:
        """ Returns a list of Movies that were released on target_date.

        If there are no Movies on the given date, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_date_of_previous_movie(self, movie: Movie):
        """ Returns the release_year of an Movie that immediately precedes movie.

        If movie is the first Movie in the repository, this method returns None because there are no Movies
        on a previous year.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_date_of_next_movie(self, movie: Movie):
        """ Returns the release_year of an Movie that immediately follows movie.

        If movie is the lase Movie in the repository, this method returns None because there are no Movies
        on a later year.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_movie(self):
        """ Returns the first Movie, ordered by release_year, from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_movie(self):
        """ Returns the last Movie, ordered by release_year, from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ids_for_genre(self, genre_name: str):
        """ Returns a list of ids representing Movies that are tagged by genre_name.

        If there are Movie that are tagged by genre_name, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_id(self, id_list):
        """ Returns a list of Movies, whose ids match those in id_list, from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError
