from odoo import models, fields, api

class WeightModel(models.Model):
    _name='truffleapp.weightmodel'
    _description="weightmodel"
    _sql_constraints=[
        ('_name_uniq',
        'UNIQUE(name,category)',
        'There cannot be two weight with the same value and category'),
    ]

    name=fields.Float(required=True,name="Weight")
    # mesure=fields.Char(required=True,name="Mesure")
    category=fields.Many2one("truffleapp.categorymodel",string="category",store=True,required=True)

    # @api.onchange('category')
    # def onchange_category(self):
    #     # Filtra las opciones de Weight basado en la categoría seleccionada en ProductModel
    #     return {'domain': {'category': [('id', '=', self.category.id)]}}