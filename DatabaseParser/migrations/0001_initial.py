# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WordTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('word', models.CharField(default='', max_length=256)),
                ('docName', models.CharField(default='', max_length=256)),
                ('freq', models.IntegerField(default=0)),
            ],
        ),
    ]
