"""abcd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from login import views
from django.contrib.auth.views import LoginView,LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.loginPage),
    path('', views.home,name='home'),
    path('main/',views.mainPage),
    path('register/',views.RegisterPage),
    path('contactus/',views.contactUs),
    path('profile/',views.profilePage),
    path('logout/', views.logOutPage),
    path('session/',views.userPage),
    path('meet/',views.curSession),
    path('new/',views.newSession,name='new'),
    path('test',views.test,name='test')
]

