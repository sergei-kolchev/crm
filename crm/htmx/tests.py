import copy
import json
from unittest import TestCase
from unittest.mock import MagicMock, Mock
from urllib.parse import quote

from django.core.serializers.json import DjangoJSONEncoder
from django.urls import exceptions
from parameterized import parameterized

from .http import HtmxData, create_trigger_event, require_HTMX, send_message

headers = ("HX-Trigger", "HX-Trigger-After-Settle", "HX-Trigger-After-Swap")
existing_triggers = (
    "some_triggers",
    "",
    " ",
    "trigger1, trigger2",
    {"exist_trigger1": {"key": "value"}},
    {"exist_trigger2": "value"},
)
messages = (
    "message",
    "message1, message2",
    {"message": "some params"},
    {"message1": "some 1"},
)

trigger_types = {
    "HX-Trigger": "receive",
    "HX-Trigger-After-Settle": "settle",
    "HX-Trigger-After-Swap": "swap",
}

params = []

for header in headers:
    for trigger in existing_triggers:
        for message in messages:
            expected = {}
            if type(trigger) is str and type(message) is str:
                trigger = trigger.strip()
                if not trigger:
                    expected = message
                else:
                    expected = f"{trigger}, {message}"
            elif type(trigger) is dict and type(message) is str:
                message_array = message.split(", ")
                expected.update(trigger)
                for m in message_array:
                    expected.update({m: {}})
            elif type(trigger) is dict and type(message) is dict:
                expected = copy.deepcopy(trigger)
                expected.update(message)
            else:  # trigger - str, message - dict
                break
            test_params = (
                header,
                trigger,
                message,
                trigger_types[header],
                expected,
            )
            params.append(test_params)


bad_types = (
    ["bad trigger"],
    {"bad trigger"},
    0,
    1,
    None,
    True,
    False,
    callable,
)
bad_types_list = []

for t in bad_types:
    bad_types_list.append(
        ("HX-Trigger", "exiting_trigger", t, "receive", TypeError),
    )


class HtmxTestCase(TestCase):
    @parameterized.expand(params)
    def test_create_trigger_event_ok(
        self, header, existing_triggers, trigger, trigger_type, expected
    ):
        data = {header: json.dumps(existing_triggers, cls=DjangoJSONEncoder)}
        httpResponseMock = MagicMock()

        httpResponseMock.__iter__.return_value = data.items()
        httpResponseMock.__getitem__ = lambda _, x: data.get(x)
        httpResponseMock.__contains__ = lambda _, x: x in data
        httpResponseMock.__setitem__ = lambda _, key, value: data.__setitem__(
            key, value
        )

        create_trigger_event(httpResponseMock, trigger, trigger_type)
        self.assertIn(header, data)
        self.assertEqual(json.loads(data[header]), expected)

    @parameterized.expand(
        [
            (
                "HX-Trigger",
                "exiting_trigger",
                {"message1": "value1"},
                "receive",
                {"message1": "value1", "exiting_trigger": {}},
            ),
            (
                "HX-Trigger",
                "exiting_trigger1, exiting_trigger2",
                {"message1": "value1"},
                "receive",
                {
                    "message1": "value1",
                    "exiting_trigger1": {},
                    "exiting_trigger2": {},
                },
            ),
            (
                "HX-Trigger",
                "exiting_trigger1, exiting_trigger2",
                {"message1": "value1", "message2": {"k": "v"}},
                "receive",
                {
                    "message1": "value1",
                    "exiting_trigger1": {},
                    "exiting_trigger2": {},
                    "message2": {"k": "v"},
                },
            ),
        ]
    )
    def test_create_trigger_event_where_trigger_json_ok(
        self, header, existing_triggers, trigger, trigger_type, expected
    ):
        data = {header: json.dumps(existing_triggers, cls=DjangoJSONEncoder)}
        httpResponseMock = MagicMock()

        httpResponseMock.__iter__.return_value = data.items()
        httpResponseMock.__getitem__ = lambda _, x: data.get(x)
        httpResponseMock.__contains__ = lambda _, x: x in data
        httpResponseMock.__setitem__ = lambda _, key, value: data.__setitem__(
            key, value
        )

        create_trigger_event(httpResponseMock, trigger, trigger_type)
        self.assertIn(header, data)
        self.assertEqual(json.loads(data[header]), expected)

    @parameterized.expand(
        [
            (
                "Bad header",
                "exiting_trigger",
                {"message1": "value1"},
                "",
                ValueError,
            ),
            ("HX-Trigger", "exiting_trigger", "", ["bad type"], TypeError),
            (
                "HX-Trigger",
                "exiting_trigger",
                ["bad trigger"],
                ["bad type"],
                TypeError,
            ),
            ("HX-Trigger", "exiting_trigger", "", "receive", ValueError),
            (
                "HX-Trigger",
                "exiting_trigger",
                "       ",
                "receive",
                ValueError,
            ),
            ("HX-Trigger", "exiting_trigger", {}, "receive", ValueError),
        ]
    )
    def test_create_trigger_event_bad_value_error(
        self, header, existing_triggers, trigger, trigger_type, exception
    ):
        data = {header: json.dumps(existing_triggers, cls=DjangoJSONEncoder)}
        httpResponseMock = MagicMock()
        httpResponseMock.__iter__.return_value = data.items()
        httpResponseMock.__getitem__ = lambda _, x: data.get(x)
        httpResponseMock.__contains__ = lambda _, x: x in data
        httpResponseMock.__setitem__ = lambda _, key, value: data.__setitem__(
            key, value
        )

        with self.assertRaises(exception):
            create_trigger_event(httpResponseMock, trigger, trigger_type)

    @parameterized.expand(bad_types_list)
    def test_create_trigger_event_bad_type_error(
        self, header, existing_triggers, trigger, trigger_type, exception
    ):
        data = {header: json.dumps(existing_triggers, cls=DjangoJSONEncoder)}
        httpResponseMock = MagicMock()

        httpResponseMock.__iter__.return_value = data.items()
        httpResponseMock.__getitem__ = lambda _, x: data.get(x)
        httpResponseMock.__contains__ = lambda _, x: x in data
        httpResponseMock.__setitem__ = lambda _, key, value: data.__setitem__(
            key, value
        )

        with self.assertRaises(exception):
            create_trigger_event(httpResponseMock, trigger, trigger_type)

    @parameterized.expand(
        [
            ("ok", "successMessage"),
            ("error", "errorMessage"),
            ("someMessage", "someMessage"),
            ("someMessage1, someMessage2", "someMessage1, someMessage2"),
            (["someMessage1", "someMessage2"], "someMessage1, someMessage2"),
            (("someMessage1", "someMessage2"), "someMessage1, someMessage2"),
            (
                {"someMessage1": "value1", "someMessage2": "value2"},
                {"someMessage1": "value1", "someMessage2": "value2"},
            ),
        ]
    )
    def test_send_message_ok(self, message, expand):
        data = {"HX-Trigger": json.dumps("", cls=DjangoJSONEncoder)}

        httpResponseMock = MagicMock()
        httpResponseMock.__iter__.return_value = data.items()
        httpResponseMock.__getitem__ = lambda _, x: data.get(x)
        httpResponseMock.__contains__ = lambda _, x: x in data
        httpResponseMock.__setitem__ = lambda _, key, value: data.__setitem__(
            key, value
        )
        send_message(httpResponseMock, message)
        self.assertEqual(
            data["HX-Trigger"], json.dumps(expand, cls=DjangoJSONEncoder)
        )  # JSON

    @parameterized.expand(
        [
            (0, TypeError),
            (1, TypeError),
            (True, TypeError),
            (None, TypeError),
            (set(), TypeError),
            (b"", TypeError),
            (0.1, TypeError),
            ("", ValueError),
            ({}, ValueError),
            ([], ValueError),
            ("      ", ValueError),
            ([""], ValueError),
            (["  "], ValueError),
        ]
    )
    def test_send_message_error(self, message, exception):
        data = {"HX-Trigger": json.dumps("", cls=DjangoJSONEncoder)}

        httpResponseMock = MagicMock()
        httpResponseMock.__iter__.return_value = data.items()
        httpResponseMock.__getitem__ = lambda _, x: data.get(x)
        httpResponseMock.__contains__ = lambda _, x: x in data
        httpResponseMock.__setitem__ = lambda _, key, value: data.__setitem__(
            key, value
        )
        with self.assertRaises(exception):
            send_message(httpResponseMock, message)

    @parameterized.expand(
        [
            ({"HX-Request": "true"},),
            (
                {
                    "HX-Request-URI-AutoEncoded": "true",
                    "HX-Request": quote("true"),
                },
            ),
        ]
    )
    def test_htmx_data_return_true(self, data):
        httpRequestMock = MagicMock()
        httpRequestMock.headers = data
        htmx = HtmxData(httpRequestMock)
        self.assertTrue(htmx)

    @parameterized.expand(
        [("",), (" ",), (None,), (0,), (1,), ("bad string",)]
    )
    def test_htmx_data_return_false(self, header_data):
        data = {"HX-Request": header_data}
        httpRequestMock = MagicMock()
        httpRequestMock.headers = data
        htmx = HtmxData(httpRequestMock)
        self.assertFalse(htmx)

    def test_htmx_data_boosted_true(self):
        data = {"HX-Boosted": "true"}
        httpRequestMock = MagicMock()
        httpRequestMock.headers = data
        htmx = HtmxData(httpRequestMock)
        self.assertTrue(htmx.boosted)

    @parameterized.expand(
        [("",), (" ",), (None,), (0,), (1,), ("bad string",)]
    )
    def test_htmx_data_boosted_false(self, header_data):
        data = {"HX-Boosted": header_data}
        httpRequestMock = MagicMock()
        httpRequestMock.headers = data
        htmx = HtmxData(httpRequestMock)
        self.assertFalse(htmx.boosted)

    def test_htmx_data_boosted_empty_data(self):
        data = {}
        httpRequestMock = MagicMock()
        httpRequestMock.headers = data
        htmx = HtmxData(httpRequestMock)
        self.assertFalse(htmx.boosted)

    @parameterized.expand(
        [
            ({"HX-Current-URL": "url"}, "current_url", "url"),
            (
                {"HX-History-Restore-Request": "true"},
                "history_restore_request",
                True,
            ),
            ({"HX-Prompt": "data"}, "prompt", "data"),
            ({"HX-Target": "data"}, "target", "data"),
            ({"HX-Trigger-Name": "data"}, "trigger_name", "data"),
            ({"HX-Trigger": "data"}, "trigger", "data"),
        ]
    )
    def test_htmx_get_data_true(self, data, method, expected):
        httpRequestMock = MagicMock()
        httpRequestMock.headers = data
        htmx = HtmxData(httpRequestMock)
        self.assertEqual(htmx.__getattribute__(method), expected)

    @parameterized.expand(
        [
            ({"HX-Undefined": "url"}, "current_url", "url"),
        ]
    )
    def test_htmx_get_trigger_error(self, data, method, expected):
        httpRequestMock = MagicMock()
        httpRequestMock.headers = data
        htmx = HtmxData(httpRequestMock)
        self.assertEqual(htmx.__getattribute__(method), None)

    def test_require_htmx_requst_with_not_htmx_and_call(self):
        data = {"HX-Request": "true"}
        httpRequestMock = MagicMock()
        httpRequestMock.headers = data
        httpRequestMock.htmx = False
        url = Mock()
        require_HTMX(url)(lambda x: x)(httpRequestMock)()
        url.assert_called()

    def test_require_htmx_requst_not_htmx_and_url(self):
        data = {"HX-Request": "true"}
        httpRequestMock = MagicMock()
        httpRequestMock.headers = data
        httpRequestMock.htmx = False
        url = "url"
        with self.assertRaises(exceptions.NoReverseMatch):
            require_HTMX(url)(lambda x: x)(httpRequestMock)()

    def test_require_htmx_requst_with_htmx(self):
        data = {"HX-Request": "true"}
        httpRequestMock = MagicMock()
        httpRequestMock.headers = data
        httpRequestMock.htmx = True
        func = Mock()
        url = "url"
        require_HTMX(url)(func)(httpRequestMock)()
        func.assert_called()
        func.assert_called_with(httpRequestMock)
