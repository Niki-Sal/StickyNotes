from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('books/', views.books_index, name='books'),
    path('books/<int:book_id>/', views.books_show, name='books_show'),
    path('books/create/', views.books_new, name='books_create'),
    path('books/<int:pk>/update/', views.BookUpdate.as_view(), name='books_update'),
    path('books/<int:pk>/delete/', views.BookDelete.as_view(), name='books_delete'),
    path('postit/<int:pk>/update-postit/', views.PostitUpdate.as_view(), name='postit_update'),
    path('postit/<int:pk>/delete-postit/', views.PostitDelete.as_view(), name='postit_delete'),
    path('books/<int:book_id>/add_postit/', views.add_postit, name='add_postit'),
    path('books/<int:book_id>/add_flashcard/', views.add_flashcard, name='add_flashcard'),
    path('books/<int:book_id>/add_photo/', views.add_photo, name='add_photo'),
    path('accounts/signup', views.sign_up, name='sign_up')
]