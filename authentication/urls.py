from django.urls import path
from .views import RegisterView, LoginView, LogoutView, VerifyAccountView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify_acc/<int:verify_id>/', VerifyAccountView.as_view(), name='verify_acc'),
]