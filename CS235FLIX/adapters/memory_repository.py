import csv
import os
from abc import ABC
from werkzeug.security import generate_password_hash
from datetime import date, datetime
from typing import List
from bisect import bisect, bisect_left, insort_left

from CS235FLIX.adapters.repository import AbstractRepository, RepositoryException
from CS235FLIX.domain.model import Movie, User, Actor, Genre, Review, Director, make_genre_association, make_review, make_actor_association


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self._movies = list()
        self._movies_index = dict()
        self._genres = list()
        self._actors = list()
        self._users = list()
        self._reviews = list()
        self._directors = list()

    def add_movie(self, movie: Movie):
        self._movies.append(movie)
        self._movies_index[movie.movie_id] = movie

    def add_genre(self, genre: Genre):
        self._genres.append(genre)

    def add_user(self, user: User):
        self._users.append(user)

    def add_actor(self, actor: Actor):
        self._actors.append(actor)

    def add_director(self, director: Director):
        self._directors.append(director)

    def add_review(self, review: Review):
        super().add_review(review)
        self._reviews.append(review)

    def get_movie(self, id: int) -> Movie:
        return next((movie for movie in self._movies if movie.movie_id == id), None)

    def get_movies(self) -> list:
        return self._movies

    def get_genres(self) -> list:
        return self._genres

    def get_user(self, username: str) -> User:
        return next((user for user in self._users if user.user_name == username), None)

    def get_actor(self, actor_name) -> User:
        return next((actor for actor in self._actors if actor.actor_full_name == actor_name), None)

    def get_reviews(self):
        return self._reviews

    def get_actors(self):
        return self._actors

    def get_number_of_movies(self):
        return len(self._movies)

    def get_director(self, director_full_name: str) -> Director:
        return next((director for director in self._directors if director.director_full_name == director_full_name), None)

    def get_movies_by_date(self, target_date: int) -> List[Movie]:
        target_movie = Movie(movie_id=None, title="None", release_year=target_date, description="None", hyperlink="None",
                             image_hyperlink="None")
        matching_movies = list()

        try:
            for movie in self._movies:
                if int(movie.release_year) == target_date:
                    matching_movies.append(movie)
                else:
                    continue
        except ValueError:
            # No articles for specified date. Simply return an empty list.
            pass

        return matching_movies

    def get_date_of_previous_movie(self, movie: Movie):
        previous_date = None

        try:
            index = self.movie_index(movie)
            for stored_movie in reversed(self._movies[0:index]):
                if stored_movie.release_year < movie.release_year:
                    previous_date = stored_movie.release_year
                    break
        except ValueError:
            # No earlier articles, so return None.
            pass

        return previous_date

    def get_date_of_next_movie(self, movie: Movie):
        next_date = None

        try:
            index = self.movie_index(movie)
            for stored_movie in self._movies[index + 1:len(self._movies)]:
                if stored_movie.release_year > movie.release_year:
                    next_date = stored_movie.release_year
                    break
        except ValueError:
            # No subsequent articles, so return None.
            pass

        return next_date

    def get_first_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movies[0]
        return movie

    def get_last_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movies[-1]
        return movie

    def get_movie_ids_for_genre(self, genre_name: str):
        # Linear search, to find the first occurrence of a Tag with the name tag_name.
        genre = next((genre for genre in self._genres if genre.genre_name == genre_name), None)

        # Retrieve the ids of articles associated with the Tag.
        if genre is not None:
            movie_ids = [movie.movie_id for movie in genre.movie_with_genre]
        else:
            # No Tag with name tag_name, so return an empty list.
            movie_ids = list()

        return movie_ids

    def get_movies_by_id(self, id_list):
        # Strip out any ids in id_list that don't represent Movie ids in the repository.
        existing_ids = [id for id in id_list if id in self._movies_index]

        # Fetch the Movies.
        movies = [self._movies_index[id] for id in existing_ids]
        return movies

    def movie_index(self, movie: Movie):
        index = self._movies.index(movie)
        if index != len(self._movies) and self._movies[index].release_year == movie.release_year:
            return index
        raise ValueError


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_movies_and_genres(data_path: str, repo: MemoryRepository):
    genres = dict()

    for data_row in read_csv_file(os.path.join(data_path, "movies.csv")):

        movie_id = int(data_row[0])
        number_of_genres = len(data_row) - 6
        movie_genres = data_row[-number_of_genres:]

        for genre in movie_genres:
            if genre not in genres:
                genres[genre] = list()
            genres[genre].append(movie_id)
        del data_row[-number_of_genres:]

        movie = Movie(movie_id=movie_id, title=data_row[1], release_year=int(data_row[2]), description=data_row[3],
                      hyperlink=data_row[4], image_hyperlink=data_row[5])

        repo.add_movie(movie)

    # Create Genre objects, associate them with Movies and add them to the repository.
    for genre_name in genres.keys():
        genre = Genre(genre_name)
        for movie_id in genres[genre_name]:
            movie = repo.get_movie(movie_id)
            make_genre_association(movie, genre)
        repo.add_genre(genre)


def load_users(data_path: str, repo: MemoryRepository):
    users = dict()

    for data_row in read_csv_file(os.path.join(data_path, 'users.csv')):
        user = User(
            user_name=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def load_reviews(data_path: str, repo: MemoryRepository, users):
    for data_row in read_csv_file(os.path.join(data_path, 'comments.csv')):
        review = make_review(
            review_text=data_row[4],
            rating=int(data_row[3]),
            user=users[data_row[1]],
            movie=repo.get_movie(int(data_row[2])),
            timestamp=datetime.fromisoformat(data_row[5])
        )
        repo.add_review(review)


def load_actors(data_path: str, repo: MemoryRepository):
    actors = dict()

    for data_row in read_csv_file(os.path.join(data_path, 'actors.csv')):
        number_of_movies = len(data_row) - 5
        acted_movies = data_row[-number_of_movies:]

        actor = Actor(
            actor_full_name=data_row[1],
            description=data_row[2],
            hyperlink=data_row[3],
            image_hyperlink=data_row[4]
        )
        for movie_id in acted_movies:
            movie = repo.get_movie(int(movie_id))
            make_actor_association(movie, actor)
        repo.add_actor(actor)


def populate(data_path: str, repo: MemoryRepository):
    # Load articles and tags into the repository.
    load_movies_and_genres(data_path, repo)

    # Load users into the repository.
    users = load_users(data_path, repo)

    # Load comments into the repository.
    load_reviews(data_path, repo, users)

    # Load actors into the repository
    load_actors(data_path, repo)
