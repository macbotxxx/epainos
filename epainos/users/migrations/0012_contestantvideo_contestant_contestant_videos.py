# Generated by Django 4.2.13 on 2024-06-30 02:40

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_transactions_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContestantVideo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='The unique identifier of an object.', primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, editable=False, help_text='Timestamp when the record was created. The date and time\n            are displayed in the Timezone from where request is made.\n            e.g. 2019-14-29T00:15:09Z for April 29, 2019 0:15:09 UTC', verbose_name='Created')),
                ('modified_date', models.DateTimeField(auto_now=True, help_text='Timestamp when the record was modified. The date and\n            time are displayed in the Timezone from where request\n            is made. e.g. 2019-14-29T00:15:09Z for April 29, 2019 0:15:09 UTC\n            ', null=True, verbose_name='Updated')),
                ('video_file', models.FileField(upload_to='videos/', verbose_name='Video File')),
            ],
            options={
                'verbose_name': 'Contestant Video',
                'verbose_name_plural': 'Contestant Video',
                'ordering': ['-created_date'],
            },
        ),
        migrations.AddField(
            model_name='contestant',
            name='contestant_videos',
            field=models.ManyToManyField(to='users.contestantvideo'),
        ),
    ]
