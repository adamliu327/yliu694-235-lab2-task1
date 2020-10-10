from datetime import date, datetime
from typing import List

import pytest

from CS235FLIX.domain.model import Director, Actor, Genre, Movie, Review, User, make_review
from CS235FLIX.adapters.repository import RepositoryException


def test_repository_can_add_a_user(in_memory_repo):
    user = User(
        user_name='dave',
        password='Bb123456789'
    )
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_movie_count(in_memory_repo):
    number_of_movies = in_memory_repo.get_number_of_movies()

    # Check that the query returned 6 movies.
    assert number_of_movies == 13


def test_repository_can_add_movie(in_memory_repo):
    movie = Movie(
        movie_id=15,
        title='The Godfather',
        release_year=1972,
        description='The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to '
                    'his reluctant son.',
        hyperlink='https://www.imdb.com/title/tt0068646/',
        image_hyperlink='https://i.loli.net/2020/10/10/Y79y2iUj5qGsrHz.png'
    )
    in_memory_repo.add_movie(movie)

    assert in_memory_repo.get_movie(15) is movie


def test_repository_can_retrieve_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1)

    # Check that the Movie has the expected title.
    assert movie.title == "The Godfather"

    genre1 = movie.genres[0]
    genre2 = movie.genres[1]
    # Check that the Movie is tagged as expected.
    assert genre1.is_applied_to(movie) is True
    assert genre2.is_applied_to(movie) is True


def test_repository_does_not_retrieve_a_non_existent_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(101)
    assert movie is None


def test_repository_can_retrieve_movies_by_date(in_memory_repo):
    movies = in_memory_repo.get_movies_by_date(1999)

    # Check that the query returned 3 movies.
    assert len(movies) == 2


def test_repository_does_not_retrieve_an_movie_when_there_are_no_movies_for_a_given_date(in_memory_repo):
    movies = in_memory_repo.get_movies_by_date(3000)
    assert len(movies) == 0


def test_repository_can_retrieve_genres(in_memory_repo):
    genres: List[Genre] = in_memory_repo.get_genres()

    assert len(genres) == 5

    genre_one = [genre for genre in genres if genre.genre_name == 'Genre 1'][0]
    genre_two = [genre for genre in genres if genre.genre_name == 'R'][0]
    genre_three = [genre for genre in genres if genre.genre_name == 'Genre 2'][0]
    genre_four = [genre for genre in genres if genre.genre_name == 'Genre 3'][0]
    genre_five = [genre for genre in genres if genre.genre_name == 'Movie with actors[test]'][0]

    assert genre_one.number_of_tagged_movies == 7
    assert genre_two.number_of_tagged_movies == 8
    assert genre_three.number_of_tagged_movies == 3
    assert genre_four.number_of_tagged_movies == 2
    assert genre_five.number_of_tagged_movies == 4


def test_repository_can_get_first_movie(in_memory_repo):
    movie = in_memory_repo.get_first_movie()
    assert movie.title == 'The Godfather'


def test_repository_can_get_last_movie(in_memory_repo):
    movie = in_memory_repo.get_last_movie()
    assert movie.title == 'Dolittle'

def test_repository_can_get_movies_by_ids(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([2, 5, 9])

    assert len(movies) == 3
    assert movies[0].title == 'Schindler\'s List'
    assert movies[1].title == 'The Shawshank Redemption'
    assert movies[2].title == 'Captain America: Civil War'


def test_repository_does_not_retrieve_movie_for_non_existent_id(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([0, 9])

    assert len(movies) == 1
    assert movies[0].title == 'Captain America: Civil War'


def test_repository_returns_an_empty_list_for_non_existent_ids(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([0, 100])

    assert len(movies) == 0


def test_repository_returns_movie_ids_for_existing_genre(in_memory_repo):
    movie_ids = in_memory_repo.get_movie_ids_for_genre('Movie with actors[test]')

    assert movie_ids == [9, 10, 11, 13]


def test_repository_returns_an_empty_list_for_non_existent_genre(in_memory_repo):
    movie_ids = in_memory_repo.get_movie_ids_for_genre('United States')

    assert len(movie_ids) == 0


def test_repository_returns_date_of_previous_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(6)
    previous_date = in_memory_repo.get_date_of_previous_movie(movie)

    assert previous_date == 1994


def test_repository_returns_none_when_there_are_no_previous_movies(in_memory_repo):
    movie = in_memory_repo.get_movie(1)
    previous_date = in_memory_repo.get_date_of_previous_movie(movie)

    assert previous_date is None


def test_repository_returns_date_of_next_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(5)
    next_date = in_memory_repo.get_date_of_next_movie(movie)

    assert next_date == 1999


def test_repository_returns_none_when_there_are_no_subsequent_movies(in_memory_repo):
    movie = in_memory_repo.get_movie(13)
    next_date = in_memory_repo.get_date_of_next_movie(movie)

    assert next_date is None


def test_repository_can_add_a_genre(in_memory_repo):
    genre = Genre('Motoring')
    in_memory_repo.add_genre(genre)

    assert genre in in_memory_repo.get_genres()


def test_repository_can_add_a_comment(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movie(2)
    comment = make_review("Good movie", 10, movie, user)

    in_memory_repo.add_review(comment)

    assert comment in in_memory_repo.get_reviews()


def test_repository_does_not_add_a_review_without_a_user(in_memory_repo):
    movie = in_memory_repo.get_movie(2)
    review = Review(movie, None, "Good!!!", 10, datetime.today())

    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)


def test_repository_does_not_add_a_comment_without_a_movie_properly_attached(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movie(2)
    review = Review(movie, None, "Trump's onto it!", 10, datetime.today())

    user.add_review(review)

    with pytest.raises(RepositoryException):
        # Exception expected because the Movie doesn't refer to the Comment.
        in_memory_repo.add_review(review)


def test_repository_can_retrieve_comments(in_memory_repo):
    assert len(in_memory_repo.get_reviews()) == 4


# TODO
# actor相关 * 2
# director相关 * 2
