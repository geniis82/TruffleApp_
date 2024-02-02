from odoo import models,fields,api,exceptions

class OrderLineModel(models.Model):
    _name = 'truffleapp.orderlinemodel'
    _description = 'Order Line Model'

    product = fields.Many2one('truffleapp.productmodel', string='Product', required=True, ondelete='cascade')
    quantity = fields.Float(string='Quantity', required= True,default=1)
    weight= fields.Float(string="Weight", compute='_compute_weight',store=True)
    mesure= fields.Char(string="Measure", compute='_compute_measure', store=True)
    price_unit = fields.Float(string='Unit Price', related='product.price', readonly=True)
    price_subtotal = fields.Float(string='Subtotal', compute='_compute_price_subtotal', store=True)
    order = fields.Many2one('truffleapp.ordermodel', string='Order')

    @api.depends('quantity', 'price_unit')
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = line.quantity * line.price_unit

    @api.depends('quantity', 'product.weight')
    def _compute_weight(self):
        for line in self:
            line.weight = line.quantity * line.product.weight.name if line.product.weight else 0.0

    @api.depends('product.mesure')
    def _compute_measure(self):
        for line in self:
            line.mesure = line.product.mesure if line.product.weight else ''
