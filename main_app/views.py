from django.shortcuts import render
from django.http import HttpResponse
from .models import Book

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')


def books_index(request):
    books = Book.objects.all()
    return render(request, 'books/index.html', {'books': books})

def books_show(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'books/show.html', {'book': book})