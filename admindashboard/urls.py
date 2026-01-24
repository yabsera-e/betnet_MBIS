from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('',  views.dashboard,  name='admin-dashboard' ),
    path('users',  views.get_users,  name='admin-users' ),
    path('users/<int:id>/action',  views.ban_unban_user,  name='admin-action'),
    path('listings',  views.get_listings,  name='admin-listings'),
    path('listings/<int:id>',  views.set_listing_status,  name='admin-listing-status'),
    path('ads',  views.create_add,  name='admin-ads'),
    path('ads/<int:id>',  views.set_ad_status,  name='admin-ads-status'),
    path('cities/add',  views.add_city,  name='admin-add-city'),
    path('cities',  views.get_cities,  name='admin-cities'),
    path('subcities/add',  views.add_subcity,  name='admin-add-subcity'),
    path('subcities',  views.get_subcitiies,  name='admin-subcities'),
    path('comments',  views.get_comments,  name='admin-comments'),
]
