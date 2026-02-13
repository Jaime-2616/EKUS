from odoo import models, fields, api

class Alumno(models.Model):
    _name = 'zubiri.alumno'
    _description = 'Alumno'

    name = fields.Char('Izena', required=True)
    email = fields.Char('Emaila')
    ciclo = fields.Selection([
        ('ms', 'MS'),
        ('ssa', 'SSA'),
        ('wg', 'WG'),
        ('paag', 'PAAG')
    ], string='Cikloa', required=True, default='ms')
    ordenador_id = fields.Many2one(
        'zubiri.equipo',
        string='Ordenagailua',
        domain=[('tipo', '=', 'ordenador')]
    )
    pantalla_id = fields.Many2one(
        'zubiri.equipo',
        string='Pantaila',
        domain=[('tipo', '=', 'pantalla')]
    )
    asistencia = fields.Integer('Asistentziak')
    nota = fields.Float('Nota')
    profesor_id = fields.Many2one('zubiri.profesor', string='Irakaslea')
    user_id = fields.Many2one('res.users', string='Erabiltzailea')
    event_ids = fields.One2many(
        'zubiri.event',
        'alumno_id',
        string='Egutegia (pertsonala)'
    )
    school_event_ids = fields.Many2many(
        'zubiri.event',
        string='Eskola egutegia',
        compute='_compute_school_event_ids',
        store=False
    )

    def _update_equipment_links(self, old_equipment, new_equipment):
        """Keep the reverse link on the equipment consistent with the alumno.

        Use sudo to avoid permission issues when the user cannot write on equipos.
        """
        if old_equipment and old_equipment != new_equipment:
            old_equipment.sudo().write({'alumno_id': False})
        if new_equipment and old_equipment != new_equipment:
            new_equipment.sudo().write({'alumno_id': self.id})

    def _ensure_user_account(self):
        """Create or update the portal user linked to this alumno."""
        self.ensure_one()
        if not self.email:
            return False

        Users = self.env['res.users'].sudo()
        student_group = self.env.ref('zubiri.group_zubiri_ikasle')
        base_group = self.env.ref('base.group_user')
        group_ids = [student_group.id, base_group.id]

        user = Users.search([('login', '=', self.email)], limit=1)

        if user:
            missing_groups = [gid for gid in group_ids if gid not in user.groups_id.ids]
            if missing_groups:
                user.write({'groups_id': [(4, gid) for gid in missing_groups]})

            updates = {}
            if user.name != self.name:
                updates['name'] = self.name
            if user.email != self.email:
                updates['email'] = self.email
            if updates:
                user.write(updates)
        else:
            user = Users.create({
                'name': self.name,
                'login': self.email,
                'email': self.email,
                'groups_id': [(6, 0, group_ids)],
            })
            user.with_context(no_reset_password=True).write({'password': self.email})

        return user

    @api.model
    def create(self, vals):
        records = super().create(vals)
        for record in records:
            record._update_equipment_links(False, record.ordenador_id)
            record._update_equipment_links(False, record.pantalla_id)
            user = record._ensure_user_account()
            if user:
                record.sudo().write({'user_id': user.id})
        return records

    def write(self, vals):
        old_links = {
            record.id: {
                'ordenador': record.ordenador_id,
                'pantalla': record.pantalla_id,
            }
            for record in self
        }

        res = super().write(vals)

        for record in self:
            old = old_links[record.id]
            if 'ordenador_id' in vals:
                record._update_equipment_links(old['ordenador'], record.ordenador_id)
            if 'pantalla_id' in vals:
                record._update_equipment_links(old['pantalla'], record.pantalla_id)

        if any(key in vals for key in ['email', 'name']):
            for record in self:
                user = record._ensure_user_account()
                if user and record.user_id != user:
                    record.sudo().write({'user_id': user.id})

        # Ensure legacy students without user_id get linked once they have an email.
        for record in self:
            if not record.user_id and record.email:
                user = record._ensure_user_account()
                if user:
                    record.sudo().write({'user_id': user.id})

        return res

    def _compute_school_event_ids(self):
        events = self.env['zubiri.event'].search([('is_school', '=', True)])
        for rec in self:
            rec.school_event_ids = events

    def init(self):
        """Backfill user links for existing alumnos so their self view works."""
        alumnos = self.search([('email', '!=', False), ('user_id', '=', False)])
        for alumno in alumnos:
            user = alumno._ensure_user_account()
            if user:
                alumno.sudo().write({'user_id': user.id})