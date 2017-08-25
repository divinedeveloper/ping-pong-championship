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
from api.views import player_registration , draw_games, referee_instructions, choose_roles_for_players, start_game, shutdown_loosers, export_game_report

urlpatterns = [

    url(r'^register-players/', player_registration, name='player_registration'),
    url(r'^draw-games/', draw_games, name='draw_games'),
    url(r'^instructions/', referee_instructions, name='referee_instructions'),
    url(r'^toss/', choose_roles_for_players, name='choose_roles_for_players'),
    url(r'^start-game/', start_game, name='start_game'),
    url(r'^shutdown-loosers/', shutdown_loosers, name='shutdown_loosers'),
    url(r'^championship/(\d+)/game-report/', export_game_report, name='export_game_report'),

]