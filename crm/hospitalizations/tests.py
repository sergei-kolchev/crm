import zoneinfo
from datetime import datetime
from http import HTTPStatus
from unittest.mock import Mock, patch

import file_downloader
from django import forms as django_forms
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from hospitalizations import forms
from hospitalizations.models import Hospitalization
from hospitalizations.utils import (check_dates_intersection,
                                    validate_hospitalization_fields)
from parameterized import parameterized
from patients.models import Patient


class AuthorizedUserTestCase(TestCase):
    fixtures = [
        "patients_patient.json",
        "users_user.json",
        "hospitalizations_hospitalization.json",
    ]

    _user = {
        "username": "test",
        "password": "Test123456",
    }

    def setUp(self):
        self.client.post(reverse("users:login"), self._user)


class HospitalizationViewTests(AuthorizedUserTestCase):
    """Тесты для представлений"""

    _hospitalization = {
        "entry_date": "2024-01-04T17:27:59Z",
        "leaving_date": "",
        "notes": "",
        "time_create": "2024-01-07T17:28:14.098Z",
        "time_update": "2024-01-07T17:28:14.098Z",
        "patient": 1,
        "doctor": 3,
    }

    @parameterized.expand(
        [
            (
                "hospitalizations:hospitalizations",
                {"pk": 4},
                ("19 декабря 2023 г. 9:40", "19 декабря 2023 г. 9:40"),
            ),
            (
                "hospitalizations:hospitalizations",
                {"order": "surname", "direction": "asc", "pk": 4},
                ("19 декабря 2023 г. 9:40", "19 декабря 2023 г. 9:40"),
            ),
            (
                "hospitalizations:hospitalizations",
                {"order": "entry_date", "direction": "desc", "pk": 4},
                ("19 декабря 2023 г. 9:40", "19 декабря 2023 г. 9:40"),
            ),
            (
                "hospitalizations:hospitalizations",
                {"pk": 4},
                ("19 декабря 2023 г. 9:40", "19 декабря 2023 г. 9:40"),
            ),
            (
                "hospitalizations:hospitalizations",
                {"order": "surname", "direction": "asc", "pk": 4},
                (
                    "19 декабря 2023 г. 9:40",
                    "19 декабря 2023 г. 9:40",
                    "2 января 2024 г.",
                    "находится на лечении",
                ),
            ),
            (
                "hospitalizations:hospitalizations",
                {"order": "entry_date", "direction": "desc", "pk": 4},
                (
                    "19 декабря 2023 г. 9:40",
                    "19 декабря 2023 г. 9:40",
                    "2 января 2024 г.",
                    "находится на лечении",
                ),
            ),
        ]
    )
    def test_hospitalizations_list_view_ok(self, viewname, kwargs, data):
        """Тест вывода списка всех госпитализаций"""
        path = reverse(viewname, kwargs=kwargs)
        response = self.client.get(path)
        content = response.content.decode()
        for d in data:
            self.assertIn(d, content)

    @parameterized.expand(
        [
            (
                "hospitalizations:current",
                None,
                None,
                ("Иванов Николай Павлович", "Иванов Михаил Сидорович"),
            ),
            (
                "hospitalizations:current",
                {"order": "surname", "direction": "asc"},
                None,
                ("Иванов Николай Павлович", "Иванов Михаил Сидорович"),
            ),
            (
                "hospitalizations:current",
                {"order": "entry_date", "direction": "desc"},
                None,
                ("Иванов Николай Павлович", "Иванов Михаил Сидорович"),
            ),
            ("hospitalizations:current", None, 3, ("Иванов Михаил Сидорович")),
            (
                "hospitalizations:current",
                {"order": "surname", "direction": "asc"},
                3,
                ("Иванов Михаил Сидорович", "Елкин Сергей Петрович"),
            ),
            (
                "hospitalizations:current",
                {"order": "entry_date", "direction": "desc"},
                3,
                ("Иванов Михаил Сидорович", "Елкин Сергей Петрович"),
            ),
        ]
    )
    def test_current_hospitalizations_list_view_ok(
        self, viewname, kwargs, doctor, data
    ):
        """Тест вывода списка всех госпитализаций"""
        path = reverse(viewname, kwargs=kwargs)
        if doctor:
            path = path + "?selected_doctor=" + str(doctor)
        response = self.client.get(path)
        content = response.content.decode()
        for d in data:
            self.assertIn(d, content)

    def test_add_hospitalizations_ok(self):
        """Тест удачного добавления госпитализации"""
        response = self.client.post(
            reverse("hospitalizations:create"), self._hospitalization
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.get(reverse("hospitalizations:current"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        content = response.content.decode()
        self.assertIn("4 января 2024 г. 17:27", content)
        self.assertIn("Иванов Иван Иванович", content)

    def test_add_hospitalizations_error(self):
        """Тест ошибки при добавлении госпитализации"""
        self.client.post(
            reverse("hospitalizations:create"), self._hospitalization
        )
        response = self.client.post(
            reverse("hospitalizations:create"), self._hospitalization
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        content = response.content.decode()
        self.assertIn("Для пациента уже существует госпитализация ", content)

    def test_update_hospitalization_ok(self):
        """Тест успешного обновления госпитализации"""
        hosp = self._hospitalization.copy()
        hosp["notes"] = "test"
        response = self.client.post(
            reverse("hospitalizations:update", kwargs={"pk": 4}),
            hosp,
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.get(reverse("hospitalizations:current"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        content = response.content.decode()
        self.assertIn("4 января 2024 г.", content)
        self.assertIn("test", content)

    def test_update_hospitalization_error(self):
        """Тест ошибки при обновлении госпитализации"""
        hosp = self._hospitalization.copy()
        hosp["entry_date"] = ""
        path = reverse("hospitalizations:update_current", kwargs={"pk": 4})
        response = self.client.post(path, hosp)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        content = response.content.decode()
        self.assertIn("Обязательное поле.", content)

    def test_delete_current_hospitalization_ok(self):
        """Тест успешного удаления текущей госпитализации"""
        content_after = self.client.get(reverse("hospitalizations:current"))
        path = reverse("hospitalizations:delete_current", kwargs={"pk": 5})
        response = self.client.post(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        content = response.content.decode()
        self.assertNotEqual(content_after, content)
        self.assertNotIn("Иванов Михаил Сидорович", content)
        self.assertNotIn("4 января 2024 г. 17:27", content)

    def test_delete_current_hospitalization_error(self):
        """Тест ошибки удаления текущей госпитализации"""
        content_after = self.client.get(reverse("hospitalizations:current"))
        path = reverse("hospitalizations:delete_current", kwargs={"pk": 777})
        response = self.client.post(path)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_delete_hospitalization_ok(self):
        """Тест успешного удаления госпитализации"""
        path = reverse("hospitalizations:delete", kwargs={"pk": 1})
        response = self.client.post(path)
        self.assertRedirects(
            response,
            reverse("hospitalizations:hospitalizations", kwargs={"pk": 4}),
        )
        content = self.client.get(response.url)
        self.assertNotIn("19 декабря 2023 г. 9:40", content)
        path = reverse("hospitalizations:delete", kwargs={"pk": 2})
        response = self.client.post(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("patients:patients"))

    def test_delete_hospitalization_error(self):
        """Тест ошибки удаления госпитализации"""
        path = reverse("hospitalizations:delete", kwargs={"pk": 999})
        response = self.client.post(path)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_leave_ok(self):
        """Тест успешной выписки пациента"""
        path = reverse("hospitalizations:leave", kwargs={"pk": 5})
        response = self.client.post(path, {"leaving_date": "2024-02-11"})
        self.assertRedirects(response, reverse("hospitalizations:current"))
        content = self.client.get(response.url)
        self.assertNotIn("Иванов Михаил Сидорович", content)

    def test_leave_error(self):
        """Тест ошибки выписки пациента"""
        path = reverse("hospitalizations:leave", kwargs={"pk": 999})
        response = self.client.post(path)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_detail_ok(self):
        """Тест успешного получения детальной информации о пациенте
        (данные встроены в таблицу)"""
        path = reverse("hospitalizations:detail", kwargs={"pk": 5})
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_detail_error(self):
        """Тест ошибки получения детальной информации о пациенте
        (данные встроены в таблицу)"""
        path = reverse("hospitalizations:detail", kwargs={"pk": 999})
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class HospitalizationTemplateTests(AuthorizedUserTestCase):
    _headers = {"HTTP_HX-Request": "true"}
    _relay_url = "htmx/relay.html"

    @parameterized.expand(
        [
            (
                "hospitalizations:hospitalizations",
                {"pk": 1},
                "hospitalizations/hospitalizations_list.html",
            ),
            (
                "hospitalizations:current",
                None,
                "hospitalizations/current_hospitalizations_list.html",
            ),
            (
                "hospitalizations:hospitalizations",
                {"order": "surname", "direction": "asc", "pk": 1},
                "hospitalizations/hospitalizations_list.html",
            ),
            (
                "hospitalizations:current",
                {"order": "surname", "direction": "asc"},
                "hospitalizations/current_hospitalizations_list.html",
            ),
            (
                "hospitalizations:update",
                {"pk": 1},
                "tables/update_form_tr.html",
            ),
            (
                "hospitalizations:update_current",
                {"pk": 1},
                "hospitalizations/add_hospitalization.html",
            ),
            (
                "hospitalizations:create",
                None,
                "hospitalizations/add_hospitalization.html",
            ),
            (
                "hospitalizations:leave",
                {"pk": 1},
                "hospitalizations/leave.html",
            ),
            (
                "hospitalizations:detail",
                {"pk": 1},
                "tables/tr.html",
            ),
        ]
    )
    def test_template_htmx(self, viewname, kwargs, template_used):
        """Тест корректного шаблона для списка госпитализаций"""
        response = self.client.get(
            reverse(viewname, kwargs=kwargs), **self._headers
        )
        self.assertTemplateNotUsed(response, self._relay_url)
        self.assertTemplateUsed(response, template_used)

    @parameterized.expand(
        [
            (
                "hospitalizations:hospitalizations",
                {"pk": 1},
                "hospitalizations/hospitalizations_list.html",
            ),
            (
                "hospitalizations:current",
                None,
                "hospitalizations/current_hospitalizations_list.html",
            ),
            (
                "hospitalizations:hospitalizations",
                {"order": "surname", "direction": "asc", "pk": 1},
                "hospitalizations/hospitalizations_list.html",
            ),
            (
                "hospitalizations:current",
                {"order": "surname", "direction": "asc"},
                "hospitalizations/current_hospitalizations_list.html",
            ),
            (
                "hospitalizations:update",
                {"pk": 1},
                "tables/update_form_tr.html",
            ),
            (
                "hospitalizations:update_current",
                {"pk": 1},
                "hospitalizations/add_hospitalization.html",
            ),
            (
                "hospitalizations:create",
                None,
                "hospitalizations/add_hospitalization.html",
            ),
            (
                "hospitalizations:leave",
                {"pk": 1},
                "hospitalizations/leave.html",
            ),
            (
                "hospitalizations:detail",
                {"pk": 1},
                "tables/tr.html",
            ),
        ]
    )
    def test_template_html(self, viewname, kwargs, template_used):
        """Тест корректного шаблона для списка госпитализаций"""
        response = self.client.get(
            reverse(viewname, kwargs=kwargs),
        )
        self.assertTemplateUsed(response, self._relay_url)
        self.assertTemplateUsed(response, template_used)

    @parameterized.expand(
        [
            (
                "hospitalizations:current",
                None,
                [
                    'patient-asc disabled-button">',
                    'patient-desc">',
                    'entry_date-asc">',
                    'entry_date-desc">',
                ],
            ),
            (
                "hospitalizations:current",
                {"order": "patient", "direction": "desc"},
                [
                    'patient-asc">',
                    'patient-desc disabled-button">',
                    'entry_date-asc">',
                    'entry_date-desc">',
                ],
            ),
            (
                "hospitalizations:current",
                {"order": "entry_date", "direction": "desc"},
                [
                    'patient-asc">',
                    'patient-desc">',
                    'entry_date-asc">',
                    'entry_date-desc disabled-button">',
                ],
            ),
            (
                "hospitalizations:hospitalizations",
                {"pk": 4},
                [
                    'entry_date-asc disabled-button">',
                    'entry_date-desc">',
                    'leaving_date-asc">',
                    'leaving_date-desc">',
                ],
            ),
            (
                "hospitalizations:hospitalizations",
                {"pk": 4, "order": "leaving_date", "direction": "desc"},
                [
                    'entry_date-asc">',
                    'entry_date-desc">',
                    'leaving_date-asc">',
                    'leaving_date-desc disabled-button">',
                ],
            ),
        ]
    )
    def test_template_contains_correct_htmx(self, viewname, kwargs, html):
        response = self.client.get(
            reverse(viewname, kwargs=kwargs), **self._headers
        )
        self.assertTemplateNotUsed(response, self._relay_url)
        content = response.content.decode()
        for h in html:
            self.assertIn(h, content)

    @parameterized.expand(
        [
            (
                "hospitalizations:current",
                None,
                [
                    'patient-asc disabled-button">',
                    'patient-desc">',
                    'entry_date-asc">',
                    'entry_date-desc">',
                ],
            ),
            (
                "hospitalizations:current",
                {"order": "patient", "direction": "desc"},
                [
                    'patient-asc">',
                    'patient-desc disabled-button">',
                    'entry_date-asc">',
                    'entry_date-desc">',
                ],
            ),
            (
                "hospitalizations:current",
                {"order": "entry_date", "direction": "desc"},
                [
                    'patient-asc">',
                    'patient-desc">',
                    'entry_date-asc">',
                    'entry_date-desc disabled-button">',
                ],
            ),
            (
                "hospitalizations:hospitalizations",
                {"pk": 4},
                [
                    'entry_date-asc disabled-button">',
                    'entry_date-desc">',
                    'leaving_date-asc">',
                    'leaving_date-desc">',
                ],
            ),
            (
                "hospitalizations:hospitalizations",
                {"pk": 4, "order": "leaving_date", "direction": "desc"},
                [
                    'entry_date-asc">',
                    'entry_date-desc">',
                    'leaving_date-asc">',
                    'leaving_date-desc disabled-button">',
                ],
            ),
        ]
    )
    def test_template_contains_correct_html(self, viewname, kwargs, html):
        response = self.client.get(
            reverse(viewname, kwargs=kwargs),
        )
        content = response.content.decode()
        for h in html:
            self.assertIn(h, content)


class HospitalizationFormTests(AuthorizedUserTestCase):
    """Тест форм"""

    @parameterized.expand(
        [
            ("hospitalizations:create", forms.CreateHospitalizationForm, None),
            (
                "hospitalizations:update",
                forms.UpdateHospitalizationInlineForm,
                {"pk": 1},
            ),
            (
                "hospitalizations:update_current",
                forms.UpdateHospitalizationForm,
                {"pk": 1},
            ),
            (
                "hospitalizations:leave",
                forms.LeaveForm,
                {"pk": 1},
            ),
        ]
    )
    def test_form_ok(self, viewname, form_class, kwargs):
        """Тест удачного отображения формы добавления госпитализации"""
        path = reverse(viewname, kwargs=kwargs)
        self.response = self.client.get(path)

        form = self.response.context.get("form")
        self.assertIsInstance(form, form_class)
        self.assertContains(self.response, "csrfmiddlewaretoken")

    @parameterized.expand(
        [
            ("hospitalizations:create", None),
            (
                "hospitalizations:update",
                {"pk": 1},
            ),
            (
                "hospitalizations:update_current",
                {"pk": 1},
            ),
            (
                "hospitalizations:leave",
                {"pk": 1},
            ),
        ]
    )
    def test_form_bootstrap_class_used_for_default_styling(
        self, viewname, kwargs
    ):
        """Тест использования дефолтных классов boostrap при отображении формы"""
        path = reverse(viewname, kwargs=kwargs)
        self.response = self.client.get(path)

        form = self.response.context.get("form")
        self.assertIn('class="form-control"', form.as_p())

    @parameterized.expand(
        [
            (forms.CreateHospitalizationForm,),
            (forms.UpdateHospitalizationInlineForm,),
            (forms.UpdateHospitalizationForm,),
        ]
    )
    def test_form_validation_blank_error(self, form):
        """Тест ошибки валидации формы при добавлении госпитализации.
        Не все поля формы заполнены.
        """
        form = form(
            data={
                "entry_date": "",
                "patient": "",
                "doctor": "",
            }
        )
        self.assertFalse(form.is_valid())

    @parameterized.expand(
        [
            (forms.CreateHospitalizationForm,),
            (forms.UpdateHospitalizationInlineForm,),
            (forms.UpdateHospitalizationForm,),
        ]
    )
    def test_form_validation_exists_error(self, form):
        """Тест ошибки валидации формы при добавлении госпитализации
        Дата поступления или дата выписки пересекаются с уже
        существующей датой поступления или выписки для данного пациента
        """
        form = form(
            data={
                "entry_date": "2023-12-19T09:40:36Z",
                "leaving_date": "2024-01-03T01:50:00Z",
                "notes": "",
                "time_create": "2024-01-03T11:41:39.998Z",
                "time_update": "2024-01-07T17:19:33.600Z",
                "patient": 4,
                "doctor": 3,
            }
        )
        form.instance.pk = 2
        self.assertFalse(form.is_valid())

        self.assertIn(
            "Для пациента уже существует госпитализация с 19.12.2023 09:12 по 03.01.2024 01:01",
            form.errors["__all__"],
        )


class HospitalizationAuthorizedUserURLsTests(AuthorizedUserTestCase):
    """Тестирование URL'ов госпитализации"""

    @parameterized.expand(
        [
            ("hospitalizations:hospitalizations", {"pk": 1}),
            ("hospitalizations:current", None),
            (
                "hospitalizations:current",
                {"order": "surname", "direction": "asc"},
            ),
            ("hospitalizations:update_current", {"pk": 1}),
            ("hospitalizations:leave", {"pk": 1}),
            (
                "hospitalizations:hospitalizations",
                {"pk": 1, "order": "surname", "direction": "asc"},
            ),
            ("hospitalizations:create", None),
            ("hospitalizations:update", {"pk": 1}),
            ("hospitalizations:detail", {"pk": 1}),
        ]
    )
    def tests_hospitalizations_url_name(self, viewname, kwargs):
        """Тестирование URL адреса для получения списка госпитализаций"""
        response = self.client.get(reverse(viewname, kwargs=kwargs))
        self.assertEqual(response.status_code, HTTPStatus.OK)


class HospitalizationUnAuthorizedUserURLsTests(SimpleTestCase):
    """Тестирование URL'ов госпитализации"""

    @parameterized.expand(
        [
            ("hospitalizations:hospitalizations", {"pk": 1}),
            ("hospitalizations:current", None),
            (
                "hospitalizations:current",
                {"order": "surname", "direction": "asc"},
            ),
            ("hospitalizations:update_current", {"pk": 1}),
            ("hospitalizations:leave", {"pk": 1}),
            (
                "hospitalizations:hospitalizations",
                {"pk": 1, "order": "surname", "direction": "asc"},
            ),
            ("hospitalizations:create", None),
            ("hospitalizations:update", {"pk": 1}),
            ("hospitalizations:detail", {"pk": 1}),
        ]
    )
    def tests_hospitalizations_url_name(self, viewname, kwargs):
        """Тестирование URL адреса для получения списка госпитализаций
        для неавторизованного пользователя"""
        url = reverse(viewname, kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("users:login") + "?next=" + url)


class HospitalizationModelTests(TestCase):
    """Тесты модели госпитализации"""

    fixtures = [
        "patients_patient.json",
        "users_user.json",
        "hospitalizations_hospitalization.json",
    ]

    _hospitalization = {
        "entry_date": "2024-01-04T17:27:59Z",
        "leaving_date": None,
        "notes": "",
        "time_create": "2024-01-07T17:28:14.098Z",
        "time_update": "2024-01-07T17:28:14.098Z",
        "patient": 1,
        "doctor": 3,
    }

    def setUp(self):
        self._hospitalization["patient"] = Patient.objects.get(pk=1)
        self._hospitalization["doctor"] = get_user_model().objects.get(pk=3)
        self.hospitalization = Hospitalization(**self._hospitalization)

    def test_create_hospitalization(self):
        """Тест создания нового объекта в модели госпитализации"""

    def test_str_representation(self):
        """Тест строкового представления объекта госпитализации"""
        self.assertEqual(
            str(self.hospitalization),
            "{}-{}".format(
                self._hospitalization["entry_date"],
                self._hospitalization["leaving_date"],
            ),
        )

    def test_saving_hospitalization(self):
        """Тест модели - сохранение госпитализации"""

    def test_retrieving_hospitalization(self):
        """Тест модели - получение госпитализаций"""

    def test_retrieving_current_hospitalization(self):
        """Тест модели - получение текущих госпитализаций"""


class UtilsTests(TestCase):
    """Тесты для модуля utils"""

    fixtures = [
        "patients_patient.json",
        "users_user.json",
        "hospitalizations_hospitalization.json",
    ]

    _hospitalizations = Hospitalization.objects.filter(patient__pk=4)

    @parameterized.expand(
        [
            (
                datetime(
                    2024, 1, 2, 8, 15, 11, tzinfo=zoneinfo.ZoneInfo(key="UTC")
                ),
                None,
            ),
            (
                datetime(
                    2024, 1, 2, 8, 15, 13, tzinfo=zoneinfo.ZoneInfo(key="UTC")
                ),
                None,
            ),
            (
                datetime(
                    2024, 1, 2, 8, 15, 13, tzinfo=zoneinfo.ZoneInfo(key="UTC")
                ),
                datetime(
                    2024, 2, 2, 8, 15, 13, tzinfo=zoneinfo.ZoneInfo(key="UTC")
                ),
            ),
            (
                datetime(
                    2024, 1, 1, 8, 15, 13, tzinfo=zoneinfo.ZoneInfo(key="UTC")
                ),
                datetime(
                    2024, 2, 2, 8, 15, 13, tzinfo=zoneinfo.ZoneInfo(key="UTC")
                ),
            ),
            (
                datetime(
                    2023,
                    12,
                    19,
                    8,
                    15,
                    13,
                    tzinfo=zoneinfo.ZoneInfo(key="UTC"),
                ),
                datetime(
                    2024, 2, 2, 8, 15, 13, tzinfo=zoneinfo.ZoneInfo(key="UTC")
                ),
            ),
            (
                datetime(
                    2023,
                    12,
                    19,
                    8,
                    15,
                    13,
                    tzinfo=zoneinfo.ZoneInfo(key="UTC"),
                ),
                datetime(
                    2023,
                    12,
                    20,
                    8,
                    15,
                    13,
                    tzinfo=zoneinfo.ZoneInfo(key="UTC"),
                ),
            ),
            (
                datetime(
                    2024, 1, 2, 8, 15, 13, tzinfo=zoneinfo.ZoneInfo(key="UTC")
                ),
                datetime(
                    2024, 1, 5, 8, 15, 13, tzinfo=zoneinfo.ZoneInfo(key="UTC")
                ),
            ),
        ]
    )
    def test_check_dates_intersection_error(self, entry_date, leaving_date):
        """ "Тест ошибки при валидации даты, проверка на пересечение добавляемой даты
        с одной из существующих дат в списке"""
        cleaned_data = {
            "entry_date": entry_date,
            "leaving_date": leaving_date,
        }
        with self.assertRaises(ValueError):
            check_dates_intersection(cleaned_data, self._hospitalizations)

    @parameterized.expand(
        [
            (
                datetime(
                    2023,
                    12,
                    17,
                    8,
                    15,
                    11,
                    tzinfo=zoneinfo.ZoneInfo(key="UTC"),
                ),
                datetime(
                    2023,
                    12,
                    18,
                    8,
                    15,
                    11,
                    tzinfo=zoneinfo.ZoneInfo(key="UTC"),
                ),
            ),
            (
                datetime(
                    2022,
                    12,
                    17,
                    8,
                    15,
                    11,
                    tzinfo=zoneinfo.ZoneInfo(key="UTC"),
                ),
                datetime(
                    2022,
                    12,
                    18,
                    8,
                    15,
                    11,
                    tzinfo=zoneinfo.ZoneInfo(key="UTC"),
                ),
            ),
        ]
    )
    def test_check_dates_intersection_ok(self, entry_date, leaving_date):
        """ "Тест успешной валидации даты, проверка на пересечение добавляемой даты
        с одной из существующих дат в списке"""
        cleaned_data = {
            "entry_date": entry_date,
            "leaving_date": leaving_date,
        }
        self.assertIsNone(
            check_dates_intersection(cleaned_data, self._hospitalizations)
        )

    @parameterized.expand(
        [
            (
                datetime(
                    2024, 1, 2, 8, 15, 11, tzinfo=zoneinfo.ZoneInfo(key="UTC")
                ),
                datetime(
                    2024, 1, 1, 8, 15, 11, tzinfo=zoneinfo.ZoneInfo(key="UTC")
                ),
            ),
            (
                datetime(
                    2024, 1, 1, 8, 15, 12, tzinfo=zoneinfo.ZoneInfo(key="UTC")
                ),
                datetime(
                    2024, 1, 1, 8, 15, 11, tzinfo=zoneinfo.ZoneInfo(key="UTC")
                ),
            ),
        ]
    )
    def test_validate_hospitalization_fields_error(
        self, entry_date, leaving_date
    ):
        """ "Тест ошибки при валидации даты, дата поступления больше
        даты выписки"""
        cleaned_data = {
            "entry_date": entry_date,
            "leaving_date": leaving_date,
        }
        with self.assertRaises(django_forms.ValidationError):
            validate_hospitalization_fields(
                cleaned_data, self._hospitalizations
            )


class HospitalizationFilesViewTests(AuthorizedUserTestCase):
    """Тесты представлений для создания и загрузки файлов"""

    @parameterized.expand(
        [
            (
                "hospitalizations:create_current_docx",
                {"order": "surname", "direction": "asc"},
                None,
            ),
            (
                "hospitalizations:create_current_docx",
                {"order": "entry_date", "direction": "desc"},
                None,
            ),
            (
                "hospitalizations:create_current_xlsx",
                {"order": "entry_date", "direction": "desc"},
                None,
            ),
            (
                "hospitalizations:create_current_xlsx",
                {"order": "surname", "direction": "asc"},
                None,
            ),
            ("hospitalizations:create_current_by_doctor_docx", {}, None),
            ("hospitalizations:create_current_by_doctor_docx", {}, 1),
        ]
    )
    def test_current_hospitalizations_create_file_ok(
        self, viewname, kwargs, selected_doctor
    ):
        """Тест успешного создания файла с текущими госпитализациями"""

        with patch.object(file_downloader.views.CreateFileView, "get_task"):
            if selected_doctor:
                path = (
                    reverse(viewname, kwargs=kwargs)
                    + "?selected_doctor="
                    + str(selected_doctor)
                )
            else:
                path = reverse(viewname, kwargs=kwargs)
            response = self.client.get(path)

            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertIn("Создание документа", response.content.decode())

            task_id = response.context_data["task_id"]

            response = self.client.get(
                reverse(
                    "hospitalizations:task_status", kwargs={"task_id": task_id}
                )
            )
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertIn("PENDING", response.content.decode())

            with patch("file_downloader.views.DownloadFileView.get") as mock:
                mock.return_value = HttpResponse("OK")
                response = self.client.get(
                    reverse(
                        "hospitalizations:download_current_docx",
                        kwargs={"task_id": "ID"},
                    )
                )
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertEqual(response.content.decode(), "OK")


class HospitalizationFilesViewNonAuthorizedTests(TestCase):
    """Тесты представлений для создания и загрузки файлов,
    пользователь не авторизован"""

    @parameterized.expand(
        [
            (
                "hospitalizations:create_current_docx",
                {"order": "surname", "direction": "asc"},
                None,
            ),
            (
                "hospitalizations:create_current_docx",
                {"order": "entry_date", "direction": "desc"},
                None,
            ),
            (
                "hospitalizations:create_current_xlsx",
                {"order": "entry_date", "direction": "desc"},
                None,
            ),
            (
                "hospitalizations:create_current_xlsx",
                {"order": "surname", "direction": "asc"},
                None,
            ),
            ("hospitalizations:create_current_by_doctor_docx", {}, None),
            ("hospitalizations:create_current_by_doctor_docx", {}, 1),
        ]
    )
    def test_current_hospitalizations_create_file_403(
        self, viewname, kwargs, selected_doctor
    ):
        """Тест создания файла с текущими госпитализациями, пользователь
        не авторизован"""
        if selected_doctor:
            path = (
                reverse(viewname, kwargs=kwargs)
                + "?selected_doctor="
                + str(selected_doctor)
            )
        else:
            path = reverse(viewname, kwargs=kwargs)
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response, reverse("users:login") + "?next=" + path
        )

        response = self.client.get(
            reverse("hospitalizations:task_status", kwargs={"task_id": "ID"})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            reverse("users:login")
            + "?next="
            + reverse(
                "hospitalizations:task_status", kwargs={"task_id": "ID"}
            ),
        )

        with patch("file_downloader.views.DownloadFileView.get") as mock:
            mock.return_value = HttpResponse("OK")
            response = self.client.get(
                reverse(
                    "hospitalizations:download_current_docx",
                    kwargs={"task_id": "ID"},
                )
            )
            self.assertEqual(response.status_code, HTTPStatus.FOUND)
            self.assertRedirects(
                response,
                reverse("users:login")
                + "?next="
                + reverse(
                    "hospitalizations:download_current_docx",
                    kwargs={"task_id": "ID"},
                ),
            )
