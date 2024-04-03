from django import forms
from django.utils import timezone


def check_date_intersection(date1, date2):
    return (date1[0] <= date2[0] <= date1[1]) or (
        date2[0] <= date1[0] <= date2[1]
    )


def check_date_range(date1, date2):
    if date2 and date2 <= date1:
        return False
    return True


def fill_date(date):
    if not date:
        return timezone.now()
    return date


def check_dates_intersection(cleaned_data, hospitalizations):
    leaving_date = fill_date(cleaned_data.get("leaving_date"))
    for hospitalization in hospitalizations:
        h_leaving_date = fill_date(hospitalization.leaving_date)

        if check_date_intersection(
            (hospitalization.entry_date, h_leaving_date),
            (cleaned_data["entry_date"], leaving_date),
        ):
            raise ValueError(
                "Для пациента уже существует госпитализация с {} по {}".format(
                    hospitalization.entry_date.strftime("%d.%m.%Y %H:%m"),
                    h_leaving_date.strftime("%d.%m.%Y %H:%m"),
                )
            )


def validate_hospitalization_fields(cleaned_data, hospitalizations):
    if not check_date_range(
        cleaned_data["entry_date"], cleaned_data["leaving_date"]
    ):
        raise forms.ValidationError(
            "Дата поступления не может быть больше даты выписки"
        )
    try:
        check_dates_intersection(cleaned_data, hospitalizations)
    except ValueError as e:
        raise forms.ValidationError(e)
