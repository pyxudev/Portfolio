from django.urls import include, path, re_path
from . import views
# from .subviews import youtube_views

app_name = 'dashboard'

urlpatterns = [
    #webage
    path('home/', views.index, name='index'),
    #js functions
    # path('start/', views.start, name='start'),
    path('download/', views.download, name='download'), # GET
    path('new_request/', views.request_scraping, name='new_request'), # POST
    path('cancel_request/', views.stop, name='cancel_request'), # POST
    path('update_status/', views.update_status, name='update_status'), # POST
    path('see_logs/', views.see_logs, name='see_logs'), # GET
    path('change_password/', views.change_password, name='change_password'), # POST
    path('update_database/', views.update_database, name='update_database') # POST
]
