# Generated by Django 4.1.2 on 2022-10-13 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_insectbusiness'),
    ]

    operations = [
        migrations.AddField(
            model_name='insectbusiness',
            name='parent_company',
            field=models.CharField(default='', max_length=50),
        ),
    ]