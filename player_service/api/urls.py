"""iec lookup URL Configuration 

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from api.views import login, defensive_move, offensive_move #, get_players, get_player_move, deactivate_player

urlpatterns = [
    url(r'^login/', login, name='login'),
    url(r'^offensive-move/', offensive_move, name='offensive_move'),
    url(r'^defensive-move/', defensive_move, name='defensive_move'),

    # url(r'^players/', get_players, name='get_players'),
    # url(r'^moves/', get_player_move, name='get_player_move'),
    # url(r'^shut-down/', deactivate_player, name='deactivate_player'),

]