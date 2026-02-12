from django.urls import path
from users import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView


router = DefaultRouter()
router.register("vendors", views.VendorViewSet, basename="vendors")


urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('signup/', views.SignUpView.as_view()),

    path('otp/request/', views.OTPRequestView.as_view()),
    path('otp/login/', views.OTPLoginView.as_view()),

    path('info/', views.UserInfoView.as_view()),
]

urlpatterns += router.urls