from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')


class Book:
    def __init__(self, name, author):
        self.name = name
        self.author = author
      

books = [
    Book('Lolo', 'lili'),
    Book('koko', 'kiki'),
    Book('momo', 'mimi')
]
def books_index(request):
    return render(request, 'books/index.html', {'books': books})