from odoo import models, fields, api


class Event(models.Model):
    _name = 'zubiri.event'
    _description = 'Egutegia'

    name = fields.Char('Izenburua', required=True)
    start_datetime = fields.Datetime('Hasiera', required=True)
    end_datetime = fields.Datetime('Amaiera', required=True)
    description = fields.Text('Deskribapena')
    alumno_id = fields.Many2one('zubiri.alumno', string='Ikaslea', ondelete='cascade')
    is_school = fields.Boolean('Eskolako ekitaldia', default=False)

    @api.model
    def create(self, vals):
        user = self.env.user
        student_group = self.env.ref('zubiri.group_zubiri_ikasle')
        if user and student_group in user.groups_id:
            # For students: force personal event and bind to their alumno
            vals = dict(vals)
            vals['is_school'] = False
            if not vals.get('alumno_id'):
                alumno = self.env['zubiri.alumno'].search([('user_id', '=', user.id)], limit=1)
                if alumno:
                    vals['alumno_id'] = alumno.id
        return super().create(vals)

    def write(self, vals):
        user = self.env.user
        student_group = self.env.ref('zubiri.group_zubiri_ikasle')
        if user and student_group in user.groups_id:
            # Students cannot convertir en evento escolar ni reasignar a otro alumno
            vals = dict(vals)
            vals.pop('is_school', None)
            vals.pop('alumno_id', None)
        return super().write(vals)
