from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProductModel(models.Model):
    _name='truffleapp.productmodel'
    _description='model of product'
    _sql_constraints=[
        ('_name_uniq',
        'UNIQUE(name,category,weight,quality)',
        'There cannot be two products with the same category,,weight and quality'),
        
    ]

    name=fields.Char(string="Name",required=True, index=True)
    photo=fields.Binary()
    price=fields.Float(string="Price",required=True)
    stock=fields.Integer(string="Stock",required=True)
    category=fields.Many2one("truffleapp.categorymodel",string="category",store=True,required=True)
    path_category=fields.Char(string="Category Path", related='category.category_path',store=True)
    weight = fields.Many2one("truffleapp.weightmodel", string="Weight", domain="[('category', '=', category)]")
    mesure= fields.Char(string="Measure",  store=True, String = "Mesure", )
    quality = fields.Many2one("truffleapp.qualitymodel", string="Quality", domain="[('category','=',category)]")

    has_category_weight = fields.Boolean(string="Has Category Weight", compute='_compute_has_category_weight')
    has_category_quality = fields.Boolean(string="Has Category Quality", compute='_compute_has_category_quality')

    # @api.onchange('category')
    # def onchange_category(self):
    #     # Actualizar el dominio del campo 'weight' según la categoría seleccionada y sus categorías padre
    #     category_ids = [self.category.id] + self.category.parent_category.ids
    #     weight_domain = [('category', 'in', category_ids)]
        
    #     # Actualizar el dominio del campo 'quality' según la categoría seleccionada y sus categorías padre
    #     quality_domain = [('category', 'in', category_ids)]
        
    #     return {
    #         'domain': {
    #             'weight': weight_domain,
    #             'quality': quality_domain,
    #         }
    #     }
    
    @api.depends('category.weight','category.parent_category.weight')
    def _compute_has_category_weight(self):
        for record in self:
            has_weight = bool(record.category.weight) 
            record.has_category_weight = has_weight

    # @api.depends('category.weight','category.parent_category.weight')
    # def _compute_measure(self):
    #     for line in self:
    #         line.mesure = line.category.weight.mesure if line.category.weight else ''

    @api.depends('category.quality','category.parent_category.quality')
    def _compute_has_category_quality(self):
        for record in self:
            has_quality = bool(record.category.quality) 
            record.has_category_quality = has_quality

    @api.model
    def create(self, values):
        if values.get('category'):
            category = self.env['truffleapp.categorymodel'].browse(values['category'])
            if not category.weight and not category.quality :
                # Permitir la creación de productos incluso si la categoría no tiene weight o quality
                product = super(ProductModel, self).create(values)
                return product

        # Permitir la creación de productos si al menos uno de los campos weight o quality está presente
        if not values.get('weight') and not values.get('quality'):
            raise ValidationError("At least one of the fields 'Weight' or 'Quality' is required.")
        
        # Validar la presencia del campo 'Measure' si 'Weight' está presente
        if values.get('weight') and not values.get('mesure'):
            raise ValidationError("Field 'Measure' is required when 'Weight' is present.")

        product = super(ProductModel, self).create(values)
        return product
    
    def set_categortPath(self):
        path=self.category.category_path
        self.path_category=path
        return True
