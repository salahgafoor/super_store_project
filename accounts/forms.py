from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("email", "name", "password1")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "Email"
        #del self.fields['password2']