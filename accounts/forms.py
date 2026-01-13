from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


# password is required by default
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("username", "email", "age")


# Can't change password, reasonably
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "age")
