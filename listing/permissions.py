from rest_framework.permissions import BasePermission, SAFE_METHODS

from listing.models import Listing


class IsOwnerOrReadOnlyPublished(BasePermission):

    def has_object_permission(self, request, view, obj: Listing):
        if request.method in SAFE_METHODS:
            if obj.status == Listing.Status.PUBLISHED:
                return True
            return request.user.is_authenticated and obj.owner_id == request.user.id

        return request.user.is_authenticated and obj.owner_id == request.user.id
