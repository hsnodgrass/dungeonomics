# Generated by Django 2.0.9 on 2018-10-06 21:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('campaign', '0008_auto_20180403_1802'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('score', models.IntegerField(default=5)),
                ('comment', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='campaign',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='campaign',
            name='tavern_description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='review',
            name='campaign',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaign.Campaign'),
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]