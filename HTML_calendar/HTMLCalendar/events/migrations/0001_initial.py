# Generated by Django 3.1.1 on 2020-10-19 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='날짜')),
                ('total', models.IntegerField(verbose_name='일매출')),
            ],
            options={
                'verbose_name': '이벤트 데이터',
                'verbose_name_plural': '이벤트 데이터',
            },
        ),
    ]
