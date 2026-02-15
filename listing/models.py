from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models import Count
from django.db.models.functions import Coalesce


class ListingQuerySet(models.QuerySet):
    def with_views_count(self):
        return self.annotate(
            views_count=Coalesce(Count("views"), 0)
        )

class Listing(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 1, "Draft"
        PUBLISHED = 2, "Published"
        SOLD = 3, "Sold"
        ARCHIVED = 4, "Archived"

    class Fuel(models.IntegerChoices):
        GASOLINE = 1, "Gasoline"
        DIESEL = 2, "Diesel"
        HYBRID = 3, "Hybrid"
        ELECTRIC = 4, "Electric"
        CNG = 5, "CNG"

    class Gearbox(models.IntegerChoices):
        MANUAL = 1, "Manual"
        AUTOMATIC = 2, "Automatic"

    # --- Ownership
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listings",
        db_index=True,
    )

    make = models.CharField(max_length=40)
    model = models.CharField(max_length=60)
    trim = models.CharField(max_length=80, blank=True, default="")

    year = models.PositiveSmallIntegerField()
    mileage_km = models.PositiveIntegerField()

    fuel = models.IntegerField(choices=Fuel.choices)
    gearbox = models.IntegerField(choices=Gearbox.choices)

    color = models.CharField(max_length=30, blank=True, default="")
    body_style = models.CharField(max_length=30, blank=True, default="")

    # --- Pricing
    price = models.BigIntegerField(default=0)
    is_price_negotiable = models.BooleanField(default=True)

    # --- Location
    city = models.CharField(max_length=50)
    area = models.CharField(max_length=80, blank=True, default="")

    # --- Content
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, default="")
    status = models.IntegerField(choices=Status.choices, default=Status.DRAFT)

    # soft fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    objects = ListingQuerySet.as_manager()

    def __str__(self):
        return f"{self.make} {self.model} {self.year} - {self.price}"
    
    @property
    def main_image(self):
        return self.images.order_by("id").first()
        
    @property
    def main_image_file(self):
        return getattr(self.main_image, "image", None)
    
    def __str__(self):
        return f"{self.name}"


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="listings/images/")
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image#{self.id} for Listing#{self.listing_id}"


class ListingPriceHistory(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="price_history")
    price = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class ListingView(models.Model):
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="views")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)