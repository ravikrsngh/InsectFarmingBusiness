# Generated by Django 3.2.15 on 2022-10-23 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20221023_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insectbusiness',
            name='home_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_country', to='app.homecountry'),
        ),
    ]
