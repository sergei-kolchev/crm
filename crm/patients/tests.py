from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class GetPatientsTestCase(TestCase):
    fixtures = ["patients_patient.json"]
    headers = {"HTTP_HX-Request": "true"}

    data = {
        "surname": "Акинфеев",
        "name": "Абрам",
        "patronymic": "Аронович",
        "birthday_day": "10",
        "birthday_month": "5",
        "birthday_year": "1980",
    }

    bad_data = {
        "surname": "",
        "name": "",
        "patronymic": "",
        "birthday_day": "10",
        "birthday_month": "5",
        "birthday_year": "1980",
    }

    _relay_url = "htmx/relay.html"

    def _get_path(self, template_name):
        return self._app_name + "/" + template_name

    def test_index_html_ok(self):
        path = reverse("patients:index")
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self._relay_url)
        self.assertTemplateUsed(response, "patients/main.html")
        self.assertContains(response, bytes("Находящиеся на лечении", "utf-8"))

    def test_index_htmx_ok(self):
        path = reverse("patients:index")
        response = self.client.get(path, **self.headers)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateNotUsed(response, self._relay_url)
        self.assertTemplateUsed(response, "patients/main.html")
        self.assertContains(response, bytes("Находящиеся на лечении", "utf-8"))

    def test_patients_page_html_ok(self):
        path = reverse("patients:patients")
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self._relay_url)
        self.assertContains(response, bytes("Картотека пациентов", "utf-8"))
        self.assertContains(
            response, bytes("Бондарев Николай Васильевич", "utf-8")
        )

    def test_patients_page_htmx_ok(self):
        path = reverse("patients:patients")
        response = self.client.get(path, **self.headers)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateNotUsed(response, self._relay_url)
        self.assertContains(response, bytes("Картотека пациентов", "utf-8"))
        self.assertContains(
            response, bytes("Бондарев Николай Васильевич", "utf-8")
        )

    def test_about_html_ok(self):
        path = reverse("patients:about")
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self._relay_url)
        self.assertTemplateUsed(response, "patients/about.html")
        self.assertContains(response, bytes("О проекте", "utf-8"))

    def test_about_htmx_ok(self):
        path = reverse("patients:about")
        response = self.client.get(path, **self.headers)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateNotUsed(response, self._relay_url)
        self.assertTemplateUsed(response, "patients/about.html")
        self.assertContains(response, bytes("О проекте", "utf-8"))

    def test_contacts_html_ok(self):
        path = reverse("patients:contacts")
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self._relay_url)
        self.assertTemplateUsed(response, "patients/contacts.html")
        self.assertContains(response, bytes("Контакты", "utf-8"))

    def test_contacts_htmx_ok(self):
        path = reverse("patients:contacts")
        response = self.client.get(path, **self.headers)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateNotUsed(response, self._relay_url)
        self.assertTemplateUsed(response, "patients/contacts.html")
        self.assertContains(response, bytes("Контакты", "utf-8"))

    def test_patient_detail_html_redirect(self):
        path = reverse("patients:patient_detail", kwargs={"pk": 1})
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        redirect_uri = reverse("patients:index")
        self.assertRedirects(response, redirect_uri)

    def test_patient_detail_get_htmx(self):
        path = reverse("patients:patient_detail", kwargs={"pk": 1})
        headers = {"HTTP_HX-Request": "true"}
        response = self.client.get(path, **headers)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateNotUsed(response, self._relay_url)
        self.assertTemplateUsed(
            response, "patients/includes/patient_detail.html"
        )
        self.assertContains(response, bytes("Иванов Иван Иванович", "utf-8"))

    def test_patients_page_htmx_pages_ok(self):
        params = [
            {
                "kwargs": {"order": "surname", "direction": "asc"},
                "page": "2",
                "value": "Иванов Николай Павлович",
            },
            {
                "kwargs": {"order": "surname", "direction": "desc"},
                "page": "2",
                "value": "Иванов Николай Петрович",
            },
        ]

        for param in params:
            path = (
                reverse("patients:patients", kwargs=param["kwargs"])
                + "?page="
                + param["page"]
            )
            response = self.client.get(path, **self.headers)
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertTemplateNotUsed(response, self._relay_url)
            self.assertTemplateUsed(response, "patients/patient_list.html")
            self.assertContains(
                response, bytes("Картотека пациентов", "utf-8")
            )
            self.assertContains(response, bytes(param["value"], "utf-8"))
            self.assertContains(response, bytes("2 из 2", "utf-8"))

    def test_patients_page_htmx_pages_search_ok(self):
        params = [
            {
                "kwargs": {"order": "surname", "direction": "asc"},
                "page": "1",
                "value": "Иванов Николай Павлович",
                "q": "Иванов",
            },
            {
                "kwargs": {"order": "surname", "direction": "desc"},
                "page": "1",
                "value": "Иванов Николай Петрович",
                "q": "Иванов",
            },
        ]

        for param in params:
            path = (
                reverse("patients:patients", kwargs=param["kwargs"])
                + "?q="
                + param["q"]
                + "&page="
                + param["page"]
            )
            response = self.client.get(path, **self.headers)
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertTemplateNotUsed(response, self._relay_url)
            self.assertTemplateUsed(response, "patients/patient_list.html")
            self.assertContains(
                response, bytes("Картотека пациентов", "utf-8")
            )
            self.assertContains(response, bytes(param["value"], "utf-8"))

    def test_patient_search_html_redirect(self):
        path = reverse("patients:search") + "?q=" + "Бондарев"
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        redirect_uri = reverse("patients:index")
        self.assertRedirects(response, redirect_uri)

    def test_patient_search_get_htmx(self):
        path = reverse("patients:search") + "?q=" + "Бондарев"
        headers = {"HTTP_HX-Request": "true"}
        response = self.client.get(path, **headers)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateNotUsed(response, self._relay_url)
        self.assertTemplateUsed(
            response, "patients/includes/patients_list_table.html"
        )
        self.assertContains(
            response, bytes("Бондарев Николай Васильевич", "utf-8")
        )

    def test_patient_search_get_htmx_not_found(self):
        path = reverse("patients:search") + "?q=" + "bad search query"
        headers = {"HTTP_HX-Request": "true"}
        response = self.client.get(path, **headers)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateNotUsed(response, self._relay_url)
        self.assertTemplateUsed(
            response, "patients/includes/patients_list_table.html"
        )
        self.assertContains(
            response, bytes("По вашему запросу ничего не найдено", "utf-8")
        )

    def test_create_patient_htmx_ok(self):
        path = reverse("patients:create_patient")
        headers = {"HTTP_HX-Request": "true"}

        response = self.client.post(path, self.data, **headers)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateNotUsed(response, self._relay_url)
        self.assertTemplateUsed(response, "patients/patient_list.html")

        path = reverse("patients:patients")
        response = self.client.get(path, **self.headers)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateNotUsed(response, self._relay_url)
        self.assertContains(response, bytes("Картотека пациентов", "utf-8"))
        self.assertContains(
            response, bytes("Акинфеев Абрам Аронович", "utf-8")
        )
        self.assertNotContains(
            response, bytes("* Обязательное поле.", "utf-8")
        )

    def test_create_patient_htmx_error(self):
        path = reverse("patients:create_patient")
        headers = {"HTTP_HX-Request": "true"}

        response = self.client.post(path, self.bad_data, **headers)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateNotUsed(response, self._relay_url)
        self.assertTemplateUsed(response, "patients/patient_list.html")
        self.assertContains(response, bytes("* Обязательное поле.", "utf-8"))

    def test_update_patient_htmx_ok(self):
        path = reverse("patients:update_patient", kwargs={"pk": "1"})
        headers = {"HTTP_HX-Request": "true"}

        response = self.client.post(path, self.data, **headers)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateNotUsed(response, self._relay_url)
        self.assertTemplateUsed(
            response, "patients/includes/patient_detail.html"
        )

        path = reverse("patients:patients")
        response = self.client.get(path, **self.headers)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateNotUsed(response, self._relay_url)
        self.assertContains(response, bytes("Картотека пациентов", "utf-8"))
        self.assertContains(
            response, bytes("Акинфеев Абрам Аронович", "utf-8")
        )
        self.assertNotContains(
            response, bytes("* Обязательное поле.", "utf-8")
        )

    def test_update_patient_htmx_error(self):
        path = reverse("patients:update_patient", kwargs={"pk": "1"})
        headers = {"HTTP_HX-Request": "true"}

        response = self.client.post(path, self.bad_data, **headers)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateNotUsed(response, self._relay_url)
        self.assertTemplateUsed(
            response, "patients/includes/update_patient_form.html"
        )

        path = reverse("patients:patients")
        response = self.client.get(path, **self.headers)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateNotUsed(response, self._relay_url)
        self.assertContains(response, bytes("Картотека пациентов", "utf-8"))
        self.assertContains(response, bytes("Иванов Иван Иванович", "utf-8"))

    def test_delete_redirect_to_html(self):
        path = reverse("patients:patient_delete", kwargs={"pk": "1"})
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        redirect_uri = reverse("patients:index")
        self.assertRedirects(response, redirect_uri)

    def test_delete_htmx_ok(self):
        path = reverse("patients:patient_delete", kwargs={"pk": "1"})
        response = self.client.delete(path, **self.headers)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateNotUsed(response, self._relay_url)
        self.assertTemplateUsed(
            response, "patients/includes/patient_deleted.html"
        )
        self.assertContains(response, bytes("Пациент удален", "utf-8"))

    def test_delete_htmx_page_not_found(self):
        path = reverse("patients:patient_delete", kwargs={"pk": "999"})
        response = self.client.delete(path, **self.headers)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_update_patient_status_htmx_ok(self):
        path = reverse("patients:update_patient_status", kwargs={"pk": "1"})
        headers = {"HTTP_HX-Request": "true"}

        response = self.client.post(path, self.data, **headers)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateNotUsed(response, self._relay_url)
        self.assertTemplateUsed(
            response, "patients/includes/patient_detail.html"
        )

        path = reverse("patients:patients")
        response = self.client.get(path, **self.headers)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateNotUsed(response, self._relay_url)
        self.assertContains(response, bytes("Картотека пациентов", "utf-8"))
        self.assertContains(response, bytes("Заблокирован", "utf-8"))

    def test_update_patient_status_htmx_bad_request(self):
        path = reverse("patients:update_patient_status", kwargs={"pk": "999"})
        headers = {"HTTP_HX-Request": "true"}
        response = self.client.post(path=path, data=self.data, **headers)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
