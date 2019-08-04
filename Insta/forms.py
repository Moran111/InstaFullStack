from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from Insta.models import InstaUser

# forms defined here handles user inputs
# create a customer user createion form, inhertitce user creation form
class CustomUserCreationForm(UserCreationForm):
    # what meta data should be used, each form should mapping to a model
    # what field should in this form? 
    class Meta(UserCreationForm.Meta):
        model = InstaUser
        fields = ('username', 'email', 'profile_pic')
