import django_filters
from listing.models import Listing


class ListingFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    year_min = django_filters.NumberFilter(field_name="year", lookup_expr="gte")
    year_max = django_filters.NumberFilter(field_name="year", lookup_expr="lte")
    mileage_min = django_filters.NumberFilter(field_name="mileage_km", lookup_expr="gte")
    mileage_max = django_filters.NumberFilter(field_name="mileage_km", lookup_expr="lte")

    class Meta:
        model = Listing
        fields = [
            "make",
            "model",
            "city",
            "fuel",
            "gearbox",
            "status",
        ]
