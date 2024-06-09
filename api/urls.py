from django.urls import path
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView

from . import views

app_name = 'api'

urlpatterns =[
    # Authentication route
    path("auth/register/", RegisterView.as_view(), name="rest_register"),
    path("auth/login/", LoginView.as_view(), name="rest_login"),
    path("auth/logout/", LogoutView.as_view(), name="rest_logout"),
    path("auth/user/", UserDetailsView.as_view(), name="rest_user_details"),

    # wallets ENDPOINT
    path("wallets/", views.WalletList.as_view()),
    path("wallets/<str:uid>/", views.WalletDetail.as_view()),

    # campaigns ENDPOINT
    path("campaigns/", views.CampaignList.as_view()),
    path("campaigns/<str:uid>/", views.CampaignDetail.as_view()),

    # transactions ENDPOINT
    path("transactions/",  views.TransactionList.as_view()),
    path("transactions/<str:uid>/", views.TransactionDetail.as_view()),

]