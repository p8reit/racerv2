from django.urls import path
from . import views

# Add this line to specify the app_name
app_name = 'embed_racing'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('generate_links/', views.generate_links, name='generate_links'),
    # Add other URLs as necessary
]

