from django.db import models

# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=120)
    author = models.CharField(max_length=120)
    notetype = models.CharField(max_length=120)
    image = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add =True)

    def __str__(self):
        return self.name