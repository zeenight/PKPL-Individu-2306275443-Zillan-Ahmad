from django import forms
from .models import UserProfile
from django.core.validators import RegexValidator

class UserProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    
    class Meta:
        model = UserProfile
        fields = ["username", "email", "password", "tanggal_lahir", "npwp", "nomor_hp", "status_sertifikasi", "url_blog", "deskripsi_diri"]
    
    def clean_tanggal_lahir(self):
        """Validates that the user is at least 12 years old"""
        tanggal_lahir = self.cleaned_data.get("tanggal_lahir")
        if tanggal_lahir and not UserProfile(tanggal_lahir=tanggal_lahir).is_age_valid():
            raise forms.ValidationError("Usia minimal 12 tahun.")
        return tanggal_lahir