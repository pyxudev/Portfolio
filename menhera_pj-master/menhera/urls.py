from django.urls import path
from django.contrib import admin
from . import views
from django.urls import include

urlpatterns = [
	path('home', views.index_template, name='index_template'),
	path('goods/', views.goods_template, name='goods_template'),
	path('blogs/', views.blogs_template, name='blogss_template'),
	path('chat/', views.chat_template, name='chat_template'),
	path('future/', views.future_template, name='future_template'),
	path('timeline/', views.timeline_template, name='timeline_template'),
	path('test/', views.test_template, name='timeline_template'),
	path('admin/', admin.site.urls),
	path('', include('accounts.urls')),
]