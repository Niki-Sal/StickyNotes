from django.db import models
from django.urls import reverse
from datetime import date
# Import the User
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=120)
    author = models.CharField(max_length=120)
    notetype = models.CharField(max_length=120)
    image = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add =True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Postit(models.Model):
    index = models.IntegerField()
    content = models.CharField(max_length=500)
    # create a book_id FK
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-index']


class Flashcard(models.Model):
    number = models.IntegerField()
    question = models.CharField(max_length=600)
    answer = models.CharField(max_length=600)
    # create a book_id FK
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.question
    