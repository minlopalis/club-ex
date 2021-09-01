from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),

    path('account/<str:pk>', views.userAccount, name="user-account"),
    path('edit-account/', views.editAccount, name="edit-account"),

    path('subscription/new/', views.subscription_new, name="subscription-new"),
    path('subscription/success/', views.subscription_success, name="subscription-success"),
    path('edit-subscription/<str:pk>', views.edit_subscription, name="renew-subscription")
]

