from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Car Market API",
      default_version='v1',
      description="API documentation for the Car Market Place Backend",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="monkey@monkeybusiness.com"),
      license=openapi.License(name="fake monkey"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)