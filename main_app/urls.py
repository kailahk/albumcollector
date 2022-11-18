from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('albums/', views.albums_index, name='index'),
    path('albums/<int:album_id>/', views.albums_detail, name='detail'),
    path('albums/create/', views.CreateAlbum.as_view(), name='create_album'),
    path('albums/<int:pk>/update/', views.UpdateAlbum.as_view(), name='update_album'),
    path('albums/<int:pk>/delete/', views.DeleteAlbum.as_view(), name='delete_album'),
    path('albums/<int:album_id>/add_listen/', views.add_listen, name='add_listen'),
    path('albums/<int:album_id>/assoc_list/<int:list_id>/', views.assoc_list, name='assoc_list'),
    path('albums/<int:album_id>/remove_list/<int:list_id>/', views.remove_list, name='remove_list'),
    path('lists/', views.ListList.as_view(), name='lists_index'),
    path('lists/<int:pk>/', views.ListDetail.as_view(), name='lists_detail'),
    path('lists/create/', views.ListCreate.as_view(), name='lists_create'),
    path('lists/<int:pk>/update/', views.ListUpdate.as_view(), name='lists_update'),
    path('lists/<int:pk>/delete/', views.ListDelete.as_view(), name='lists_delete'),
]