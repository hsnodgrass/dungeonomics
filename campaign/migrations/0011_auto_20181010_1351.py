# Generated by Django 2.0.9 on 2018-10-10 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0010_campaign_published_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='published_date',
            field=models.DateTimeField(blank=True),
        ),
    ]