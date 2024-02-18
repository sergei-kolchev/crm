import random
import warnings
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.db.models import Q
from faker import Faker

from hospitalizations.models import Diagnosis, Hospitalization
from patients.models import Patient

warnings.filterwarnings("ignore")
fake = Faker("RU-ru")


def get_dates(year=None):
    if not year:
        year = random.choice([2020, 2021, 2022])
    entry_date = datetime(
        year=year,
        month=random.randint(1, 12),
        day=random.randint(1, 28),
        hour=random.randint(1, 23),
        minute=random.randint(0, 59),
    )
    leaving_date = entry_date + timedelta(days=random.randint(10, 99))

    return entry_date, leaving_date


def check(date1, date2):
    return (date1[0] <= date2[0] <= date1[1]) or (
        date2[0] <= date1[0] <= date2[1]
    )


def get_dates_list():
    years = [2019, 2020, 2021, 2022, 2023]
    res = []
    for year in years:
        entry_date, leaving_date = get_dates(year=year)
        if leaving_date > datetime.now():
            break
        res.append((entry_date, leaving_date))

    r = []
    for i in range(1, len(res)):
        for j in range(i, len(res)):
            if check(res[i - 1], res[j]):
                break
        else:
            r.append(res[i])
    return r


fios = set(
    f"{fake.last_name_female()} {fake.first_name_female()} "
    f"{fake.middle_name_female()}"
    for n in range(1000)
)

diagnosis = Diagnosis.objects.all()

for fio in fios:
    data = fio.split()
    if len(data) == 3:
        p = Patient(
            name=data[1],
            patronymic=data[2],
            surname=data[0],
            birthday=fake.date_of_birth(minimum_age=18, maximum_age=70),
            registration_address=fake.address(),
            residential_address=fake.address(),
            active=True,
        )
        p.save()
        doctors = get_user_model().objects.filter(~Q(username="root"))

        dates = get_dates_list()

        for date in dates:
            h = Hospitalization(
                entry_date=date[0],
                leaving_date=date[1],
                patient=p,
                doctor=random.choice(doctors),
                diagnosis=random.choice(diagnosis),
                number=random.randint(1, 99999),
            )
            h.save()
