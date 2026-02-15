from django.db.models import Q
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from datetime import timedelta, timezone

from .models import Listing, ListingView
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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        user = request.user if request.user.is_authenticated else None

        # Owner view shouldn't count
        if user != instance.owner:
            twenty_four_hours_ago = timezone.now() - timedelta(hours=24)

            already_viewed = ListingView.objects.filter(
                listing=instance,
                user=user,
                created_at__gte=twenty_four_hours_ago).exists()

            if not already_viewed:
                ListingView.objects.create(
                    listing=instance,
                    user=user)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

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
