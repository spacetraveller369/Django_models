"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
import app.views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('news/', app.views.categories_list_view),
    path('news/category/<str:category_id>/', app.views.category_detail_view),
    path('news/item/<int:news_id>/', app.views.news_detail_view),
    
    path('news/create-event/', app.views.create_event_view, name='create_event'),
    path('news/event-detail/', app.views.event_detail_view, name='event_detail'),
    
    path('movies/', app.views.movies_list_view),
    path('movies/add/', app.views.add_movie_view),
    path('movies/<int:movie_id>/', app.views.movie_detail_view),
    path('movies/<int:movie_id>/edit/', app.views.edit_movie_view),
    path('movies/<int:movie_id>/delete/', app.views.delete_movie_view),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
