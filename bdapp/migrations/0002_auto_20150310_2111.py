# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fec', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='l10n_ec_authorization',
            name='codDoc',
        ),
        migrations.AddField(
            model_name='l10n_ec_authorization',
            name='ptoEmision',
            field=models.CharField(default='001', max_length=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='l10n_ec_partner',
            name='email',
            field=models.CharField(default='example@example.com', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='l10n_ec_partner',
            name='phone',
            field=models.CharField(default='02999999', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='l10n_ec_authorization',
            name='ambiente',
            field=models.CharField(default=b'1', max_length=2, choices=[(b'1', 'Pruebas'), (b'2', 'Producci\xf3n')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='l10n_ec_authorization',
            name='tipoEmision',
            field=models.CharField(default=b'1', max_length=2, choices=[(b'1', 'Emisi\xf3n Normal'), (b'2', 'Emisi\xf3n por indisponibilidad del sistema (contingencia)')]),
            preserve_default=True,
        ),
    ]
