from odoo import models, fields

class Aula(models.Model):
    _name = 'zubiri.aula'
    _description = 'Aula'

    name = fields.Char('Izena', required=True)
    equipo_ids = fields.One2many('zubiri.equipo', 'aula_id', string='Ekipamenduak')