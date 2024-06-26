# Generated by Django 5.0.3 on 2024-04-15 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0017_alter_globals_number_of_rows_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='globals',
            name='training_thread_running',
            field=models.IntegerField(default=False),
        ),
        migrations.AlterField(
            model_name='globals',
            name='testing_thread_running',
            field=models.BooleanField(default=False),
        ),
    ]
