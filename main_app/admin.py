from django.contrib import admin

# Register your models here.
from django.contrib import admin
# Register your models here.
from .models import Book, Postit, Flashcard

# Register your models here
admin.site.register(Book)
admin.site.register(Postit)
admin.site.register(Flashcard)