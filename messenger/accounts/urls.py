from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.UserFormView.as_view(), name='accounts'),
    path('my_friends/', views.My_Friends.as_view(), name='my_friends'),
    path('home/', views.home, name='home'),
    path('show_user/', views.show_user, name='show_user'),
    path('messages/', views.PostView.as_view(), name='my_messages'),
    path('', views.logout_user, name='logout_user'),
    path('change_password/', views.change_password, name='change_password'),
    path('connect/<slug:operation>/<int:id>', views.change_friends, name='change_friends')
]
