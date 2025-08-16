from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Profile
from django.contrib.auth.forms import PasswordChangeForm


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'expertise']

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     if commit:
    #         user.save()
    #         Profile.objects.create(
    #             user=user,
    #             phone_number=self.cleaned_data.get('phone_number'),
    #             bio=self.cleaned_data.get('bio'),
    #         )
    #     return user


class CustomAuthenticationForm(AuthenticationForm):
    pass


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']


class ProfileForm(forms.ModelForm):
    department = forms.CharField(max_length=100, required=True)
    skills = forms.CharField(max_length=255, required=True)
    phone_number = forms.CharField(max_length=20, required=False)
    profile_picture = forms.ImageField(required=False)
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', 'department', 'skills', 'phone_number']



class PreferenceForm(forms.ModelForm):
    notifications_enabled = forms.BooleanField(required=False)

    class Meta:
        model = CustomUser
        fields = ['notifications_enabled', 'preference_field_1', 'preference_field_2']