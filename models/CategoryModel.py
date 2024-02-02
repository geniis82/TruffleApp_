from odoo import models, fields, api

class CategoryModel(models.Model):
    _name='truffleapp.categorymodel'
    _description='categrymodel'
    _sql_constraints=[
        ('_name_uniq',
        'UNIQUE(name)',
        'There cannot be two categories with the same name'),
    ]

    name=fields.Char(string="Name",required=True)
    parent_category = fields.Many2one('truffleapp.categorymodel', string='Parent Category', index=True, ondelete='cascade')
    child_categories = fields.One2many('truffleapp.categorymodel', 'parent_category', string='Child Categories')
    category_path = fields.Char(string="Category Path", compute="_compute_category_path", store=True)

    quality=fields.One2many("truffleapp.qualitymodel","category",string="qualities")
    weight=fields.One2many("truffleapp.weightmodel","category",string="weight")
    product=fields.One2many("truffleapp.productmodel","category",string="product")


    @api.depends('name', 'parent_category', 'parent_category.category_path')
    def _compute_category_path(self):
        for category in self:
            category_path = category.name
            parent_category = category.parent_category
            while parent_category:
                category_path = f"{parent_category.name} / {category_path}"
                parent_category = parent_category.parent_category
            category.category_path = category_path

    # @api.model
    # def update_category_paths(self):
    #     # Método para actualizar manualmente los 'category_path'
    #     categories = self.search([])
    #     categories._compute_category_path()