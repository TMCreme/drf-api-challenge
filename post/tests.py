"""
TestCases for APIs in Post
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

# from .models import Post

POST_URL = reverse("post:post-list")


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PostAPITests(TestCase):
    """Test cases for APIs"""

    def setUp(self) -> None:
        self.client = APIClient()
        payload = {
            "first_name": "AuthorSupreme",
            "email": "test123@email.com",
            "password": "supersecret142"
        }
        user = create_user(**payload)
        self.client.force_authenticate(user)

    def test_post_success(self):
        """Creating a post with success"""
        post_payload = {
            "title": "Awesome Blog Post",
            "body": "Posting is such an easy task but writing"
        }

        res = self.client.post(
            POST_URL,
            post_payload
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # get all
        response = self.client.get(
            POST_URL
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn("title", response.data[0])
        self.assertEqual(res.data, response.data[0])

    def test_patch_request(self):
        """Test an update"""
        post_payload = {
            "title": "Awesome Blog Post",
            "body": "Posting is such an easy task but writing"
        }
        update_payload = {
            "title": "Edited Awesome Blog"
        }
        res = self.client.post(
            POST_URL,
            post_payload
        )
        self.assertIn("id", res.data)

        update_res = self.client.patch(
            "/api/post/post/{}/".format(res.data["id"]),
            update_payload
        )
        self.assertEqual(update_res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            update_res.data["title"],
            update_payload["title"]
        )

    def test_put_update(self):
        """Testing method not allowed"""
        post_payload = {
            "title": "Awesome Blog Post",
            "body": "Posting is such an easy task but writing"
        }
        update_payload = {
            "title": "Edited Awesome Blog"
        }
        res = self.client.post(
            POST_URL,
            post_payload
        )
        self.assertIn("id", res.data)

        update_res = self.client.put(
            "/api/post/post/{}/".format(res.data["id"]),
            update_payload
        )
        self.assertEqual(
            update_res.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_delete_method(self):
        """Testing deleting a model"""
        post_payload = {
            "title": "Awesome Blog Post",
            "body": "Posting is such an easy task but writing"
        }
        res = self.client.post(
            POST_URL,
            post_payload
        )
        self.assertIn("id", res.data)

        delete_res = self.client.delete(
            "/api/post/post/{}/".format(res.data["id"])
        )
        self.assertEqual(
            delete_res.status_code,
            status.HTTP_204_NO_CONTENT
        )


class UnauthorizedTests(TestCase):
    """Testing all unauthorized APIs"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_post(self):
        """Creating a post with unauthorized user"""
        payload = {
            "title": "Awesome Blog Post",
            "body": "Posting is such an easy task but writing"
        }
        res = self.client.post(
            POST_URL,
            payload
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_with_put(self):
        """Update a post with unauthenticated user"""

        update_payload = {
            "title": "Edited Awesome Blog"
        }
        update_res = self.client.put(
            "/api/post/post/1/",
            update_payload
        )
        self.assertEqual(update_res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_with_patch(self):
        """Update a post with unauthenticated user"""

        update_payload = {
            "title": "Edited Awesome Blog"
        }
        update_res = self.client.patch(
            "/api/post/post/1/",
            update_payload
        )
        self.assertEqual(update_res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_post(self):
        """Update a post with unauthenticated user"""

        update_res = self.client.delete(
            "/api/post/post/1/"
        )
        self.assertEqual(update_res.status_code, status.HTTP_401_UNAUTHORIZED)


# Create your tests here.
