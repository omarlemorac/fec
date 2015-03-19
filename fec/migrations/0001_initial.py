# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='l10n_ec_authorization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('ambiente', models.CharField(max_length=2)),
                ('tipoEmision', models.CharField(max_length=2)),
                ('razonSocial', models.CharField(max_length=255)),
                ('nombreComercial', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=50)),
                ('signature', models.TextField()),
                ('ruc', models.CharField(max_length=13)),
                ('codDoc', models.CharField(max_length=3)),
                ('estab', models.CharField(max_length=3)),
                ('secuencial', models.IntegerField(default=1)),
                ('dirMatriz', models.CharField(max_length=255)),
                ('dirEstablecimiento', models.CharField(max_length=255)),
                ('contribuyenteEspecial', models.CharField(max_length=50)),
                ('obligadoContabilidad', models.CharField(max_length=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='l10n_ec_invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('authorization', models.ForeignKey(to='fec.l10n_ec_authorization')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='l10n_ec_partner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('razonSocial', models.CharField(max_length=255)),
                ('identificacion', models.CharField(max_length=255)),
                ('tipoIdentificacion', models.CharField(max_length=5)),
                ('direccion', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='l10n_ec_invoice',
            name='partner',
            field=models.ForeignKey(to='fec.l10n_ec_partner'),
            preserve_default=True,
        ),
    ]
