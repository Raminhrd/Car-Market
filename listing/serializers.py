from rest_framework import serializers
from .models import Listing


class ListingListSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.full_name", read_only=True)
    main_image = serializers.ImageField(source="main_image_file", read_only=True)
    views_count = serializers.IntegerField(source="views.count", read_only=True)

    class Meta:
        model = Listing
        fields = (
            "id",
            "title",
            "price",
            "city",
            "year",
            "mileage",
            "main_image",
            "owner_name",
            "created_at",
            "views_count",
        )

class ListingDetailSerializer(serializers.ModelSerializer):
    views_count = serializers.IntegerField(source="views.count", read_only=True)
    owner_name = serializers.CharField(source="owner.full_name", read_only=True)
    listing_main_image = serializers.ImageField(source="main_image_file", read_only=True)
    images = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = (
            "id",
            "title",
            "description",
            "price",
            "brand",
            "model",
            "year",
            "mileage",
            "city",
            "images",
            "owner",
            "owner_name",
            "created_at",
            "views_count",
        )
        read_only_fields = ("owner", "created_at")
