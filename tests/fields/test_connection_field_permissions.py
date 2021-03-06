import pytest
from graphql_relay import to_global_id
from rest_framework.utils import json


@pytest.mark.django_db()
def test_connection_field_permission_classes_without_authentication(
    book_factory, graphql_client
):
    book_factory()

    response = graphql_client.execute(
        """
        query BooksAsAdmin {
            booksAsAdmin {
              totalCount
              edges {
                node {
                  id
                }
              }
            }
        }""",
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"booksAsAdmin": None},
        "errors": [
            {
                "locations": [{"column": 13, "line": 3}],
                "message": "You do not have permission to perform this action.",
                "path": ["booksAsAdmin"],
            }
        ],
    }


@pytest.mark.django_db()
def test_connection_field_permission_classes_without_permission(
    user_factory, book_factory, graphql_client
):
    user = user_factory()
    book_factory()
    graphql_client.force_authenticate(user)

    response = graphql_client.execute(
        """
        query BooksAsAdmin {
            booksAsAdmin {
              totalCount
              edges {
                node {
                  id
                }
              }
            }
        }""",
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"booksAsAdmin": None},
        "errors": [
            {
                "locations": [{"column": 13, "line": 3}],
                "message": "You do not have permission to perform this action.",
                "path": ["booksAsAdmin"],
            }
        ],
    }


@pytest.mark.django_db()
def test_connection_field_permission_classes_with_permission(
    user_factory, book_factory, graphql_client
):
    user = user_factory(is_staff=True)
    book = book_factory()

    graphql_client.force_authenticate(user)

    response = graphql_client.execute(
        """
        query BooksAsAdmin {
            booksAsAdmin {
              totalCount
              edges {
                node {
                  id
                }
              }
            }
        }""",
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {
            "booksAsAdmin": {
                "edges": [{"node": {"id": to_global_id("BookType", book.pk)}}],
                "totalCount": 1,
            }
        }
    }
