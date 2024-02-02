from odoo import models, fields,api,exceptions
from datetime import datetime

class OrderModel(models.Model):
    _name = 'truffleapp.ordermodel'
    _description = 'Order Model'

    name = fields.Integer(string='Order Number', default=lambda self: self.setRef(),readonly=True)
    data = fields.Date(string='Invoice Date', default=lambda self: datetime.today())
    orderLine = fields.One2many('truffleapp.orderlinemodel','order' ,string='Order Lines')
    # quantity= fields.Integer(string="Quantity",required=True)
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)
    iva_percentage = fields.Selection(string='IVA Percentage', selection=[('0','0%'),('4','4%'),('10','10%'),('21','21%')],default='0')
    total_without_iva = fields.Float(string='Total Amount (without IVA)', compute='_compute_total_without_iva', store=True)
    client= fields.Many2one('res.partner',string="Clients",required=True)
    state=fields.Selection(string="State:",selection=[('D','Draft'),('C','Confirmed'),('I','Invoiced')], default='D')
    active=fields.Boolean(default=True)
    # invoice=fields.Many2one('truffleapp.facturamodel',string="Invoice",required=True)

    @api.depends('orderLine.price_subtotal', 'iva_percentage')
    def _compute_total_amount(self):
        for order in self:
            subtotal = sum(order.orderLine.mapped('price_subtotal'))
            iva_amount = (subtotal * int(order.iva_percentage)) / 100.0
            order.total_amount = subtotal + iva_amount

    @api.depends('orderLine.price_subtotal')
    def _compute_total_without_iva(self):
        for order in self:
            order.total_without_iva = sum(order.orderLine.mapped('price_subtotal'))

    def changeStatusC(self):
        if(self.state=='D'):
            for order_line in self.orderLine:
                if order_line.quantity <= order_line.product.stock:
                    new_stock = order_line.product.stock - order_line.quantity
                    order_line.product.write({'stock': new_stock})
                    order_line.quantity = min(order_line.quantity, order_line.product.stock)
            self.state = 'C'
        else:
            self.state = 'D'
    

    def change_status_i_create_invoice(self):
        if self.state == 'C':
            invoice_lines = []
            for order_line in self.orderLine:
                invoice_lines.append((0, 0, {
                    'product': order_line.product.id,
                    'quantity': order_line.quantity,
                }))
            invoice_data = {
                'clients': self.client.id,
                'lines': invoice_lines,
                'iva_percentage': self.iva_percentage,
                'state': 'D',  
            }
            invoice = self.env['truffleapp.facturamodel'].create(invoice_data)
            self.state = 'I'
            return invoice
        else:
            self.state = 'C'

    @api.model
    def create(self, values):
        if 'orderLine' not in values or not values['orderLine']:
            raise exceptions.ValidationError("You can't create an order without any line order")
        
        order_lines = values.get('orderLine')
    
        for order_line_data in order_lines:
            product_id = order_line_data[2].get('product')
            quantity = order_line_data[2].get('quantity')

            # Verificar si hay suficiente stock
            product = self.env['truffleapp.productmodel'].browse(product_id)
            if quantity > product.stock:
                raise exceptions.ValidationError(f"The stock of product {product.name} is not available")
        return super(OrderModel, self).create(values)

    def setRef(self):
        result=self.env['truffleapp.ordermodel'].search_read()
        if len(result)==0:
            return 1
        else:
            return result[-1]["name"]+1
        
    def history(self):
        invoiced_orders = self.env['truffleapp.ordermodel'].search([('state', '=', 'I'), ('active', '=', True)])
        for order in invoiced_orders:
            order.write({'state': 'I', 'active': False})