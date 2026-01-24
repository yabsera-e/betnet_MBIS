from django.urls import path
from .views import login_view, register, logout_view, home_view, profile_update_view, get_landing

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup', register,name='register'),
    path('logout', logout_view,name='logout'),
    path('home', home_view,name='home'),
    path('', get_landing,name='landing'),
    path('profile/update',profile_update_view,name='profile_update_view')
]