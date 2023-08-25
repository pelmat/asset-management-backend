from rest_framework.filters import BaseFilterBackend
from rest_framework.exceptions import NotFound
from django.contrib.postgres.search import TrigramSimilarity


class FieldsFilter(BaseFilterBackend):
    """
    Endpoint model attribute based filtering.

    Examples:
    1) {endpoint}/?id=34
    1) {endpoint}/?name=system&product_owner=john
    3) {endpoint}/?count=10&ownership=test&classification=test

    Order of these parameters does not matter.
    """

    def filter_queryset(self, request, queryset, view):
        for field_name, value in request.GET.items():
            # Taking into consideration the default Django REST filter parameters:
            if field_name not in ('page', 'count', 'nested_max_count'):
                try:
                    queryset.model._meta.get_field(field_name)
                except Exception as e:
                    raise NotFound(
                        f"field filter error. {value} is not a valid value for {field_name} ({str(e)})"
                    )

                queryset = (
                    queryset.annotate(similarity=TrigramSimilarity(field_name, value))
                    .filter(similarity__gte=0.1)
                    .order_by('-similarity')
                )

        return queryset
