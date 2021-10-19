from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext_lazy
from django.contrib.auth import get_user_model
from dashboard.models import User_dashboard
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError
User = get_user_model()
allowed_domain = ["@****","@****","@****"]


#Login
class LoginForm(AuthenticationForm):
    def clean_username(self):
        username = self.data['username']
        try:
            username = User.objects.get(email=username).username
        except ObjectDoesNotExist:
            raise ValidationError(gettext_lazy("Please enter the correct Email address."))
        return username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label=gettext_lazy('Email')
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

# Signup
class SignupForm(UserCreationForm):
    last_name = forms.CharField(label=gettext_lazy("Last Name"))
    first_name = forms.CharField(label=gettext_lazy("First Name"))
    username = forms.CharField(label=gettext_lazy("Username"))
    email = forms.EmailField(label="Email")

    def clean_email(self):
        data = self.cleaned_data['email']
        count = 0
        for domain in allowed_domain:
            if domain not in data:   # any check you need
                count+=1
        if count==len(allowed_domain):
            raise forms.ValidationError(gettext_lazy("Incorrect email address"))
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError(gettext_lazy("Email already exists"))
        return data

    class Meta:
        model = User
        fields = ('email', 'last_name', 'first_name', 'username')
        unique = ['username','email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username')
        for field in self.fields.values():
            # print(field)
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(False)
        current_domain = ""
        for domain in allowed_domain:
            if domain in user.email:
                current_domain = domain
                break
        user.username = user.email[:-(len(current_domain))]
        user = super().save()

        return user

# PasswordReset
class PasswordResetForm(PasswordResetForm):
    """パスワード忘れたときのフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class PasswordResetConfirmForm(SetPasswordForm):
    """パスワード再設定用フォーム(パスワード忘れて再設定)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class ProfileForm(forms.ModelForm):
    last_name = forms.CharField(label=gettext_lazy("Last Name"))
    first_name = forms.CharField(label=gettext_lazy("First Name"))
    username = forms.CharField(label=gettext_lazy("Username"))
    email = forms.EmailField(label=gettext_lazy("Email"))

    def clean_email(self):
        data = self.cleaned_data['email']
        count = 0
        for domain in allowed_domain:
            if domain not in data:   # any check you need
                count+=1
        if count==len(allowed_domain):
            raise forms.ValidationError(gettext_lazy("Incorrect email address"))
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError(gettext_lazy("Email already exists"))
        return data

    class Meta:
        model = User
        fields = {'last_name','first_name','username','email'}
        unique = ['username','email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly']=True
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
