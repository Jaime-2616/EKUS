from odoo import models, fields

class Incidencia(models.Model):
    _name = 'zubiri.incidencia'
    _description = 'Incidencia'

    name = fields.Char('Izena', required=True)
    equipo_id = fields.Many2one('zubiri.equipo', string='Ekipoa')
    descripcion = fields.Text('Deskribapena')
    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('resuelta', 'Resuelta')
    ], string='Egoera', default='pendiente')