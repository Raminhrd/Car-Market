from datetime import timedelta
from django.utils import timezone

from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import Listing, ListingView
from .filters import ListingFilter
from .serializers import ListingListSerializer, ListingDetailSerializer
from .permissions import IsOwnerAndEditable


class ListingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,):

    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerAndEditable]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ListingFilter
    ordering_fields = ["created_at", "price", "year", "views_count"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        return ListingListSerializer if self.action == "list" else ListingDetailSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return (
            Listing.objects
            .select_related("owner")
            .prefetch_related("images")
            .with_views_count()
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_authenticated and request.user != instance.owner:
            since = timezone.now() - timedelta(hours=24)

            already_viewed = ListingView.objects.filter(
                listing=instance,
                user=request.user,
                created_at__gte=since,
            ).exists()

            if not already_viewed:
                ListingView.objects.create(listing=instance, user=request.user)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
