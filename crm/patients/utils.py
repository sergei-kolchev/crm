from django.db.models import Q


def get_filtering_query(q: str) -> list:
    words_list = q.strip().split()[:3]
    filters = {
        0: lambda x: Q(surname__istartswith=x),
        1: lambda x: Q(name__istartswith=x),
        2: lambda x: Q(patronymic__istartswith=x),
    }
    return [filters[i](words_list[i]) for i in range(len(words_list))]
