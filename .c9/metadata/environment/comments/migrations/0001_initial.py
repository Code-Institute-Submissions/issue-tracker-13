{"filter":false,"title":"0001_initial.py","tooltip":"/comments/migrations/0001_initial.py","undoManager":{"mark":-1,"position":-1,"stack":[[{"start":{"row":26,"column":0},"end":{"row":54,"column":5},"action":"insert","lines":["# -*- coding: utf-8 -*-","# Generated by Django 1.11 on 2019-07-08 11:58","from __future__ import unicode_literals","","from django.db import migrations, models","import django.db.models.deletion","import django.utils.timezone","","","class Migration(migrations.Migration):","","    initial = True","","    dependencies = [","        ('tickets', '__first__'),","    ]","","    operations = [","        migrations.CreateModel(","            name='Comment',","            fields=[","                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),","                ('author', models.CharField(max_length=150)),","                ('comment', models.TextField()),","                ('comment_date', models.DateTimeField(default=django.utils.timezone.now)),","                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickets.Ticket')),","            ],","        ),","    ]"],"id":2}]]},"ace":{"folds":[],"scrolltop":0,"scrollleft":0,"selection":{"start":{"row":26,"column":0},"end":{"row":26,"column":0},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":0},"timestamp":1566209151919,"hash":"efb5b2afc44178e1de6573a39df66ba4bdc61d07"}