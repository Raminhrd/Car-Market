# permissions.py
from rest_framework.permissions import BasePermission
from django.utils import timezone
from datetime import timedelta


class IsOwnerAndEditable(BasePermission):

    def has_object_permission(self, request, view, obj):
        # safe methods allowed for everyone
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True

        if obj.owner != request.user:
            return False

        # DELETE always allowed for owner
        if request.method == "DELETE":
            return True

        # PATCH/PUT allowed only within 48h
        if request.method in ("PUT", "PATCH"):
            return obj.created_at >= timezone.now() - timedelta(hours=48)

        return False
