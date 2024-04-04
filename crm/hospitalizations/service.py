from django.contrib.auth import get_user_model
from django.db.models import CharField, F, Func, Q, TextField, Value
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404

from hospitalizations.models import Hospitalization


def _get_order(queryset, **kwargs):
    if "order" in kwargs and "direction" in kwargs:
        if kwargs["order"] == "surname":
            order = "patient__" + kwargs["order"]
        else:
            order = kwargs["order"]
        if kwargs["direction"] == "desc":
            order = f"-{order}"
        return queryset.order_by(order)
    return queryset


def get_all(patient_pk=None, **kwargs):
    queryset = Hospitalization.objects
    if patient_pk:
        queryset = queryset.filter(patient__pk=patient_pk)
    queryset = _get_order(queryset, **kwargs)
    return queryset.select_related("patient")


def get_all_current(selected_doctor=0, **kwargs):
    queryset = Hospitalization.current
    if selected_doctor:
        queryset = queryset.filter(doctor__pk=selected_doctor)
    queryset = _get_order(queryset, **kwargs)
    return queryset.select_related("patient")


def get_one(pk):
    return get_object_or_404(Hospitalization, pk=pk)


def get(pk):
    return Hospitalization.objects.filter(pk=pk)


class FileContent:
    @staticmethod
    def get_current_by_doctors():
        queryset = get_user_model().objects.filter(
            Q(hospitalizations__leaving_date=None)
        )
        queryset = (
            queryset.annotate(
                doctor=Concat(
                    "last_name",
                    Value(" "),
                    "first_name",
                    Value(" "),
                    "patronymic",
                    output_field=CharField(),
                )
            )
            .annotate(
                patient=Concat(
                    "hospitalizations__patient__surname",
                    Value(" "),
                    "hospitalizations__patient__name",
                    Value(" "),
                    "hospitalizations__patient__patronymic",
                )
            )
            .values_list("doctor", "patient", "hospitalizations__entry_date")
            .order_by(
                "last_name",
                "hospitalizations__patient__surname",
                "hospitalizations__patient__name",
                "hospitalizations__patient__patronymic",
            )
        )
        data = {}
        for row in queryset:
            data.setdefault(row[0], [])
            data[row[0]].append(row[1:])
        return data

    @staticmethod
    def get_current(selected_doctor, **kwargs):
        if selected_doctor:
            queryset = Hospitalization.current.filter(
                doctor__pk=selected_doctor
            )
        else:
            queryset = Hospitalization.current
        queryset = _get_order(queryset, **kwargs)
        return {
            "tbl_contents": list(
                queryset.annotate(
                    formatted_entry_date=Func(
                        F("entry_date"),
                        Value("DD.MM.YYYY"),
                        function="TO_CHAR",
                        output_field=TextField(),
                    )
                )
                .annotate(
                    formatted_birthday=Func(
                        F("patient__birthday"),
                        Value("DD.MM.YYYY"),
                        function="TO_CHAR",
                        output_field=TextField(),
                    )
                )
                .annotate(
                    doctor_fio=Concat(
                        "doctor__last_name",
                        Value(" "),
                        "doctor__first_name",
                        Value(" "),
                        "doctor__patronymic",
                        output_field=CharField(),
                    )
                )
                .annotate(
                    patient_fio=Concat(
                        "patient__surname",
                        Value(" "),
                        "patient__name",
                        Value(" "),
                        "patient__patronymic",
                    )
                )
                .values_list(
                    "patient_fio",
                    "formatted_birthday",
                    "formatted_entry_date",
                    "doctor_fio",
                )
            )
        }
