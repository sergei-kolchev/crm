from pathlib import Path
from unittest.mock import Mock

from django.test import TestCase
from file_downloader.views import CreateFileView, DownloadFileView
from parameterized import parameterized


class CreateFileViewTests(TestCase):
    """Тесты для класса CreateFileView, отвечающего за создание файла"""

    def test_create_object_ok(self):
        """Тест успешного создания экземпляра класса CreateFileView"""
        CreateFileView.template_file_path = "/path/to/file"
        CreateFileView.download_url = "/path/to/file"
        CreateFileView.temp_file_extension = "docx"
        CreateFileView.task = Mock()

        create_file = CreateFileView()

        create_file.task.result = create_file.template_file_path

        self.assertEqual(create_file.get_temp_file_extension(), "docx")
        self.assertEqual(create_file.get_task_kwargs(), {})
        self.assertEqual(
            create_file.get_template_file_path(),
            Path(CreateFileView.template_file_path),
        )

    @parameterized.expand(
        [
            ("", "", "", ValueError),
            ("", "url", "ext", ValueError),
            ("path", "", "ext", ValueError),
            ("path", "url", "", ValueError),
            (None, "url", "ext", TypeError),
            (1, 2, "ext", TypeError),
            ("path", 1.0, "ext", TypeError),
            ("path", True, "", TypeError),
        ]
    )
    def test_create_object_error(self, path, url, extension, ex):
        """Тест ошибки при создании экземпляра класса CreateFileView"""
        with self.assertRaises(ex):
            CreateFileView(
                template_file_path=path,
                download_url=url,
                temp_file_extension=extension,
            )


class DownloadFileViewTests(TestCase):
    """Тесты для класса DownloadFileView, отвечающего за создание файла"""

    def test_create_object_ok(self):
        """Тест успешного создания экземпляра класса DownloadFileView"""
        DownloadFileView.content_type = "content"
        DownloadFileView.filename = "file"
        DownloadFileView.extension = "docx"

        download_file = DownloadFileView()
        self.assertEqual(
            download_file.get_filename(), DownloadFileView.filename
        )
        self.assertEqual(
            download_file.get_extension(), DownloadFileView.extension
        )
        self.assertEqual(
            download_file.get_content_type(), DownloadFileView.content_type
        )

    @parameterized.expand(
        [
            ("", "", "", ValueError),
            ("", "url", "ext", ValueError),
            ("path", "", "ext", ValueError),
            ("path", "url", "", ValueError),
            (None, "url", "ext", TypeError),
            (1, 2, "ext", TypeError),
            ("path", 1.0, "ext", TypeError),
            ("path", True, "", TypeError),
        ]
    )
    def test_create_object_error(self, filename, content_type, extension, ex):
        """Тест ошибки при создании экземпляра класса CreateFileView"""
        with self.assertRaises(ex):
            DownloadFileView(
                filename=filename,
                extension=extension,
                content_type=content_type,
            )
