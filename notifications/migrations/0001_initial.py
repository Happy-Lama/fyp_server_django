# Generated by Django 4.2.10 on 2024-02-28 19:44

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('notification_type', models.CharField(choices=[('WARN', 'WARNING'), ('DANGER', 'DANGER'), ('INFO', 'INFORMATIONAL')], max_length=7)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('transformer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.transformerspecification')),
            ],
        ),
    ]
