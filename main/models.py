# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator, EmailValidator, URLValidator
from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta

class UserProfile(AbstractUser):
    # Validasi NPWP (Format: XX.XXX.XXX.X-XXX.XXX)
    npwp_validator = RegexValidator(
        regex=r'^\d{2}\.\d{3}\.\d{3}\.\d{1}-\d{3}\.\d{3}$',
        message="Format NPWP harus XX.XXX.XXX.X-XXX.XXX"
    )

    # Validasi Nomor HP (Format: minimal 8, maksimal 15 angka, tanpa '+')
    phone_validator = RegexValidator(
        regex=r'^\d{8,15}$',
        message="Nomor HP harus terdiri dari 8-15 digit angka tanpa '+'"
    )

    # Status Sertifikasi
    STATUS_CHOICES = [
        ('Belum', 'Belum'),
        ('Sedang', 'Sedang'),
        ('Diterima', 'Diterima'),
        ('Ditolak', 'Ditolak'),
    ]

    # Field Model
    npwp = models.CharField(
        max_length=20,
        unique=True,
        validators=[npwp_validator],
        help_text="Format: XX.XXX.XXX.X-XXX.XXX"
    )
    status_sertifikasi = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Belum'
    )
    tanggal_lahir = models.DateField(
        help_text="Minimal umur 12 tahun",
        default=date(2000, 1, 1)  # Default ke 1 Januari 2000
    )

    nomor_hp = models.CharField(
        max_length=15,
        validators=[phone_validator],
        help_text="Isi tanpa '+' atau '-'"
    )
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator(message="Format email tidak valid")],
        help_text="Masukkan email yang valid"
    )
    url_blog = models.URLField(
        blank=True,
        null=True,
        validators=[URLValidator(message="Masukkan URL yang valid")],
        help_text="Masukkan URL blog (Opsional)"
    )
    deskripsi_diri = models.TextField(
        validators=[MinLengthValidator(5), MaxLengthValidator(1000)],
        help_text="Minimal 5 karakter, maksimal 1000 karakter"
    )

    def __str__(self):
        return self.username

    def is_age_valid(self):
        """Validasi apakah usia minimal 12 tahun."""
        if self.tanggal_lahir:
            today = date.today()
            min_birth_date = today - timedelta(days=12*365)
            return self.tanggal_lahir <= min_birth_date
        return False
    
    def save(self, *args, **kwargs):
    # Jika user adalah superuser, abaikan validasi tertentu
        if self.is_superuser:
            self.npwp = self.npwp or "00.000.000.0-000.000"  # Dummy NPWP
            self.nomor_hp = self.nomor_hp or "00000000"  # Dummy nomor HP
            self.deskripsi_diri = self.deskripsi_diri or "Admin user"
        
        super().save(*args, **kwargs)