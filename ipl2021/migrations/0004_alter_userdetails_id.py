# Generated by Django 3.2.6 on 2021-09-01 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipl2021', '0003_auto_20210901_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]