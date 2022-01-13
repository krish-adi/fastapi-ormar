import json

from fastapi import status
from fastapi.testclient import TestClient
import pytest

from .models import Book


@pytest.mark.asyncio
async def test_api_can_add_book(client: TestClient, db):
    books = await db(Book.objects.all())
    books_count = len(books)
    with client as client:
        post_data = {
            "title": "example book",
            "description": "example description",
            "price": 50,
        }
        url = "/add"
        response = client.post(url, json=post_data)
        response_data = json.loads(response.text)
        print(response_data)
        assert response_data["id"] is not None
        assert response_data["title"] == post_data["title"]
        assert response_data["description"] == post_data["description"]
        assert response_data["price"] == post_data["price"]
    books = await db(Book.objects.all())
    assert books_count + 1 == len(books)


@pytest.mark.asyncio
async def test_api_can_fetch_books(client: TestClient):
    with client as client:
        url = "/"
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
