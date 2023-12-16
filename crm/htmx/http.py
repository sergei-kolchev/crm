import json
import warnings
from functools import cached_property, wraps
from typing import Any, Callable, Literal, TypeVar
from urllib.parse import unquote

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpRequest, HttpResponse, HttpResponseBase
from django.shortcuts import redirect
from django.template import loader


class HtmxData:
    def __init__(self, request):
        self._request = request

    def _get_header_value(self, header):
        value = self._request.headers.get(header)
        if value:
            if (
                self._request.headers.get(f"{header}-URI-AutoEncoded")
                == "true"
            ):
                value = unquote(value)
        return value

    def __bool__(self):
        return self._get_header_value("HX-Request") == "true"

    @cached_property
    def boosted(self):
        return self._get_header_value("HX-Boosted") == "true"

    @cached_property
    def current_url(self):
        return self._get_header_value("HX-Current-URL")

    @cached_property
    def history_restore_request(self):
        return self._get_header_value("HX-History-Restore-Request") == "true"

    @cached_property
    def prompt(self):
        return self._get_header_value("HX-Prompt")

    @cached_property
    def target(self):
        return self._get_header_value("HX-Target")

    @cached_property
    def trigger_name(self):
        return self._get_header_value("HX-Trigger-Name")

    @cached_property
    def trigger(self):
        return self._get_header_value("HX-Trigger")


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxData


HtmxHttpResponse = TypeVar("HtmxHttpResponse", bound=HttpResponseBase)

trigger_types = {
    "receive": "HX-Trigger",
    "settle": "HX-Trigger-After-Settle",
    "swap": "HX-Trigger-After-Swap",
}

message_types = {
    "ok": "successMessage",
    "error": "errorMessage",
}


def require_HTMX(redirect_url: str | Callable) -> Callable:
    def decorator(f):
        @wraps(f)
        def inner(request, *args, **kwargs):
            if not request.htmx:
                if callable(redirect_url):
                    return redirect_url(request, *args, **kwargs)
                return redirect(redirect_url)
            return f(request, *args, **kwargs)

        return inner

    return decorator


def send_message(
    response: HtmxHttpResponse, message_type: str | list | tuple | dict
) -> HtmxHttpResponse:
    if type(message_type) not in (str, list, tuple, dict):
        raise TypeError("Type for message must be one of: str, list, tuple")

    if type(message_type) is str:
        message_type = message_type.strip().split(", ")

    if not message_type:
        raise ValueError("Message can't be an empty")

    if type(message_type) is dict:
        message = {message_types.get(k, k): v for k, v in message_type.items()}
    else:
        message = ", ".join(
            [message_types.get(msg, msg) for msg in message_type]
        )
    return create_trigger_event(response, message)


def create_trigger_event(
    response: HtmxHttpResponse,
    trigger: str | dict[str, str | dict],
    trigger_type: Literal["receive", "settle", "swap"] = "receive",
    encoder: type[json.JSONEncoder] = DjangoJSONEncoder,
) -> HtmxHttpResponse:
    if type(trigger) not in (str, dict):
        raise TypeError("Type for trigger must be one of: str, dict")

    if trigger_type not in trigger_types or type(trigger_type) is not str:
        raise ValueError(
            "Value for trigger_type must be on of: receive, settle, swap"
        )

    if type(trigger) is str:
        trigger = trigger.strip()

    if not trigger:
        raise ValueError(
            f"Trigger cannot contain an empty string or an empty dictionary, "
            f"passed type {type(trigger)}, value - {trigger}"
        )

    header = trigger_types.get(trigger_type, None)

    if header in response:
        data = response[header]
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"{header}, JSON is invalid. {e}")

        if type(data) is not type(trigger):
            message = (
                f"{type(trigger)} and {type(data)} are"
                f"different data types, data types must be the same"
            )
            warnings.warn(
                message, category=RuntimeWarning, stacklevel=2, source=None
            )
        if type(data) is str and type(trigger) is str:
            if not data:
                data = trigger
            else:
                data = f"{data}, {trigger}"
        elif type(data) is dict and type(trigger) is str:
            trigger_array = trigger.split(", ")
            for t in trigger_array:
                data.update({t: {}})
        elif type(data) is dict and type(trigger) is dict:
            data.update(trigger)
        else:  # data - str, trigger - dict
            if not data:
                data = trigger
            else:
                data_array = data.split(", ")
                data = {}
                for d in data_array:
                    trigger.update({d: {}})
                data.update(trigger)
    else:
        data = trigger
    response[header] = json.dumps(data, cls=encoder)

    return response


def render_partial(
    request: Any,
    template_name: Any,
    context: Any = None,
    content_type: Any = None,
    status: Any = None,
    using: Any = None,
    message: str | list[str] | dict[str, Any] | None = None,
):
    if not request.htmx:
        context["template_include"] = template_name
        template_name = "htmx/relay.html"

    content = loader.render_to_string(
        template_name, context, request, using=using
    )
    response = HttpResponse(content, content_type, status)
    if message:
        response = send_message(response, message)
    return response
