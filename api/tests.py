from random import choices
from string import ascii_letters
from typing import Dict, Optional

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APITestCase

from emphasoft.settings import ADMIN_USERNAME, ADMIN_PASSWORD


class UserTests(APITestCase):

    auth_token = None

    def get_auth_token(self) -> str:
        response = self.client.post(
            path=reverse('obtain_auth_token'),
            data=dict(
                username=ADMIN_USERNAME,
                password=ADMIN_PASSWORD
            )
        )
        self.assertEqual(response.status_code, 200)
        return response.json()['token']

    def authenticated_request(
            self,
            method: str,
            path: str,
            token: Optional[str] = None,
            data: Optional[Dict] = None
    ) -> Response:
        function = getattr(self.client, method)
        kwargs = dict(
            path=path,
            HTTP_AUTHORIZATION=f"Token {token or self.auth_token}",
            data=data
        )

        return function(**kwargs)

    def get_user_details(self, user_id: int) -> Response:
        return self.authenticated_request('get', path=reverse('user-detail', args=[user_id]))

    def setUp(self) -> None:
        self.auth_token = self.get_auth_token()

    def test_auth(self):
        assert isinstance(self.auth_token, str)

    def test_token_auth_without_token(self) -> None:
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()['detail'], 'Учетные данные не были предоставлены.')

    def test_token_auth_with_invalid_token(self) -> None:
        response = self.authenticated_request(method='get', path=reverse('user-list'), token="InvalidToken")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()['detail'], 'Недопустимый токен.')

    def test_user_listing(self) -> None:
        response = self.authenticated_request(method='get', path=reverse('user-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [x['id'] for x in response.json()],
            [x.id for x in User.objects.all()]
        )

    def test_user_creation(self):
        new_user_name = 'NewUser'
        response = self.authenticated_request(method='post', path=reverse('user-list'), data=dict(username=new_user_name))
        self.assertEqual(response.status_code, 201)
        new_user_id = response.json()['id']
        user = User.objects.get(id=new_user_id)
        self.assertEqual(user.username, new_user_name)

    def test_user_details(self):
        response = self.get_user_details(user_id=1)
        self.assertEqual(
            [x for x in response.json().keys()],
            ['id', 'username', 'first_name', 'last_name', 'is_active', 'last_login', 'is_superuser']
        )

    def test_full_user_update(self):
        new_first_name = ''.join(choices(ascii_letters, k=10))
        new_last_name = ''.join(choices(ascii_letters, k=10))
        response = self.get_user_details(user_id=1)

        data = {k: v if v is not None else '' for k,v in response.json().items()}
        self.assertNotEqual(data['first_name'], new_first_name)
        self.assertNotEqual(data['last_name'], new_last_name)
        data['first_name'] = new_first_name
        data['last_name'] = new_last_name

        response = self.authenticated_request(method='put', path=reverse('user-detail', args=[1]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['first_name'], new_first_name)
        self.assertEqual(response.json()['last_name'], new_last_name)

    def test_partial_user_update(self):
        new_first_name = ''.join(choices(ascii_letters, k=10))
        response = self.get_user_details(user_id=1)
        self.assertNotEqual(response.json()['first_name'], new_first_name)

        response = self.authenticated_request(
            method='patch',
            path=reverse('user-detail', args=[1]),
            data=dict(first_name=new_first_name)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['first_name'], new_first_name)

    def test_user_deletion(self):
        response = self.authenticated_request(method='post', path=reverse('user-list'), data=dict(username='NewUser'))
        new_user_id = response.json()['id']
        self.assertEqual(self.get_user_details(new_user_id).status_code, 200)

        response = self.authenticated_request('delete', path=reverse('user-detail', args=[new_user_id]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.get_user_details(new_user_id).status_code, 404)
