from django.urls import path
from . import views
app_name = 'prevention_theft'
urlpatterns = [
    path('', views.main, name='main'),
    path('start/', views.start, name='start'),
    path('stealed_list/', views.stealed_list, name='stealed_list'),

    
]