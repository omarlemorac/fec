# -*- coding: utf-8 -*-

from django.db import models

class l10n_ec_authorization(models.Model):
    AMBIENTE_CHOICES=(
            ('1', u'Pruebas'),
            ('2', u'Producción'),
            )
    TIPO_EMISION_CHOICES=(
            ('1', u'Emisión Normal'),
            ('2', u'Emisión por indisponibilidad del sistema (contingencia)'),
            )
    name = models.CharField(max_length=200)
    ambiente = models.CharField(max_length=2, choices=AMBIENTE_CHOICES,
            default='1')
    tipoEmision = models.CharField(max_length=2,
            choices=TIPO_EMISION_CHOICES,
            default = '1')
    razonSocial = models.CharField(max_length=255)
    nombreComercial = models.CharField(max_length=255)
    password = models.CharField(max_length=50)
    signature = models.TextField()
    ruc = models.CharField(max_length=13)
    estab = models.CharField(max_length=3)
    ptoEmision = models.CharField(max_length=3)
    secuencial = models.IntegerField(default=1)
    dirMatriz = models.CharField(max_length=255)
    dirEstablecimiento = models.CharField(max_length=255)
    contribuyenteEspecial = models.CharField(max_length=50)
    obligadoContabilidad = models.CharField(max_length=2)

def __unicode__():
    return name


class l10n_ec_partner(models.Model):
    name = models.CharField(max_length=255)
    razonSocial = models.CharField(max_length=255)
    identificacion = models.CharField(max_length= 255)
    tipoIdentificacion = models.CharField(max_length= 5)
    direccion = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)

class l10n_ec_invoice(models.Model):
    name = models.CharField(max_length=255)
    authorization = models.ForeignKey(l10n_ec_authorization)
    partner = models.ForeignKey(l10n_ec_partner)










#vim: ai ts=8 sts=4 et sw=4


