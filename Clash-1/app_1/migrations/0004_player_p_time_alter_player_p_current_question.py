# Generated by Django 4.1.7 on 2023-03-06 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0003_alter_player_p_current_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='p_time',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='p_current_question',
            field=models.IntegerField(blank=True, default=4, null=True),
        ),
    ]
