from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name="event",
            old_name="starts_at",
            new_name="date",
        ),
        migrations.AlterField(
            model_name="event",
            name="poster",
            field=models.ImageField(blank=True, upload_to="posters/"),
        ),
        migrations.AddField(
            model_name="event",
            name="location",
            field=models.CharField(default="", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="event",
            name="organizer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="events",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]