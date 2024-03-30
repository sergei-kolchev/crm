from file_downloader.tasks import BuildFileTask
from hospitalizations import service

from crm import celery_app


class BuildCurrentByDoctorsDocxFileTask(BuildFileTask):
    def get_file_context(self):
        return {
            "tbl_contents": service.FileContent.get_current_by_doctors(),
        }


class BuildCurrentDocxFileTask(BuildFileTask):
    def get_file_context(self, **kwargs):
        return service.FileContent.get_current(
            selected_doctor=self.selected_doctor,
            order=self.order,
            direction=self.direction,
        )


class BuildCurrentXlsxFileTask(BuildFileTask):
    def get_file_context(self, **kwargs):
        return service.FileContent.get_current(
            selected_doctor=self.selected_doctor,
            order=self.order,
            direction=self.direction,
        )


class BuildDocxFileTask(BuildFileTask):
    def get_file_context(self, **kwargs):
        return {"obj": service.get_one(self.pk)}


BuildCurrentByDoctorsDocxFileTask = celery_app.register_task(
    BuildCurrentByDoctorsDocxFileTask()
)
BuildCurrentDocxFileTask = celery_app.register_task(BuildCurrentDocxFileTask())
BuildCurrentXlsxFileTask = celery_app.register_task(BuildCurrentXlsxFileTask())
BuildDocxFileTask = celery_app.register_task(BuildDocxFileTask())
