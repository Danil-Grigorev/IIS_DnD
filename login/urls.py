from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='sign_up'),
    # path('login/', views.Login.as_view(), name='login')
]