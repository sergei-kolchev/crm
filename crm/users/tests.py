from http import HTTPStatus
from unittest.mock import Mock

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized
from users.models import User
from users.validators import (ImageMaxDimValidator, ImageMinDimValidator,
                              ImageSizeValidator)


class UsersLoginTestCase(TestCase):
    fixtures = [
        "users_user.json",
    ]
    _user = {
        "username": "test",
        "password": "Test12345678",
    }

    def test_login_user_ok(self):
        response = self.client.post(reverse("users:login"), self._user)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("patients:index"))
        self.assertTemplateUsed("users/login.html")

    def test_login_user_error(self):
        response = self.client.post(
            reverse("users:login"), {"username": "bad", "password": "bad"}
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(
            response,
            "Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.",
        )

    def test_logout_ok(self):
        response = self.client.post(reverse("users:logout"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTemplateUsed("users/login.html")


class UsersProfileTestCase(TestCase):
    fixtures = [
        "users_user.json",
    ]
    headers = {"HTTP_HX-Request": "true"}

    _user = {
        "username": "test",
        "password": "Test12345678",
    }

    _relay_url = "htmx/relay.html"

    _data = {
        "photo": "",
        "email": "test@mail.com",
        "first_name": "новое имя",
        "last_name": "новая фамилия",
        "date_birth_day": "10",
        "date_birth_month": "10",
        "date_birth_year": "2001",
    }

    def setUp(self):
        response = self.client.post(reverse("users:login"), self._user)
        self.assertRedirects(response, reverse("patients:index"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_get_user_profile_ok(self):
        response = self.client.get(reverse("users:profile"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed("users/profile.html")
        self.assertEqual(
            response.context_data["title"], "Профиль пользователя"
        )
        user = User.objects.get(username="test")
        self.assertEqual(user, response.context_data["user"])

    def test_get_user_profile_not_authorized(self):
        response = self.client.post(reverse("users:logout"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTemplateUsed("users/login.html")
        response = self.client.get(reverse("users:profile"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        redirect_url = reverse("users:login") + "?next=%2Fusers%2Fprofile%2F"
        self.assertRedirects(response, redirect_url)

    def test_user_profile_change_ok(self):
        response = self.client.get(reverse("users:profile"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed("users/profile.html")
        self.assertEqual(
            response.context_data["title"], "Профиль пользователя"
        )

        response = self.client.post(reverse("users:profile"), self._data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed("users/profile.html")
        self.assertEqual(
            response.context_data["form"].cleaned_data["last_name"],
            self._data["last_name"],
        )
        self.assertEqual(
            response.context_data["form"].cleaned_data["first_name"],
            self._data["first_name"],
        )
        self.assertEqual(
            response.context_data["form"].cleaned_data["photo"], None
        )

        user = User.objects.get(username="test")
        self.assertEqual(response.context_data["user"], user)
        self.assertEqual(
            response.context_data["user"].first_name, self._data["first_name"]
        )

    def test_user_profile_change_error(self):
        response = self.client.get(reverse("users:profile"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed("users/profile.html")
        self.assertEqual(
            response.context_data["title"], "Профиль пользователя"
        )
        response = self.client.post(
            reverse("users:profile"), {"first_name": "bad_data"}
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed("users/profile.html")
        self.assertContains(response, "Обязательное поле")

    def test_user_profile_change_password_page_ok(self):
        response = self.client.post(
            reverse("users:password_change"),
            {
                "old_password": self._user["password"],
                "new_password1": "NewPassword123456",
                "new_password2": "NewPassword123456",
            },
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("users:password_change_done"))
        self.assertTemplateUsed("users/password_change_done.html")
        response = self.client.get(reverse("users:password_change_done"))
        self.assertContains(response, "Пароль успешно изменен!")

    def test_user_profile_change_password_page_error(self):
        response = self.client.post(
            reverse("users:password_change"),
            {
                "old_password": self._user["password"],
                "new_password1": "NewPassword12345",
                "new_password2": "NewPassword123456",
            },
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Введенные пароли не совпадают")

    def test_user_profile_change_password_page_not_authorized(self):
        response = self.client.post(reverse("users:logout"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTemplateUsed("users/login.html")
        response = self.client.get(reverse("users:password_change"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        redirect_url = (
            reverse("users:login") + "?next=%2Fusers%2Fpassword-change%2F"
        )
        self.assertRedirects(response, redirect_url)


class ValidatorsTestCase(TestCase):
    @parameterized.expand(
        [
            (ImageMinDimValidator, (300, 300), 300, 300),
            (ImageMaxDimValidator, (600, 600), 600, 600),
        ]
    )
    def test_image_dim_validators_ok(self, validator, dims, width, height):
        img = Mock()
        img.width = width
        img.height = height
        self.assertIsNone(validator(dims)(img))

    @parameterized.expand(
        [
            (ImageMinDimValidator, (300, 300), 299, 299, ValidationError),
            (ImageMinDimValidator, (0.600, 600), 600, 600, ValueError),
            (ImageMinDimValidator, (600, 600, 600), 600, 600, ValueError),
            (ImageMinDimValidator, (600, 600, None), 600, 600, ValueError),
            (ImageMinDimValidator, None, 600, 600, TypeError),
            (ImageMinDimValidator, "", 600, 600, TypeError),
            (ImageMaxDimValidator, (600, 600), 601, 601, ValidationError),
            (ImageMaxDimValidator, (0.600, 600), 600, 600, ValueError),
            (ImageMaxDimValidator, (600, 600, 600), 600, 600, ValueError),
            (ImageMaxDimValidator, (600, 600, None), 600, 600, ValueError),
            (ImageMaxDimValidator, None, 600, 600, TypeError),
            (ImageMaxDimValidator, "", 600, 600, TypeError),
        ]
    )
    def test_image_dim_validators_error(
        self, validator, dims, width, height, exc
    ):
        img = Mock()
        img.width = width
        img.height = height
        with self.assertRaises(exc):
            validator(dims)(img)

    @parameterized.expand(
        [
            (ImageSizeValidator, 300, 300),
            (ImageSizeValidator, 300, 10),
        ]
    )
    def test_image_size_validator_ok(self, validator, size_limit, size):
        img = Mock()
        img.size = size
        self.assertIsNone(validator(size_limit)(img))

    @parameterized.expand(
        [
            (ImageSizeValidator, 300, 301, ValidationError),
            (ImageSizeValidator, 300, 3001, ValidationError),
            (ImageSizeValidator, 0.300, 301, TypeError),
            (ImageSizeValidator, "", 301, TypeError),
            (ImageSizeValidator, None, 301, TypeError),
        ]
    )
    def test_image_size_validator_ok(self, validator, size_limit, size, exc):
        img = Mock()
        img.size = size
        with self.assertRaises(exc):
            validator(size_limit)(img)
