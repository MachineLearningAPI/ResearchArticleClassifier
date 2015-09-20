# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DatabaseParser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocClass',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('docName', models.CharField(default='', max_length=256)),
                ('className', models.CharField(default='', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='DocFreqTable',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('word', models.CharField(default='', max_length=256)),
                ('docFreq', models.IntegerField(default=0)),
            ],
        ),
    ]
