from django.contrib import admin
from django.db.models import Count

from listing.models import Listing, ListingImage, ListingView


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 0
    fields = ("id", "image", "created_at")
    readonly_fields = ("id", "created_at")


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    inlines = [ListingImageInline]

    list_display = (
        "id",
        "title",
        "owner",
        "price",
        "city",
        "year",
        "mileage_km",
        "fuel",
        "gearbox",
        "views_count",
        "created_at",
    )
    list_select_related = ("owner",)
    list_filter = ("city", "year", "fuel", "gearbox", "created_at")
    search_fields = ("title", "city", "owner__phone_number", "owner__first_name", "owner__last_name")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"

    readonly_fields = ("created_at",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_views_count=Count("views"))

    @admin.display(description="Views", ordering="_views_count")
    def views_count(self, obj):
        return getattr(obj, "_views_count", 0)


@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "created_at")
    list_select_related = ("listing",)
    search_fields = ("listing__title", "listing__owner__phone_number")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)


@admin.register(ListingView)
class ListingViewAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "user", "created_at")
    list_select_related = ("listing", "user")
    list_filter = ("created_at",)
    search_fields = ("listing__title", "user__phone_number")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
