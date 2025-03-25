**cara masukkan superuser/admin**

masuk ke python shell lalu ketik yang ada dibawah

from main.models import UserProfile
from datetime import date

admin_user = UserProfile.objects.create_superuser(
    username="admin",
    email="admin@example.com",
    password="admin123",
    npwp="00.000.000.0-000.000",
    nomor_hp="00000000",
    deskripsi_diri="Admin user",
    tanggal_lahir=date(2000, 1, 1)  # Tambahkan tanggal lahir manual
)
admin_user.save()

