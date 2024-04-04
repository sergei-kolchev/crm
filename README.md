<p align="center">
      <img src="https://i.ibb.co/DYdd64d/noun-hospital-1891627.png" alt="Project Logo" width="200">
</p>

<p align="center">
   <img src="https://img.shields.io/badge/Python-3.11-blue" alt="Python 3.11">
   <img src="https://img.shields.io/badge/Django-5.0-success" alt="Django Version">
   <img src="https://img.shields.io/badge/CRM-1.0-blue" alt="CRM Version">
   <img src="https://img.shields.io/badge/License-MIT-success" alt="License">
</p>

## О проекте

Медицинская CRM для автоматизации работы медицинского учреждения:

Возможности: 
- Управление учетными записями пациентов 
- Управление госпитализациями 
- Работа с медицинскими документами

## Установка

1. Клонировать репозиторий
2. Cоздать файл crm/.env по образцу crm/.env-example

> [!IMPORTANT]
> Необходимо изменить пароль суперпользователя DJANGO_SUPERUSER_PASSWORD


3. Скопировать ключи в nginx/ssl/
4. Отредактировать crm/crm/settings/base.py, добавить адрес сайта в CSRF_TRUSTED_ORIGINS:

```python
...
CSRF_TRUSTED_ORIGINS = ["https://nginx", "https://127.0.0.1", "https://mysite.com"]
...
```

5. Выполнить
```commandline
sudo docker-compose build && sudo docker-compose up -d
```

По умолчанию проект разворачивается с фейковыми данными.

## Демо-версия

[перейти](https://91.236.198.62)

## Разработчики

- [sergei-kolchev](https://github.com/sergei-kolchev)

## Лицензия

Проект распространяется под лицензией MIT license.