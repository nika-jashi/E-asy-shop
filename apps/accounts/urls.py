from django.urls import path
from apps.accounts.views import AccountRegistrationView

urlpatterns = [
    path('registration/', AccountRegistrationView.as_view(), name='registration'),
]