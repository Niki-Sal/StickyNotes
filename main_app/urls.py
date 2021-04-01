from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('books/', views.books_index, name='books_index'),
    path('books/<int:book_id>/', views.books_show, name='books_show'),
    path('books/create/', views.BookCreate.as_view(), name='books_create'),
    path('books/<int:pk>/update/', views.BookUpdate.as_view(), name='books_update'),
    path('books/<int:pk>/delete/', views.BookDelete.as_view(), name='books_delete')
]