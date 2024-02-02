from odoo import models, fields, api

class QualityModel(models.Model):
    _name='truffleapp.qualitymodel'
    _description='qualitymodel'
    _sql_constraints=[
        ('_name_uniq',
        'UNIQUE(name,category)',
        'There cannot be two qualities with the same value and category'),
    ]

    name=fields.Char(name="Quality",required=True)
    category=fields.Many2one("truffleapp.categorymodel",string="category",store=True,required=True)
