from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usern

class UsernCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Usern
        fields = ('email','name')

class UsernChangeForm(UserChangeForm):

    class Meta:
        model = Usern
        fields = UserChangeForm.Meta.fields