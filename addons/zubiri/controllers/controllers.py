# -*- coding: utf-8 -*-
# from odoo import http


# class Zubiri(http.Controller):
#     @http.route('/zubiri/zubiri', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/zubiri/zubiri/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('zubiri.listing', {
#             'root': '/zubiri/zubiri',
#             'objects': http.request.env['zubiri.zubiri'].search([]),
#         })

#     @http.route('/zubiri/zubiri/objects/<model("zubiri.zubiri"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('zubiri.object', {
#             'object': obj
#         })

