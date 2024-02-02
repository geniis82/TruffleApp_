# -*- coding: utf-8 -*-
# from odoo import http


# class Truffleapp(http.Controller):
#     @http.route('/truffleapp/truffleapp', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/truffleapp/truffleapp/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('truffleapp.listing', {
#             'root': '/truffleapp/truffleapp',
#             'objects': http.request.env['truffleapp.truffleapp'].search([]),
#         })

#     @http.route('/truffleapp/truffleapp/objects/<model("truffleapp.truffleapp"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('truffleapp.object', {
#             'object': obj
#         })
