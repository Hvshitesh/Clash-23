# Generated by Django 4.1.7 on 2023-05-10 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0032_alter_player_questionnumber'),
    ]

    operations = [
        migrations.CreateModel(
            name='APICount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='player',
            name='questionNumber',
            field=models.IntegerField(blank=True, default=9, null=True),
        ),
    ]
