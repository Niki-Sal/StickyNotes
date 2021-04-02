from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Book, Postit, Photo
from .forms import PostitForm, BookForm, FlashcardForm
import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-2.amazonaws.com/'
BUCKET = 'flashnotes'


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

############################
class PostitUpdate(UpdateView):
  model = Postit
  fields = ['index', 'content']

  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.save()
   
    return HttpResponseRedirect('/books/'+ str(self.object.book.pk))

class PostitDelete(DeleteView):
    model = Postit
    
    def form_valid(self, form):
      self.object = form.save(commit=False)
      self.object.save()
    success_url = '/books'
    
###########################

# Create your views here.
def index(request):
    allbooks = Book.objects.all()
    return render(request, 'index.html',{'allbooks': allbooks })

def about(request):
    return render(request, 'about.html')


# def books_index(request):
#     books = Book.objects.all()
#     return render(request, 'books/index.html', {'books': books})


@login_required
def books_index(request):
    books = Book.objects.filter(user = request.user)
    return render(request, 'books/index.html', { 'books': books })


@login_required
def books_show(request, book_id):
    book = Book.objects.get(id=book_id)
    postit_form = PostitForm()
    flashcard_form = FlashcardForm()
    return render(request, 'books/show.html', {
        'book': book, 
        'postit_form':postit_form,
        'flashcard_form':flashcard_form
    })

@login_required
def books_new(request):
  book_form = BookForm(request.POST or None)

  if request.POST and book_form.is_valid():
    new_book = book_form.save(commit=False)
    new_book.user = request.user
    new_book.save()
    return redirect('index')
  else:
    return render(request, 'books/new.html', { 'book_form': book_form })


@login_required
def add_postit(request, book_id):
    form = PostitForm(request.POST)

    if form.is_valid():
        new_postit = form.save(commit=False)
        new_postit.book_id = book_id
        new_postit.save()
    return redirect('books_show', book_id=book_id)

@login_required
def add_flashcard(request, book_id):
    form = FlashcardForm(request.POST)

    if form.is_valid():
        new_flashcard = form.save(commit=False)
        new_flashcard.book_id = book_id
        new_flashcard.save()
    return redirect('books_show', book_id=book_id)

def sign_up(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'

  form = UserCreationForm()
  return render(request, 'registration/signup.html', {
    'form': form, 
    'error_message': error_message
  })

def add_photo(request, book_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a book object)
            photo = Photo(url=url, book_id=book_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('books_show', book_id=book_id)