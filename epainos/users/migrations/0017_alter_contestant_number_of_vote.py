# Generated by Django 4.2.13 on 2024-07-19 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_contestantstage_stage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestant',
            name='number_of_vote',
            field=models.IntegerField(blank=True, default=0, help_text='this displays the contestant vote count', null=True, verbose_name='Contestant Votes'),
        ),
    ]
