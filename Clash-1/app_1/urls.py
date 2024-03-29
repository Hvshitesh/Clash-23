"""clash_rc_1 URL Configuration

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
from . import views
urlpatterns = [
    path('wadhivv/', admin.site.urls),
    path('', views.home, name='home'),
    path('questions/', views.questions, name='questions'),
    path('lifelineActivation/', views.lifelineActivation, name='lifelineActivation'),
    path('quiz-submit/', views.submit, name='submit'),
    path('result/', views.result, name='result'),
    path('LogoutClicked/', views.LogoutClicked, name='LogoutClicked'),
    path('signin/', views.signin, name='signin'),
    path('prasadsignup686/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('getJSLeaderboard/', views.getJSLeaderboard, name='getJSLeaderboard'),
    path('windowBlurError/', views.windowBlurError, name='windowBlurError'),
    path('webadmin/', views.webadmin, name='webadmin'),
    # path('getip', views.ipaddress, name='ipaddress'),
    
] 
 
 
