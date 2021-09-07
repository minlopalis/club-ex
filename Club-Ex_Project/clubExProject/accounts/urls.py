from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    
    path('view/', views.view_account, name="view-account"),
    path('edit/', views.editAccount, name="edit-account"),

    path('customer/new/', views.customer_new, name="customer-new"),

    path('subscription/new/', views.subscription_new, name="subscription-new"),
    path('subscription/success/', views.subscription_success, name="subscription-success"),
    path('edit-subscription/<str:pk>', views.edit_subscription, name="renew-subscription")
]

