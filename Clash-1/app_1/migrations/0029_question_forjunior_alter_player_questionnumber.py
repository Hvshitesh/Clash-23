# Generated by Django 4.1.7 on 2023-05-09 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0028_player_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='forJunior',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='questionNumber',
            field=models.IntegerField(blank=True, default=7, null=True),
        ),
    ]
