from odoo import models, fields, api,exceptions
from datetime import datetime

class FacturaModel(models.Model):
    _name = 'truffleapp.facturamodel'
    _description = 'Invoice Model'

    name = fields.Integer(string='Invoice Number', default=lambda self: self.setRef(),readonly=True)
    date = fields.Date(string='Invoice Date', default=lambda self: datetime.today(),readonly=True)
    lines = fields.One2many('truffleapp.facturalineamodel', 'invoice', string='Invoice Lines')
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)
    iva_percentage = fields.Selection(string='IVA Percentage', selection=[('0','0%'),('4','4%'),('10','10%'),('21','21%')],default='0')
    total_without_iva = fields.Float(string='Total Amount (without IVA)', compute='_compute_total_without_iva', store=True)
    state=fields.Selection(string="State:",selection=[('D','Draft'),('C','Confirmed')], default='D')
    clients= fields.Many2one('res.partner',string="Clients",required=True,default=lambda self: self.env.user.partner_id.id,readonly=True)
    active=fields.Boolean(default=True)
    order=fields.One2many('truffleapp.ordermodel','invoice',string="Order")

    @api.depends('lines.price_subtotal', 'iva_percentage')
    def _compute_total_amount(self):
        for invoice in self:
            subtotal = sum(invoice.lines.mapped('price_subtotal'))
            iva_amount = (subtotal * int(invoice.iva_percentage)) / 100.0
            invoice.total_amount = subtotal + iva_amount

    @api.depends('lines.price_subtotal')
    def _compute_total_without_iva(self):
        for invoice in self:
            invoice.total_without_iva = sum(invoice.lines.mapped('price_subtotal'))

    @api.model
    def create(self, values):
        if 'lines' not in values or not values['lines']:
            raise exceptions.ValidationError("You can't create an invoice without any line invoice")
    
        invoiced_lines = values.get('lines')
    
        for invoiced_lines_data in invoiced_lines:
            product_id = invoiced_lines_data[2].get('product')
            quantity = invoiced_lines_data[2].get('quantity')

            # Verificar si hay suficiente stock
            # product = self.env['truffleapp.productmodel'].browse(product_id)
            # if quantity > product.stock:
            #     raise exceptions.ValidationError(f"The stock of product {product.name} is not available")
        return super(FacturaModel, self).create(values)
    
    def changeStatus(self):
        if(self.state=='D'):
            for iinvoiced_line in self.lines:
                product_id=iinvoiced_line.product.id
                quantity=iinvoiced_line.quantity
            #     if iinvoiced_line.quantity <= iinvoiced_line.product.stock:
            #         new_stock = iinvoiced_line.product.stock - iinvoiced_line.quantity
            #         iinvoiced_line.product.sudo().write({'stock': new_stock})
            #         iinvoiced_line.quantity = min(iinvoiced_line.quantity, iinvoiced_line.product.stock)
                product = self.env['truffleapp.productmodel'].browse(product_id)
                if quantity > product.stock:
                    raise exceptions.ValidationError(f"The stock of product {product.name} is not available")
                self.state = 'C'
        else:
            self.state = 'D'

    def setRef(self):
        result=self.env['truffleapp.facturamodel'].search_read()
        if len(result)==0:
            return 1
        else:
            return result[-1]["name"]+1
        
    def history(self):
        invoice_confirm = self.env['truffleapp.facturamodel'].search([('state', '=', 'C'), ('active', '=', True)])
        invoice_confirm.write({'state': 'C', 'active': False})