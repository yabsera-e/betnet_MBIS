from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='listings'),
    path('my',views.my_listings,name='my_listings'),
    path('<int:id>',views.listing_retrieve,name='listing_retrieve'),
    path('create',views.listing_create,name='listing_create'),
    path('<int:id>/change-status',views.set_status, name='listing-change-status'),
    path('<int:id>/edit',views.listing_update,name='listing_update'),
    path('<int:id>/delete',views.listing_delete,name='listing_delete'),
]