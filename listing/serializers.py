from rest_framework import serializers
from .models import Listing, ListingImage


class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ("id", "image")


class ListingListSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.full_name", read_only=True)
    main_image = serializers.ImageField(source="main_image_file", read_only=True)
    views_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Listing
        fields = (
            "id",
            "title",
            "price",
            "city",
            "year",
            "mileage_km",
            "fuel",
            "gearbox",
            "main_image",
            "owner_name",
            "views_count",
            "created_at",
        )
        

class ListingDetailSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.full_name", read_only=True)
    listing_main_image = serializers.ImageField(source="main_image_file",read_only=True)
    views_count = serializers.IntegerField(read_only=True)
    images = ListingImageSerializer(many=True, read_only=True)

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
            "mileage_km",
            "fuel",
            "gearbox",
            "city",
            "listing_main_image",
            "images",
            "owner",
            "owner_name",
            "views_count",
            "created_at",
        )
        read_only_fields = ("owner", "created_at")

