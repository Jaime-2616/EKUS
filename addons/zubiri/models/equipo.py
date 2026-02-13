from odoo import models, fields, api

class Equipo(models.Model):
    _name = 'zubiri.equipo'
    _description = 'Equipo Informatikoa'

    name = fields.Char('Izena', required=True)
    tipo = fields.Selection([
        ('ordenador', 'Ordenagailua'),
        ('pantalla', 'Pantaila')
    ], string='Mota')
    aula_id = fields.Many2one('zubiri.aula', string='Aula')
    alumno_id = fields.Many2one('zubiri.alumno', string='Ikaslea')
    alumno_ordenador_ids = fields.One2many(
        'zubiri.alumno',
        'ordenador_id',
        string='Ikasleak (ordenagailua)',
        readonly=True
    )
    alumno_pantalla_ids = fields.One2many(
        'zubiri.alumno',
        'pantalla_id',
        string='Ikasleak (pantaila)',
        readonly=True
    )
    alumno_multi_ids = fields.Many2many(
        'zubiri.alumno',
        string='Ikasleak',
        compute='_compute_alumno_multi_ids',
        inverse='_inverse_alumno_multi_ids',
        store=False
    )

    def _sync_alumno_links(self, _old_alumno, _old_tipo):
        """Keep alumno <-> equipo links consistent when editing the equipo.

        Do not desasignar alumnos previos; solo añadimos el vínculo al alumno actual.
        """
        self.ensure_one()
        alumno = self.alumno_id

        if alumno:
            if self.tipo == 'ordenador' and alumno.ordenador_id != self:
                alumno.sudo().write({'ordenador_id': self.id})
            if self.tipo == 'pantalla' and alumno.pantalla_id != self:
                alumno.sudo().write({'pantalla_id': self.id})

    def _compute_alumno_multi_ids(self):
        for rec in self:
            if rec.tipo == 'ordenador':
                rec.alumno_multi_ids = rec.alumno_ordenador_ids
            elif rec.tipo == 'pantalla':
                rec.alumno_multi_ids = rec.alumno_pantalla_ids
            else:
                rec.alumno_multi_ids = False

    def _inverse_alumno_multi_ids(self):
        for rec in self:
            alumnos = rec.alumno_multi_ids
            if rec.tipo == 'ordenador':
                for alumno in alumnos:
                    if alumno.ordenador_id != rec:
                        alumno.sudo().write({'ordenador_id': rec.id})
            elif rec.tipo == 'pantalla':
                for alumno in alumnos:
                    if alumno.pantalla_id != rec:
                        alumno.sudo().write({'pantalla_id': rec.id})

    @api.model
    def create(self, vals):
        records = super().create(vals)
        for record in records:
            record._sync_alumno_links(False, vals.get('tipo'))
        return records

    def write(self, vals):
        old_state = {
            rec.id: {'alumno': rec.alumno_id, 'tipo': rec.tipo}
            for rec in self
        }

        res = super().write(vals)

        for rec in self:
            old = old_state[rec.id]
            rec._sync_alumno_links(old['alumno'], old['tipo'])

        return res