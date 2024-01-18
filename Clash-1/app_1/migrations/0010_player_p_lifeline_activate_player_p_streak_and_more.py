# Generated by Django 4.1.7 on 2023-03-10 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0009_alter_player_p_current_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='p_lifeline_activate',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='p_streak',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='p_current_question',
            field=models.IntegerField(blank=True, default=4, null=True),
        ),
    ]