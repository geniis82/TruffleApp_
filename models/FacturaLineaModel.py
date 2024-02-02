from odoo import models, fields, api,exceptions

class FacturaLineaModel(models.Model):
    _name = 'truffleapp.facturalineamodel'
    _description = 'Invoice Line Model'

    product = fields.Many2one('truffleapp.productmodel', string='Product', required=True, ondelete='cascade')
    quantity = fields.Float(string='Quantity', required= True,default=1)
    weight= fields.Float(string="Weight", compute='_compute_weight',store=True)
    mesure= fields.Char(string="Measure", compute='_compute_measure', store=True)
    price_unit = fields.Float(string='Unit Price', related='product.price', readonly=True)
    price_subtotal = fields.Float(string='Subtotal', compute='_compute_price_subtotal', store=True)
    invoice = fields.Many2one('truffleapp.facturamodel', string='Invoice')

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

    # @api.onchange('quantity', 'product')
    # def _onchange_quantity(self):
    #     if self.product and self.quantity > self.product.stock:
    #         raise exceptions.ValidationError("La cantidad no puede ser mayor al stock disponible.")

    # @api.model
    # def create(self, values):
    #     line = super(FacturaLineaModel, self).create(values)
    #     line._update_stock()
    #     return line

    # def write(self, values):
    #     super(FacturaLineaModel, self).write(values)
    #     self._update_stock()

    # def _update_stock(self):
    #     if self.product:
    #         new_stock = self.product.stock - self.quantity
    #         self.product.write({'stock': new_stock})

    # @api.onchange('product')
    # def _onchange_product(self):
    #     if self.product:
    #         # Establece la cantidad máxima permitida por el stock
    #         self.quantity = min(self.quantity, self.product.stock)
    
    