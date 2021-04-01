from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required

from .models import Book
from .forms import PostitForm, BookForm


# class BookCreate(CreateView):
#   model = Book
#   fields = '__all__'
#   success_url = '/books'

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


# def books_index(request):
#     books = Book.objects.all()
#     return render(request, 'books/index.html', {'books': books})
@login_required
def books_index(request):
    # cats = Cat.objects.all()
    # we want to have access to the user request.user - only cats that belong to one user
    books = Book.objects.filter(user = request.user)
    return render(request, 'books/index.html', { 'books': books })


@login_required
def books_show(request, book_id):
    book = Book.objects.get(id=book_id)
    postit_form = PostitForm()
    return render(request, 'books/show.html', {
        'book': book, 'postit_form':postit_form
    })

@login_required
def books_new(request):
  # create new instance of cat form filled with submitted values or nothing
  book_form = BookForm(request.POST or None)
  # if the form was posted and valid
  if request.POST and book_form.is_valid():
    new_book = book_form.save(commit=False)
    new_book.user = request.user
    new_book.save()
    # redirect to index
    return redirect('index')
  else:
    # render the page with the new cat form
    return render(request, 'books/new.html', { 'book_form': book_form })


@login_required
def add_postit(request, book_id):
    form = PostitForm(request.POST)
    # validate the form
    if form.is_valid():
        new_postit = form.save(commit=False)
        new_postit.book_id = book_id
        new_postit.save()
    return redirect('books_show', book_id=book_id)

def sign_up(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A GET or a bad POST request, so render signup.html with an empty form
  #this will run after if it is not a POST or it is invalid
  form = UserCreationForm()
  return render(request, 'registration/signup.html', {
    'form': form, 
    'error_message': error_message
  })