from django import forms
# from .models import Accountant
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Position

class UserStaffForm(UserCreationForm):
    email = forms.EmailField()
    admin_status = forms.BooleanField(required=False)
    class meta:
        model = User
        fields = ['email','username','password1','password2','admin_status']
    def save(self, commit=True):
        user = super(UserStaffForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_staff = self.cleaned_data['admin_status']
        if commit:
            user.save()
        return user
    
class PositionForm(forms.ModelForm):
    class meta:
        model = Position
        fields = "__all__"
    
