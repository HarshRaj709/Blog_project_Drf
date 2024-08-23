from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.StudentRegister.as_view(),name='register'),
    path('login1/',views.StudentLogin.as_view(),name='login'),
    path('login2/',views.Studentloginusingtoken.as_view(),name='login2'),
]
