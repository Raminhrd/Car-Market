from django.db.models import Q
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Listing
from .serializers import ListingListSerializer, ListingDetailSerializer
from .permissions import IsOwnerAndEditable


class ListingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
    ):
    
    queryset = (
        Listing.objects
        .select_related("owner")
        .prefetch_related("images")
        .order_by("-created_at")
    )

    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerAndEditable]

    def get_serializer_class(self):
        if self.action == "list":
            return ListingListSerializer
        return ListingDetailSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        brand = params.get("brand")
        city = params.get("city")
        min_price = params.get("min_price")
        max_price = params.get("max_price")
        min_year = params.get("min_year")
        max_year = params.get("max_year")

        if brand:
            qs = qs.filter(brand__icontains=brand)

        if city:
            qs = qs.filter(city__icontains=city)

        if min_price:
            qs = qs.filter(price__gte=min_price)

        if max_price:
            qs = qs.filter(price__lte=max_price)

        if min_year:
            qs = qs.filter(year__gte=min_year)

        if max_year:
            qs = qs.filter(year__lte=max_year)

        return qs
