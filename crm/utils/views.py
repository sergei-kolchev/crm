from file_downloader.views import (DownloadFileDocxView, DownloadFileXlsxView,
                                   TaskStatusView)
from htmx.http import RenderPartial

from utils.utils import LoginRequiredMixin


class DownloadFileDocxAuthorizedView(
    LoginRequiredMixin, RenderPartial, DownloadFileDocxView
):
    pass


class DownloadFileXlsxAuthorizedView(
    LoginRequiredMixin, RenderPartial, DownloadFileXlsxView
):
    pass


class TaskStatusAuthorizedView(
    LoginRequiredMixin, RenderPartial, TaskStatusView
):
    pass
