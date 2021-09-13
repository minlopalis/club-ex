from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    
    path('view/', views.view_account, name="view-account"),
    path('edit/<str:pk>', views.AccountUpdateView.as_view(), name="edit-account"),

    path('customer/new/', views.customer_new, name="customer-new"),

    #path('contact/', views.contact_us, name="contact-us"),
    path("contact", views.contact, name="contact"),

    path('subscription/new/', views.subscription_new, name="subscription-new"),
    path('subscription/success/', views.subscription_success, name="subscription-success"),
    path('edit-subscription/<str:pk>', views.edit_subscription, name="renew-subscription"),
    path('subscription/cancel/', views.cancel_subscription, name="cancel-subscription")
]

