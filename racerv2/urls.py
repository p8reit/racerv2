from django.urls import path
from . import views

app_name = 'racerv2'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('generate_links/', views.generate_links, name='generate_links'),
    path('track/<str:unique_id>.gif', views.track_embed, name='track'),  # Add this line
    path('hide-group/', views.hide_group, name='hide_group'),
]


