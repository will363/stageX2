from django import forms
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Utilisateur, Role, Action, Document


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie')
    search_fields = ('nom', 'categorie')
    ordering = ('nom', 'categorie')
    list_filter = ('nom', 'categorie')


class UserCreationForm(forms.ModelForm):
    # formulaire creant de nouveaux utilisateurs . inluant tous les champs , plus les mots de passe repetes
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Utilisateur
        fields = ['email', 'nom', 'prenom', 'image', 'role', 'date_creation']

    def clean_password2(self):
        # verifie que les 2 entrees matchent
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("les mots de passes ne correxpondent pas")
        return password2

    def save(self, commit=True):
        # enregistre le mot de passe hashé
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    # formulaire pour les modifications d'utilisateur .il inclut tous les mots de passe de l'utilisateur mais affiche le mot de passe
    password = ReadOnlyPasswordHashField()

    class Meta:
        mode = Utilisateur
        fields = ['email', 'nom', 'prenom', 'password', 'role', 'is_active']


class UserAdmin(BaseUserAdmin):
    # formulaire pour ajouter et changer les instances d'utilisateurs
    form = UserChangeForm
    add_form = UserCreationForm

    # definir l'affichage des formulaires
    list_display = ['email', 'nom', 'prenom', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_active']
    fieldsets = [
        (None, {"fields": ['email', 'password', 'role']}),
        ("Informations personnelles", {"fields": ['nom', 'prenom', 'image']}),
        ("Permissions", {"fields": ['is_staff', 'is_active']}),
    ]

    # add fieldsets

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "nom", "prenom", "role", "image", "password1", "password2", "is_active",
                           "is_staff"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


# # custom
# admin.site.index_template = 'admin/dashboard.html',

# Register your models here.
admin.site.register(Utilisateur, UserAdmin)
admin.site.register(Role)
admin.site.register(Action)
admin.site.register(Document, DocumentAdmin)
