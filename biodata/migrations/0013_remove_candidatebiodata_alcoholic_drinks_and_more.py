# Generated by Django 5.2.1 on 2025-05-09 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('biodata', '0012_remove_candidatebiodata_current_city_country_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidatebiodata',
            name='alcoholic_drinks',
        ),
        migrations.RemoveField(
            model_name='candidatebiodata',
            name='children',
        ),
        migrations.RemoveField(
            model_name='candidatebiodata',
            name='company_name',
        ),
        migrations.RemoveField(
            model_name='candidatebiodata',
            name='eating_habits',
        ),
        migrations.RemoveField(
            model_name='candidatebiodata',
            name='hobbies',
        ),
        migrations.RemoveField(
            model_name='candidatebiodata',
            name='legal_police_case',
        ),
        migrations.RemoveField(
            model_name='candidatebiodata',
            name='other_habits',
        ),
        migrations.RemoveField(
            model_name='candidatebiodata',
            name='smoke',
        ),
    ]
