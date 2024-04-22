<p align="center">
      <img src="https://i.ibb.co/DYdd64d/noun-hospital-1891627.png" alt="Project Logo" width="200">
</p>

<p align="center">
   <img src="https://img.shields.io/badge/Python-3.11-blue" alt="Python 3.11">
   <img src="https://img.shields.io/badge/Django-5.0-success" alt="Django Version">
   <img src="https://img.shields.io/badge/CRM-1.0-blue" alt="CRM Version">
   <img src="https://img.shields.io/badge/License-MIT-success" alt="License">
</p>

## About

Medical information system for automating the work of the medical department:

Opportunities: 
- Managing patient accounts 
- Management of hospitalizations 
- Work with medical documents

## Installation

1. Clone the repository
2. Create a `crm/.env` file (example - `crm/.env-example`)

> [!IMPORTANT]
> You need to change the superuser password `DJANGO_SUPERUSER_PASSWORD`


3. Copy the keys to `nginx/ssl/`
4. Edit `crm/crm/settings/base.py`, add the site address to `CSRF_TRUSTED_ORIGINS`:

```python
...
CSRF_TRUSTED_ORIGINS = ["https://nginx", "https://127.0.0.1", "https://mysite.com"]
...
```

5. Execute
```commandline
sudo docker-compose build && sudo docker-compose up -d
```

By default, the project is deployed with fake data.

## Demo

[link](https://91.236.198.62)

## Developers

- [sergei-kolchev](https://github.com/sergei-kolchev)

## License

The project is distributed under the MIT license.