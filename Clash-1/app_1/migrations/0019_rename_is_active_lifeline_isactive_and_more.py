# Generated by Django 4.1.7 on 2023-03-26 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0018_submission_iscorrect_alter_player_p_current_question'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lifeline',
            old_name='is_active',
            new_name='isactive',
        ),
        migrations.RenameField(
            model_name='lifeline',
            old_name='number_of_lifeline',
            new_name='lifelinecounter',
        ),
        migrations.RenameField(
            model_name='lifeline',
            old_name='lifeline_id',
            new_name='lifelineid',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='p_end_time',
            new_name='endingtime',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='p_is_ended',
            new_name='isended',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='p_is_started',
            new_name='isstarted',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='p_lifeline_activate',
            new_name='lifelineactivateflag',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='p_lifeline_array',
            new_name='lifelinearray',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='p_marks_add',
            new_name='marksadd',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='p_marks_sub',
            new_name='markssubstract',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='p_current_score',
            new_name='playerscore',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='p_previous_question',
            new_name='previousquestionnumber',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='p_current_question_number',
            new_name='questionindex',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='p_que_list',
            new_name='questionlist',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='p_starting_time',
            new_name='startingtime',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='q_option_1',
            new_name='questionOption2',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='q_option_2',
            new_name='questionOption3',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='q_option_3',
            new_name='questionOption4',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='q_answer',
            new_name='questionanswer',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='q_id',
            new_name='questionid',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='q_option_4',
            new_name='questionoption1',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='question',
            new_name='questiontext',
        ),
        migrations.RenameField(
            model_name='submission',
            old_name='lifeline_activated',
            new_name='islifelineactivated',
        ),
        migrations.RenameField(
            model_name='submission',
            old_name='sequential_ques_id',
            new_name='questionindex',
        ),
        migrations.RenameField(
            model_name='submission',
            old_name='question_id',
            new_name='questionnumber',
        ),
        migrations.RenameField(
            model_name='submission',
            old_name='question_answer',
            new_name='questionoption',
        ),
        migrations.RemoveField(
            model_name='player',
            name='p_current_question',
        ),
        migrations.AddField(
            model_name='player',
            name='questionnumber',
            field=models.IntegerField(blank=True, default=4, null=True),
        ),
    ]
