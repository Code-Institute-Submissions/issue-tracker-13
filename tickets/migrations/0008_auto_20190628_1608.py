# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-06-28 19:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0007_ticketpayment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TicketPayment',
        ),
        migrations.AddField(
            model_name='ticket',
            name='total_paid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]