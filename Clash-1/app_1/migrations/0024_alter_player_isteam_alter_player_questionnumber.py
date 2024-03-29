# Generated by Django 4.1.7 on 2023-05-01 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0023_player_isteam_alter_player_questionnumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='isTeam',
            field=models.BooleanField(choices=[('True', True), ('False', False)], default=False),
        ),
        migrations.AlterField(
            model_name='player',
            name='questionNumber',
            field=models.IntegerField(blank=True, default=3, null=True),
        ),
    ]
