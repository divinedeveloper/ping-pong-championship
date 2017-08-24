# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-24 12:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20170823_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referee',
            name='game',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Game'),
        ),
        migrations.AlterField(
            model_name='referee',
            name='player_one_detail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='details_player_one', to='api.Player'),
        ),
        migrations.AlterField(
            model_name='referee',
            name='player_two_detail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='details_player_two', to='api.Player'),
        ),
    ]
