from django.urls import include, path, re_path

from . import views

app_name = 'tool'

urlpatterns = [
    path('home/', views.index, name='index'),
    path('input/', views.input, name='input'),
    path('entry/', views.entry, name='entry'),
    path('domain/', views.domain, name='domain'),
    path('webscan/<domain>/', views.webscan, name='webscan'),
    # path('webscan/', views.webscan, name='webscan'),
    path('view_web/', views.view_web, name='view_web'),
]



# from django.urls import include, path, re_path
# from . import views
# from .subviews import youtube_views
# app_name = 'dashboard'

# urlpatterns = [
#     path('home/', views.index, name='index'),
#     path('twitter/home/', views.twitter_home, name='twitter_home'),
#     path('twitter/daily/', views.twitter_daily, name='twitter_daily'),
#     path('youtube/home/', youtube_views.home, name='youtube_home'),
#     path('youtube/daily/', youtube_views.daily, name='youtube_daily'),
#     path('email/', views.send_email_view, name='email'),
#     re_path(r'^.*\.html', views.generate_html, name='generate_html'),
# ]