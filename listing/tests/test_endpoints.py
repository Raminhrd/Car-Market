import pytest
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken

from listing.models import Listing, ListingView

User = get_user_model()
pytestmark = pytest.mark.django_db


def auth_client(api_client, user):
    refresh = RefreshToken.for_user(user)
    api_client.cookies["accessToken"] = str(refresh.access_token)
    return api_client


def make_user(phone):
    return User.objects.create_user(phone_number=phone, password="x12345678")


def _default_value_for_field(field):
    
    if field.choices:
        for value, _ in field.choices:
            if value not in (None, ""):
                return value
            
    if isinstance(field, models.CharField):
        return "test"

    if isinstance(field, models.TextField):
        return "test"

    if isinstance(field, models.IntegerField):
        return 1

    if isinstance(field, models.PositiveIntegerField):
        return 1

    if isinstance(field, models.DecimalField):
        return 1000

    if isinstance(field, models.BooleanField):
        return True

    return None


def make_listing(owner, **kwargs):
    data = {"owner": owner}

    for field in Listing._meta.fields:
        if field.name in ("id", "owner"):
            continue

        if field.name in kwargs:
            continue

        if field.null:
            continue

        if field.has_default():
            continue

        if getattr(field, "auto_now", False) or getattr(field, "auto_now_add", False):
            continue

        if field.is_relation:
            continue

        data[field.name] = _default_value_for_field(field)

    data.update(kwargs)

    return Listing.objects.create(**data)



def extract_items(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and "results" in payload and isinstance(payload["results"], list):
        return payload["results"]
    return payload


class TestListingViewCounter:
    def test_owner_view_is_not_counted(self, api_client):
        owner = make_user("+989121111111")
        listing = make_listing(owner)

        client = auth_client(api_client, owner)
        res = client.get(reverse("listing-detail", kwargs={"pk": listing.id}))

        assert res.status_code == 200
        assert ListingView.objects.filter(listing=listing).count() == 0

    def test_authenticated_non_owner_view_is_counted_once(self, api_client):
        owner = make_user("+989121111111")
        viewer = make_user("+989122222222")
        listing = make_listing(owner)

        client = auth_client(api_client, viewer)

        res1 = client.get(reverse("listing-detail", kwargs={"pk": listing.id}))
        assert res1.status_code == 200
        assert ListingView.objects.filter(listing=listing, user=viewer).count() == 1

        res2 = client.get(reverse("listing-detail", kwargs={"pk": listing.id}))
        assert res2.status_code == 200
        assert ListingView.objects.filter(listing=listing, user=viewer).count() == 1

    def test_view_counts_again_after_24_hours(self, api_client):
        owner = make_user("+989121111111")
        viewer = make_user("+989122222222")
        listing = make_listing(owner)

        client = auth_client(api_client, viewer)

        res1 = client.get(reverse("listing-detail", kwargs={"pk": listing.id}))
        assert res1.status_code == 200
        assert ListingView.objects.filter(listing=listing, user=viewer).count() == 1

        lv = ListingView.objects.get(listing=listing, user=viewer)
        ListingView.objects.filter(id=lv.id).update(created_at=timezone.now() - timedelta(hours=25))

        res2 = client.get(reverse("listing-detail", kwargs={"pk": listing.id}))
        assert res2.status_code == 200
        assert ListingView.objects.filter(listing=listing, user=viewer).count() == 2

    def test_list_returns_views_count_from_annotate(self, api_client):
        owner = make_user("+989121111111")
        v1 = make_user("+989122222222")
        v2 = make_user("+989123333333")
        listing = make_listing(owner)

        ListingView.objects.create(listing=listing, user=v1)
        ListingView.objects.create(listing=listing, user=v2)

        res = api_client.get(reverse("listing-list"))
        assert res.status_code == 200

        items = extract_items(res.json())
        found = next(i for i in items if i["id"] == listing.id)

        assert found["views_count"] == 2

    
