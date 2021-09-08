# Generated by Django 3.2.6 on 2021-09-01 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipl2021', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('passwrd', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'user_details',
                'managed': True,
            },
        ),
        migrations.AlterModelOptions(
            name='matches',
            options={'verbose_name_plural': 'Matches'},
        ),
        migrations.AlterModelOptions(
            name='players',
            options={'verbose_name_plural': 'Players'},
        ),
    ]
