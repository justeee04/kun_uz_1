# Generated by Django 4.1.3 on 2022-11-29 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='region_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='region', to='news.region'),
        ),
    ]
