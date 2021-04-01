from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Book
from .forms import PostitForm


class BookCreate(CreateView):
  model = Book
  fields = '__all__'
  success_url = '/books'

class BookUpdate(UpdateView):
  model = Book
  fields = ['name', 'author', 'notetype', 'image']

  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.save()
    return HttpResponseRedirect('/books/' + str(self.object.pk))

class BookDelete(DeleteView):
    model = Book
    success_url = '/books'


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
    postit_form = PostitForm()
    return render(request, 'books/show.html', {
        'book': book, 'postit_form':postit_form
    })

def add_postit(request, book_id):
    form = PostitForm(request.POST)
    # validate the form
    if form.is_valid():
        new_postit = form.save(commit=False)
        new_postit.book_id = book_id
        new_postit.save()
    return redirect('books_show', book_id=book_id)
