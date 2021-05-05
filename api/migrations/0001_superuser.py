from django.contrib.auth.models import User
from django.db import migrations

from emphasoft.settings import ADMIN_USERNAME, ADMIN_PASSWORD


class Migration(migrations.Migration):

    def create_superuser(apps, schema_editor):
        superuser = User.objects.create_superuser(username=ADMIN_USERNAME, password=ADMIN_PASSWORD, email=None)
        superuser.save()

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
