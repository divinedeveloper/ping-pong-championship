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
from api.views import player_registration , draw_games, referee_instructions, choose_roles_for_players #, play_match, judge_move_winner_and_player_type,  shutdown_defeated_players, export_report

urlpatterns = [

    url(r'^register-players/', player_registration, name='player_registration'),
    url(r'^draw-games/', draw_games, name='draw_games'),
    url(r'^instructions/', referee_instructions, name='referee_instructions'),
    url(r'^game/(\d+)/toss/', choose_roles_for_players, name='choose_roles_for_players'),

    # #there is some confusion regarding the following two
    # url(r'^start-match/', start_matches, name='start_matches'),
    # url(r'^play-match/', start_matches, name='play_match'),

    # url(r'^player-move/', get_player_move, name='get_player_move'),
    # url(r'^move-winner/', judge_move_winner_and_player_type, name='judge_move_winner_and_player_type'),
    # url(r'^shutdown-players/', shutdown_defeated_players, name='shutdown_defeated_players'),

    # url(r'^game-report/', export_report, name='export_report'),



]