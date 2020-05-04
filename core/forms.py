from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django import forms

from core.models import Profile, Tag
from django_select2.forms import Select2MultipleWidget
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    github = forms.URLField(
        label="Github (opcional)",
        widget=forms.TextInput(attrs={"placeholder": "Link do seu GitHub"}),
        required=False,
    )

    tags_ = forms.ModelMultipleChoiceField(
        label="Tags", queryset=Tag.objects.all(), widget=Select2MultipleWidget
    )

    bio = forms.CharField(
        label="Sobre você",
        widget=forms.Textarea(attrs={"bio": "Diga algo sobre você."}),
        help_text="Descreva sobre você para os amiginhos poderem te conhecer melhor!!",
        required=False,
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username")

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ["password1", "password2"]:
            self.fields[fieldname].help_text = None

    def save(self, commit=True):
        instance = super(RegisterForm, self).save(commit=False)

        if commit:
            instance.save()

            profile = Profile(
                user=instance,
                github=self.cleaned_data["github"],
                bio=self.cleaned_data["bio"],
            )
            authenticate(
                username=instance.username, password=self.cleaned_data.get("password1")
            )
            profile.save()
            profile.tags.set(self.cleaned_data["tags_"])
            profile.save()
        return instance


class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = {
        **SetPasswordForm.error_messages,
        'password_incorrect': "Your old password was entered incorrectly. Please enter it again.",
    }
    old_password = forms.CharField(
        label="Old password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True}),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("github", "tags")
        widgets = {"tags": Select2MultipleWidget}


class RegisterRoom(forms.ModelForm):
    group_name = forms.CharField(
        label="Nome do Grupo de estudo ou do Projeto",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'required': "required"})
    )

    telegram_link = forms.URLField(
        label="Telegram Invite (opcional)",
        widget=forms.TextInput(attrs={"placeholder": "Se houver um grupo no telegram para este grupo, link aqui."}),
        required=False
    )

    discord_link = forms.URLField(
        label="Discord link (opcional)",
        widget=forms.TextInput(attrs={"placeholder": "Se houver um discord para este grupo, link aqui."}),
        required=False
    )

    tags_ = forms.ModelMultipleChoiceField(
        label="Tags", queryset=Tag.objects.all(), widget=Select2MultipleWidget
    )

    '''
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username")
        
   
    def __init__(self, *args, **kwargs):
        super(RegisterRoom, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(RegisterRoom, self).save(commit=False)

        if commit:
            instance.save()

            profile = Profile(
                user=instance,
                github=self.cleaned_data["github"],
            )
            authenticate(
                username=instance.username, password=self.cleaned_data.get("password1")
            )
            profile.save()
            profile.tags.set(self.cleaned_data["tags_"])
            profile.save()
        return instance'''
