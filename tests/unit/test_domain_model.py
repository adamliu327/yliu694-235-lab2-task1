from datetime import date

from CS235FLIX.domain.model import User, Movie, Genre, make_review, make_genre_association, ModelException

import pytest

@pytest.fixture()
def movie():
    return Movie(
        movie_id=1,
        title='The Godfather',
        release_year=1972,
        description='The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
        hyperlink='https://www.imdb.com/title/tt0068646/',
        image_hyperlink='https://i.loli.net/2020/10/10/Y79y2iUj5qGsrHz.png'
    )


@pytest.fixture()
def user():
    return User('dbowie', '1234567890')


@pytest.fixture()
def genre():
    return Genre('Genre 1')


def test_user_construction(user):
    assert user.user_name == 'dbowie'
    assert user.password == '1234567890'
    assert repr(user) == '<User dbowie>'

    for review in user.reviews:
        # User should have an empty list of Reviews after construction.
        assert False


def test_movie_construction(movie):
    assert movie.movie_id is 1
    assert movie.release_year == 1972
    assert movie.title == 'The Godfather'
    assert movie.description == 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.'
    assert movie.hyperlink == 'https://www.imdb.com/title/tt0068646/'
    assert movie.image_hyperlink == 'https://i.loli.net/2020/10/10/Y79y2iUj5qGsrHz.png'

    assert len(list(movie.reviews)) == 0
    assert len(movie.genres) == 0

    assert repr(
        movie) == '<Movie The Godfather, 1972>'


def test_movie_less_than_operator():
    movie_1 = Movie(
        "None", 1998, "None", "None", "None", None
    )

    movie_2 = Movie(
        "None", 2020, "None", "None", "None", None
    )

    assert movie_1 < movie_2


def test_genre_construction(genre):
    assert genre.genre_name == 'Genre 1'

    for movie in genre.movie_with_genre:
        assert False

    assert not genre.is_applied_to(Movie("None", 2020, "None", "None", "None", None))


def test_make_review_establishes_relationships(movie, user):
    review_text = 'Goooooooooood'
    rating = 9
    review = make_review(review_text, rating, movie, user)

    # Check that the User object knows about the Review.
    assert review in user.reviews

    # Check that the Review knows about the User.
    assert review.user is user

    # Check that Article knows about the Review.
    assert review in movie.reviews

    # Check that the Review knows about the Movie.
    assert review.movie is movie


def test_make_tag_associations(movie, genre):
    make_genre_association(movie, genre)

    # Check that the Article knows about the Tag.
    assert movie.is_tagged()
    assert movie.is_tagged_by(genre)

    # check that the Tag knows about the Article.
    assert genre.is_applied_to(movie)
    assert movie in genre.movie_with_genre


def test_make_tag_associations_with_movie_already_tagged(movie, genre):
    make_genre_association(movie, genre)

    with pytest.raises(ModelException):
        make_genre_association(movie, genre)