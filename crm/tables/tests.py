from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized

from tables import buttons, fields
from tables.builders import TableHeaderCellBuilder
from tables.cells import TableHeaderCell
from tables.html import HTMLAttributes


class TableHeaderCellTestCase(TestCase):
    @parameterized.expand(
        [
            (
                "surname",
                "Название ячейки",
                {"style": "width:20%"},
                "asc_url",
                "desc_url",
                True,
            ),
            ("name", "", {"style": "width:50%"}, "asc_url", "desc_url", False),
        ]
    )
    def test_create_ok(
        self, name, verbose_name, attrs, asc_url, desc_url, visible
    ):
        cell = TableHeaderCell(
            _name=name,
            _verbose_name=verbose_name,
            _attrs_th=HTMLAttributes(attrs),
            _asc_sorting_url=asc_url,
            _desc_sorting_url=desc_url,
            _visible=visible,
        )
        self.assertIsInstance(cell, TableHeaderCell)
        if verbose_name:
            self.assertEqual(cell.name, verbose_name)
        else:
            self.assertEqual(cell.name, name.title())
        self.assertEqual(cell.attrs, HTMLAttributes(attrs).raw)
        self.assertEqual(cell.asc_sorting_url, asc_url)
        self.assertEqual(cell.desc_sorting_url, desc_url)
        self.assertEqual(cell.visible, visible)


class TableHeaderCellBuilderTestCase(TestCase):
    @parameterized.expand(
        [
            (
                "surname",
                "hospitalizations:current",
                {"order": "surname", "direction": "asc"},
                {"doctor": "3"},
            ),
            (
                "name",
                "hospitalizations:current",
                {"order": "name", "direction": "asc"},
                {},
            ),
            (
                "name",
                "hospitalizations:current",
                {"order": "name", "direction": "asc"},
                {"doctor": "3", "nurse": "4"},
            ),
            ("entry_date", "hospitalizations:current", {}, {}),
            ("surname", "hospitalizations:current", {}, {"doctor": "3"}),
        ]
    )
    def test_get_sorting_url_ok(
        self, name, view_name, request_kwargs, request_params
    ):
        builder = TableHeaderCellBuilder()
        params = {
            "_name": name,
            "_view_name_th": view_name,
            "_request_kwargs": request_kwargs,
            "_request_params": request_params,
        }
        result = builder(**params)
        self.assertIsInstance(result, TableHeaderCell)

        if not params["_request_kwargs"]:
            params["_request_kwargs"] = {
                "order": params["_name"],
                "direction": "asc",
            }

        url = reverse(
            viewname=params["_view_name_th"],
            kwargs=params["_request_kwargs"],
        )
        params["_request_kwargs"]["direction"] = "desc"
        url_desc = reverse(
            viewname=params["_view_name_th"],
            kwargs=params["_request_kwargs"],
        )

        if params["_request_params"]:
            url = (
                url
                + "?"
                + "&".join(
                    [f"{k}={v}" for k, v in params["_request_params"].items()]
                )
            )
            url_desc = (
                url_desc
                + "?"
                + "&".join(
                    [f"{k}={v}" for k, v in params["_request_params"].items()]
                )
            )

        self.assertEqual(
            result.asc_sorting_url,
            url,
        )
        self.assertEqual(
            result.desc_sorting_url,
            url_desc,
        )

    @parameterized.expand([("",), (None,)])
    def test_get_sorting_url_none(self, view_name):
        builder = TableHeaderCellBuilder()
        params = {
            "_name": "surname",
            "_view_name_th": view_name,
        }
        result = builder(**params)
        self.assertIsInstance(result, TableHeaderCell)


class TextFieldTestCase(TestCase):
    @parameterized.expand(
        [
            (
                {
                    "default": "Default value",
                    "name": "surname",
                    "verbose_name": "Field",
                    "visible": True,
                    "attrs_th": None,
                    "attrs_td": None,
                    "converters": None,
                },
            ),
            (
                {
                    "default": "Default value",
                    "name": "surname",
                    "verbose_name": "Field",
                    "visible": False,
                    "attrs_th": HTMLAttributes(attrs={"styl": "width:30%"}),
                    "attrs_td": HTMLAttributes(attrs={"style": "width:30%"}),
                    "converters": None,
                },
            ),
            (
                {
                    "default": "Default value",
                    "name": "surname",
                    "verbose_name": "Field",
                    "visible": False,
                    "attrs_th": HTMLAttributes(attrs={"styl": "width:30%"}),
                    "attrs_td": HTMLAttributes(attrs={"style": "width:30%"}),
                    "converters": None,
                },
            ),
        ]
    )
    def test_text_field_ok(self, params):
        field = fields.TextField(**params)
        d = field.to_dict()
        for key, value in d.items():
            self.assertIn(key[1:], params)
            self.assertEqual(value, params[key[1:]])

        self.assertEqual(field.name, params["name"])
        self.assertEqual(field.verbose_name, params["verbose_name"])
        self.assertEqual(field.visible, params["visible"])
        self.assertEqual(field.attrs_td, params["attrs_td"])
        self.assertEqual(field.attrs_th, params["attrs_th"])
        self.assertEqual(field.converters, params["converters"])
        field.name = "new_name"
        self.assertEqual(field.name, "new_name")
        self.assertIsInstance(field.to_dict(), dict)

    @parameterized.expand(
        [
            ({"default": 1},),
            ({"default": 1.0},),
            ({"default": False},),
            ({"default": object},),
            ({"name": 1},),
            ({"name": 1.0},),
            ({"name": False},),
            ({"name": object},),
            ({"verbose_name": 1},),
            ({"verbose_name": 1.0},),
            ({"verbose_name": False},),
            ({"verbose_name": object},),
            ({"visible": 1},),
            ({"visible": 1.0},),
            ({"visible": "text"},),
            ({"visible": object},),
            ({"attrs_th": 1},),
            ({"attrs_th": 1.0},),
            ({"attrs_th": "text"},),
            ({"attrs_th": object},),
            ({"attrs_td": 1},),
            ({"attrs_td": 1.0},),
            ({"attrs_td": "text"},),
            ({"attrs_td": object},),
            ({"attrs_td": 1},),
            ({"attrs_td": 1.0},),
            ({"attrs_td": "text"},),
            ({"attrs_td": object},),
        ]
    )
    def test_text_field_type_check_error(self, params):
        with self.assertRaises(TypeError):
            fields.TextField(**params)


class TextSortedFieldTestCase(TestCase):
    @parameterized.expand(
        [
            (
                {
                    "default": "Default value",
                    "name": "surname",
                    "verbose_name": "Field",
                    "visible": True,
                    "attrs_th": None,
                    "attrs_td": None,
                    "converters": None,
                    "view_name_th": "view",
                },
            ),
            (
                {
                    "default": "Default value",
                    "name": "surname",
                    "verbose_name": "Field",
                    "visible": False,
                    "attrs_th": HTMLAttributes(attrs={"styl": "width:30%"}),
                    "attrs_td": HTMLAttributes(attrs={"style": "width:30%"}),
                    "converters": None,
                    "view_name_th": "view",
                },
            ),
            (
                {
                    "default": "Default value",
                    "name": "surname",
                    "verbose_name": "Field",
                    "visible": False,
                    "attrs_th": HTMLAttributes(attrs={"styl": "width:30%"}),
                    "attrs_td": HTMLAttributes(attrs={"style": "width:30%"}),
                    "converters": None,
                    "view_name_th": "view",
                },
            ),
        ]
    )
    def test_text_sorted_field_ok(self, params):
        field = fields.TextSortedField(**params)
        d = field.to_dict()
        for key, value in d.items():
            self.assertIn(key[1:], params)
            self.assertEqual(value, params[key[1:]])

    @parameterized.expand(
        [
            ({"default": 1},),
            ({"default": 1.0},),
            ({"default": False},),
            ({"default": object},),
            ({"name": 1},),
            ({"name": 1.0},),
            ({"name": False},),
            ({"name": object},),
            ({"verbose_name": 1},),
            ({"verbose_name": 1.0},),
            ({"verbose_name": False},),
            ({"verbose_name": object},),
            ({"visible": 1},),
            ({"visible": 1.0},),
            ({"visible": "text"},),
            ({"visible": object},),
            ({"attrs_th": 1},),
            ({"attrs_th": 1.0},),
            ({"attrs_th": "text"},),
            ({"attrs_th": object},),
            ({"attrs_td": 1},),
            ({"attrs_td": 1.0},),
            ({"attrs_td": "text"},),
            ({"attrs_td": object},),
            ({"attrs_td": 1},),
            ({"attrs_td": 1.0},),
            ({"attrs_td": "text"},),
            ({"attrs_td": object},),
        ]
    )
    def test_text_sorted_field_type_check_error(self, params):
        with self.assertRaises(TypeError):
            fields.TextField(**params)


class TextLinkFieldTestCase(TestCase):
    @parameterized.expand(
        [
            (
                {
                    "default": "Default value",
                    "name": "surname",
                    "verbose_name": "Field",
                    "visible": True,
                    "attrs_th": None,
                    "attrs_td": None,
                    "converters": None,
                    "view_name_td": "view",
                },
            ),
            (
                {
                    "default": "Default value",
                    "name": "surname",
                    "verbose_name": "Field",
                    "visible": False,
                    "attrs_th": HTMLAttributes(attrs={"styl": "width:30%"}),
                    "attrs_td": HTMLAttributes(attrs={"style": "width:30%"}),
                    "converters": None,
                    "view_name_td": "view",
                },
            ),
            (
                {
                    "default": "Default value",
                    "name": "surname",
                    "verbose_name": "Field",
                    "visible": False,
                    "attrs_th": HTMLAttributes(attrs={"styl": "width:30%"}),
                    "attrs_td": HTMLAttributes(attrs={"style": "width:30%"}),
                    "converters": None,
                    "view_name_td": "view",
                },
            ),
        ]
    )
    def test_text_link_field_ok(self, params):
        field = fields.LinkField(**params)
        d = field.to_dict()
        for key, value in d.items():
            self.assertIn(key[1:], params)
            self.assertEqual(value, params[key[1:]])

    @parameterized.expand(
        [
            ({"default": 1},),
            ({"default": 1.0},),
            ({"default": False},),
            ({"default": object},),
            ({"name": 1},),
            ({"name": 1.0},),
            ({"name": False},),
            ({"name": object},),
            ({"verbose_name": 1},),
            ({"verbose_name": 1.0},),
            ({"verbose_name": False},),
            ({"verbose_name": object},),
            ({"visible": 1},),
            ({"visible": 1.0},),
            ({"visible": "text"},),
            ({"visible": object},),
            ({"attrs_th": 1},),
            ({"attrs_th": 1.0},),
            ({"attrs_th": "text"},),
            ({"attrs_th": object},),
            ({"attrs_td": 1},),
            ({"attrs_td": 1.0},),
            ({"attrs_td": "text"},),
            ({"attrs_td": object},),
            ({"attrs_td": 1},),
            ({"attrs_td": 1.0},),
            ({"attrs_td": "text"},),
            ({"attrs_td": object},),
        ]
    )
    def test_text_link_field_type_check_error(self, params):
        with self.assertRaises(TypeError):
            fields.LinkField(**params)


class AllFieldsTestCase(TestCase):
    @parameterized.expand(
        [
            (fields.TextField,),
            (fields.TextSortedField,),
            (fields.ButtonsField,),
            (fields.LinkField,),
            (fields.TextLinkSortedField,),
        ]
    )
    def test_fields_type_error(self, field_class):
        with self.assertRaises(TypeError):
            field_class(bad_attribute="")

    @parameterized.expand(
        [
            (fields.TextField,),
            (fields.TextSortedField,),
            (fields.LinkField,),
            (fields.TextLinkSortedField,),
        ]
    )
    def test_fields_get_attribute_error(self, field_class):
        field = field_class(name="some name")
        with self.assertRaises(AttributeError):
            a = field.bad_attribute

    @parameterized.expand(
        [
            (fields.TextField,),
            (fields.TextSortedField,),
            (fields.LinkField,),
            (fields.TextLinkSortedField,),
        ]
    )
    def test_fields_del_attribute_error(self, field_class):
        field = field_class(name="some name")
        with self.assertRaises(AttributeError):
            del field.name


class ButtonsFieldTestCase(TestCase):
    def test_buttons_field_ok(self):
        field = fields.ButtonsField(
            buttons=[
                buttons.UpdateButton(name="update"),
                buttons.DeleteButton(name="delete"),
                buttons.ConfirmButton(name="confirm"),
            ]
        )
        self.assertEqual(len(field.buttons), 3)
        self.assertIsInstance(field.buttons[0], buttons.Button)
        self.assertEqual(field.buttons[0].name, "update")

    @parameterized.expand(
        [
            ([0, 1],),
            ([True, 1],),
            ([0.0, 0.9],),
            (
                [
                    fields.Field,
                ],
            ),
            ((0, 1),),
            (
                [
                    list,
                ],
            ),
            (tuple(),),
            (dict(),),
            (set(),),
            (None,),
            (
                [
                    None,
                ],
            ),
            ("",),
            (
                [
                    "",
                ],
            ),
        ]
    )
    def test_buttons_field_error(self, param):
        with self.assertRaises(TypeError):
            field = fields.ButtonsField(buttons=param)
