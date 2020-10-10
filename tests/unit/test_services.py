from datetime import date

import pytest

from CS235FLIX.authentication.services import AuthenticationException
from CS235FLIX.movies import services as movies_services
from CS235FLIX.authentication import services as auth_services
from CS235FLIX.movies.services import NonExistentMovieException


def test_can_add_user(in_memory_repo):
    new_username = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    username = 'thorke'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_username, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_username, '0987654321', in_memory_repo)


def test_can_add_comment(in_memory_repo):
    movie_id = 3

    review_text = 'Badbadbadbad'
    rating = 5
    username = 'fmercury'

    # Call the service layer to add the comment.
    movies_services.add_review(movie_id, review_text, rating, username, in_memory_repo)

    # Retrieve the comments for the article from the repository.
    reviews_as_dict = movies_services.get_reviews_for_movie(movie_id, in_memory_repo)

    # Check that the comments include a comment with the new comment text.
    assert next(
        (dictionary['review_text'] for dictionary in reviews_as_dict if dictionary['review_text'] == review_text),
        None) is not None


def test_cannot_add_review_for_non_existent_movie(in_memory_repo):
    movie_id = 100
    review_text = "test_cannot_add_review_for_non_existent_movie"
    rating = 10
    username = 'fmercury'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(movies_services.NonExistentMovieException):
        movies_services.add_review(movie_id, review_text, rating, username, in_memory_repo)


def test_cannot_add_comment_by_unknown_user(in_memory_repo):
    movie_id = 3
    review_text = 'test_cannot_add_comment_by_unknown_user'
    rating = 10
    username = 'gmichael'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(movies_services.UnknownUserException):
        movies_services.add_review(movie_id, review_text, rating, username, in_memory_repo)


def test_can_get_movie(in_memory_repo):
    movie_id = 2

    movie_as_dict = movies_services.get_movie(movie_id, in_memory_repo)

    assert movie_as_dict['id'] == movie_id
    assert movie_as_dict['date'] == 1993
    assert movie_as_dict['title'] == 'Schindler\'s List'
    assert movie_as_dict['description'] == 'In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis.'
    assert movie_as_dict['hyperlink'] == 'https://www.imdb.com/title/tt0108052'
    assert movie_as_dict['image_hyperlink'] == 'https://i.loli.net/2020/10/10/sT4WR7iqFVnQt38.png'
    assert len(movie_as_dict['reviews']) == 0
    assert len(movie_as_dict['actors']) == 0

    genre_names = [dictionary['name'] for dictionary in movie_as_dict['genres']]
    assert 'Genre 1' in genre_names
    assert 'Genre 2' in genre_names


def test_cannot_get_movie_with_non_existent_id(in_memory_repo):
    movie_id = 170

    # Call the service layer to attempt to retrieve the Article.
    with pytest.raises(movies_services.NonExistentMovieException):
        movies_services.get_movie(movie_id, in_memory_repo)


def test_get_first_movie(in_memory_repo):
    movies_as_dict = movies_services.get_first_movie(in_memory_repo)

    assert movies_as_dict['id'] == 1


def test_get_last_movie(in_memory_repo):
    movies_as_dict = movies_services.get_last_movie(in_memory_repo)

    assert movies_as_dict['id'] == 13


def test_get_movies_by_date_with_one_date(in_memory_repo):
    target_date = 1972

    movies_as_dict, prev_date, next_date = movies_services.get_movies_by_date(target_date, in_memory_repo)

    assert len(movies_as_dict) == 1
    assert movies_as_dict[0]['id'] == 1

    assert prev_date is None
    assert next_date == 1993


def test_get_movies_by_date_with_multiple_dates(in_memory_repo):
    target_date = 1994

    movies_as_dict, prev_date, next_date = movies_services.get_movies_by_date(target_date, in_memory_repo)

    # Check that there are 3 articles dated 2020-03-01.
    assert len(movies_as_dict) == 3

    # Check that the article ids for the the articles returned are 3, 4 and 5.
    movie_ids = [movie['id'] for movie in movies_as_dict]
    assert set([3, 4, 5]).issubset(movie_ids)

    # Check that the dates of articles surrounding the target_date are 2020-02-29 and 2020-03-05.
    assert prev_date == 1993
    assert next_date == 1999


def test_get_movies_by_date_with_non_existent_date(in_memory_repo):
    target_date = 3000

    movies_as_dict, prev_date, next_date = movies_services.get_movies_by_date(target_date, in_memory_repo)

    # Check that there are no articles dated 2020-03-06.
    assert len(movies_as_dict) == 0


def test_get_movies_by_id(in_memory_repo):
    target_movie_ids = [12, 13, 14, 15]
    movies_as_dict = movies_services.get_movies_by_id(target_movie_ids, in_memory_repo)

    # Check that 2 articles were returned from the query.
    assert len(movies_as_dict) == 2

    # Check that the article ids returned were 5 and 6.
    movie_ids = [movie['id'] for movie in movies_as_dict]
    assert {12, 13}.issubset(movie_ids)


def test_get_reviews_for_movie(in_memory_repo):
    reviews_as_dict = movies_services.get_reviews_for_movie(1, in_memory_repo)

    # Check that 2 comments were returned for article with id 1.
    assert len(reviews_as_dict) == 4

    # Check that the comments relate to the article whose id is 1.
    movie_ids = [review['movie_id'] for review in reviews_as_dict]
    movie_ids = set(movie_ids)
    assert 1 in movie_ids and len(movie_ids) == 1


def test_get_reviews_for_non_existent_movie(in_memory_repo):
    with pytest.raises(NonExistentMovieException):
        reviews_as_dict = movies_services.get_reviews_for_movie(100, in_memory_repo)


def test_get_reviews_for_movie_without_reviews(in_memory_repo):
    comments_as_dict = movies_services.get_reviews_for_movie(2, in_memory_repo)
    assert len(comments_as_dict) == 0