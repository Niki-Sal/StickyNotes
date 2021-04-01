from django import forms
from .models import Postit

class PostitForm(forms.ModelForm):
  class Meta:
    model = Postit
    fields = ['index', 'content']