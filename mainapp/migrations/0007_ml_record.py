# Generated by Django 5.0.3 on 2024-04-09 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_alter_customuser_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='ML_record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_date', models.DateField(auto_now_add=True)),
                ('sh_score', models.TextField()),
                ('ch_score', models.TextField()),
                ('number_of_clusters', models.TextField()),
                ('total_records', models.TextField()),
                ('word2vec_vector_size', models.TextField()),
                ('word2vec_window_size', models.TextField()),
                ('word2vec_word_min_count', models.TextField()),
                ('from_date', models.TextField()),
                ('end_date', models.TextField()),
            ],
            options={
                'ordering': ['-added_date'],
            },
        ),
    ]
