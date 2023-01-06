from django.db import migrations
from api.user.models import CustomUser


class Migration(migrations.Migration):
    def seed_data(apps, schema_editor):
        user = CustomUser(name="p9648213", email="lvp3795@gmail.com",
                          is_staff=True, is_superuser=True, phone='099993949', gender="Male")
        user.set_password("ad12345#")
        user.save()

    dependencies = [

    ]

    operations = [
        migrations.RunPython(seed_data),
    ]
