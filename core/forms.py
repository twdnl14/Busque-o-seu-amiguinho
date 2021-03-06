from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django import forms

from core.models import *
from django_select2.forms import Select2MultipleWidget
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    github = forms.URLField(
        label="Github (opcional)",
        widget=forms.TextInput(attrs={"placeholder": "Link do seu GitHub"}),
        required=False,
    )

    telegram_nick = forms.CharField(
        label="Telegram (opcional)",
        widget=forms.TextInput(attrs={"placeholder": "Nickname seu Telegram"}),
        required=False,
    )

    discord_nick = forms.CharField(
        label="Discord (opcional)",
        widget=forms.TextInput(attrs={"placeholder": "Nickname seu Discord"}),
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
                github=self.cleaned_data['github'],
                discord_nick=self.cleaned_data['discord_nick'],
                telegram_nick=self.cleaned_data['telegram_nick'],
                bio=self.cleaned_data['bio']
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
        fields = ("github", "telegram_nick", "discord_nick", "bio", "tags")
        widgets = {"tags": Select2MultipleWidget}


class CreateRoomForm(forms.ModelForm):
    group_name = forms.CharField(
        label="Nome do Grupo de estudos ou projeto",
        widget=forms.TextInput(attrs={"placeholder": "Nome do Grupo"}),
        required=False,
    )

    telegram_group = forms.CharField(
        label="Telegram (opcional)",
        widget=forms.TextInput(attrs={"placeholder": "Link do Telegram do Grupo"}),
        required=False,
    )

    discord_group = forms.URLField(
        label="Discord (opcional)",
        widget=forms.TextInput(attrs={"placeholder": "Link para o Discord do Grupo"}),
        required=False,
    )

    tags_group = forms.ModelMultipleChoiceField(
        label="Tags", queryset=Tag.objects.all(), widget=Select2MultipleWidget
    )

    limit_date = forms.CharField(
        widget=forms.HiddenInput()
    )

    group_users = forms.ModelMultipleChoiceField(
        label="Profile", queryset=Profile.objects.all(), widget=Select2MultipleWidget
    )

    class Meta:
        model = Profile
        fields = ("id",)
        widgets = {"id": Select2MultipleWidget}

    def __init__(self, *args, **kwargs):
        super(CreateRoomForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(CreateRoomForm, self).save(commit=False)

        if commit:
            instance.save()
            group = StudyRoom(
                users_group=self.cleaned_data['users_group'],
                group_name=self.cleaned_data['group_name'],
                discord_group=self.cleaned_data['discord_group'],
                telegram_group=self.cleaned_data['telegram_group'],
            )
            print(group)
            authenticate(
                username=instance.username
            )
            print(instance.username)
            group.save()
            group.tags_group.set(self.cleaned_data["tags_group"])
            group.save()
        return instance
