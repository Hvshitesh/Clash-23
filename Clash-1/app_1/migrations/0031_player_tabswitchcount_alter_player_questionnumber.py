# Generated by Django 4.1.7 on 2023-05-09 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0030_question_questionnumber_alter_player_questionnumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='tabSwitchCount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='player',
            name='questionNumber',
            field=models.IntegerField(blank=True, default=2, null=True),
        ),
    ]
