# Generated by Django 4.2 on 2023-05-31 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_article_timestamp_article_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
