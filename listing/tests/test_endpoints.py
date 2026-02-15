import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
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


def make_listing(owner, **kwargs):
    # اینجا باید فیلدهای required مدل خودت رو پر کنی
    # چون گفتی fuel/gearbox/mileage_km NOT NULL هستن:
    data = dict(
        owner=owner,
        title="Test",
        price=1000000,
        city="Tehran",
        year=2020,
        mileage_km=1000,
        fuel=1,      # مطابق choices خودت
        gearbox=1,   # مطابق choices خودت
    )
    data.update(kwargs)
    return Listing.objects.create(**data)


class TestListingViewCounter:
    def test_owner_view_is_not_counted(self, api_client):
        owner = make_user("+989121111111")
        listing = make_listing(owner)

        client = auth_client(api_client, owner)
        res = client.get(reverse("listing-detail", kwargs={"pk": listing.id}))
        assert res.status_code == 200

        assert ListingView.objects.filter(listing=listing).count() == 0

    def test_authenticated_non_owner_view_is_counted(self, api_client):
        owner = make_user("+989121111111")
        viewer = make_user("+989122222222")
        listing = make_listing(owner)

        client = auth_client(api_client, viewer)

        res = client.get(reverse("listing-detail", kwargs={"pk": listing.id}))
        assert res.status_code == 200

        assert ListingView.objects.filter(listing=listing, user=viewer).count() == 1

    def test_list_returns_views_count_from_annotate(self, api_client):
        owner = make_user("+989121111111")
        viewer = make_user("+989122222222")
        listing = make_listing(owner)

        ListingView.objects.create(listing=listing, user=viewer)
        ListingView.objects.create(listing=listing, user=viewer)

        res = api_client.get(reverse("listing-list"))
        assert res.status_code == 200

        data = res.json()
        items = data["results"] if isinstance(data, dict) and "results" in data else data
        row = next(i for i in items if i["id"] == listing.id)

        assert row["views_count"] == 2
