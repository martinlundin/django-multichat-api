from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import UsernCreationForm, UsernChangeForm
from .models import Usern

class UsernAdmin(UserAdmin):
    add_form = UsernCreationForm
    form = UsernChangeForm
    model = Usern
    list_display = ['email', 'name']

admin.site.register(Usern, UsernAdmin)