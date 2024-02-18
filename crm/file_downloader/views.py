import logging
from pathlib import PosixPath

from celery.result import AsyncResult
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from crm import settings

logger = logging.getLogger("django.console")


class CreateFileView(TemplateView):
    task = None
    template_file_path = None
    temp_file_extension = None
    template_name = "http_files/create.html"
    download_url = None
    task_kwargs = {}

    __attrs = {
        "template_file_path": (str, PosixPath),
        "download_url": (str,),
        "task": (callable,),
        "temp_file_extension": (str,),
        "template_name": (str,),
        "task_kwargs": (dict,),
    }

    def __setattr__(self, key, value):
        if key in self.__attrs and type(value) not in self.__attrs[key]:
            raise TypeError("Invalid type, expected type 'str'")
        super().__setattr__(key, value)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.template_file_path:
            raise ValueError(
                "Attribute template_file_path can't be None or empty string"
            )

        if not self.download_url:
            raise ValueError("Attribute download_url can't be empty string")

        if not self.temp_file_extension:
            raise ValueError(
                "Attribute temp_file_extension can't be empty string"
            )

        if not self.task:
            raise ValueError("Attribute task can't be None")

        self.template_file_path = settings.MEDIA_ROOT / self.template_file_path

    def get_temp_file_extension(self):
        return self.temp_file_extension

    def get_download_url(self, task_id):
        return reverse(self.download_url, args=[task_id])

    def get_task(self):
        return self.task

    def get_task_kwargs(self):
        return self.task_kwargs

    def get_template_file_path(self):
        return self.template_file_path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            result = self.get_task().delay(
                str(self.template_file_path),
                self.get_temp_file_extension(),
                **self.get_task_kwargs(),
            )
        except Exception as ex:
            logger.error(f"{__name__} connection refused {ex}")
            context["error"] = "Server unavailable"
        else:
            logger.info(f'{__name__} created task "{result}"')
            context["task_id"] = result
            context["download_url"] = self.get_download_url(result)
        return context


class DownloadFileView(View):
    content_type = None
    filename = None
    extension = None

    __attrs = {
        "content_type": (str, PosixPath),
        "filename": (str,),
        "extension": (str,),
    }

    def __setattr__(self, key, value):
        if key in self.__attrs and type(value) not in self.__attrs[key]:
            raise TypeError(f"Invalid type, expected type {self.__attrs[key]}")
        super().__setattr__(key, value)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.content_type:
            raise ValueError("Attribute content_type can't be empty")

        if not self.filename:
            raise ValueError("Attribute filename can't be empty")

        if not self.extension:
            raise ValueError("Attribute extension can't be empty")

    def get_filename(self):
        return self.filename

    def get_extension(self):
        return self.extension

    def get_content_type(self):
        return self.content_type

    def get(self, request, task_id, *args, **kwargs):
        result = AsyncResult(task_id)
        filename = result.result
        logger.info(f'{__name__} opening file "{filename}"')
        with open(filename, "rb") as file:
            response = HttpResponse(file, content_type=self.get_content_type())
            response[
                "Content-Disposition"
            ] = "attachment; filename={}.{}".format(
                self.get_filename(), self.get_extension()
            )
            logger.info(f'{__name__} make response with file "{filename}"')
            return response


class TaskStatusView(View):
    def get(self, request, task_id, *args, **kwargs):
        result = AsyncResult(task_id)
        return JsonResponse({"task_status": result.status})


class DownloadFileXlsxView(DownloadFileView):
    content_type = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    filename = "file"
    extension = "xlsx"


class DownloadFileDocxView(DownloadFileView):
    content_type = (
        "application/vnd.openxmlformats-officedocument."
        "wordprocessingml.document"
    )
    filename = "file"
    extension = "docx"


class CreateFileXlsxView(CreateFileView):
    temp_file_extension = "xlsx"


class CreateFileDocxView(CreateFileView):
    temp_file_extension = "docx"
