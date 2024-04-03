import celery
from django.core.files.temp import NamedTemporaryFile

from .renders import renders_list


class BuildFileTask(celery.Task):
    temp_file_extension = ""
    template_file_path = ""
    broker_connection_retry = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_file_context(self):
        raise NotImplementedError(
            "Can't use 'get_file_context' on an BuildFileTask"
        )

    def build(self):
        outfile = NamedTemporaryFile(
            suffix=f".{self.temp_file_extension}", delete=False
        )

        if self.temp_file_extension not in renders_list:
            raise ValueError(
                f"Unknown type of file - {self.temp_file_extension}"
            )

        render = renders_list.get(self.temp_file_extension)

        if not render or not callable(render):
            raise ValueError(f"Render must be a callable - {type(render)}")

        render(self.template_file_path, self.get_file_context(), outfile)
        return outfile.name

    def run(self, template_file_path, temp_file_extension="docx", **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)
        self.template_file_path = template_file_path
        self.temp_file_extension = temp_file_extension
        try:
            return self.build()
        except Exception as exc:
            self.retry(exc=exc, countdown=5)
