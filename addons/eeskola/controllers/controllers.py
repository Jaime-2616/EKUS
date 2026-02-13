# -*- coding: utf-8 -*-
# from odoo import http


# class Eeskola(http.Controller):
#     @http.route('/eeskola/eeskola', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/eeskola/eeskola/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('eeskola.listing', {
#             'root': '/eeskola/eeskola',
#             'objects': http.request.env['eeskola.eeskola'].search([]),
#         })

#     @http.route('/eeskola/eeskola/objects/<model("eeskola.eeskola"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('eeskola.object', {
#             'object': obj
#         })

