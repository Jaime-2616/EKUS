from odoo import models, fields, api

class Profesor(models.Model):
    _name = 'zubiri.profesor'
    _description = 'Profesor'

    name = fields.Char('Izena', required=True)
    email = fields.Char('Emaila')
    alumnos_ids = fields.One2many('zubiri.alumno', 'profesor_id', string='Ikasleak')
    user_id = fields.Many2one('res.users', string='Erabiltzailea')

    def _ensure_user_account(self):
        """Create or update the portal user linked to this profesor."""
        self.ensure_one()
        if not self.email:
            return False

        Users = self.env['res.users'].sudo()
        teacher_group = self.env.ref('zubiri.group_zubiri_profesor')
        base_group = self.env.ref('base.group_user')
        group_ids = [teacher_group.id, base_group.id]

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
            user = record._ensure_user_account()
            if user:
                record.sudo().write({'user_id': user.id})
        return records

    def write(self, vals):
        res = super().write(vals)
        if any(key in vals for key in ['email', 'name']):
            for record in self:
                user = record._ensure_user_account()
                if user and record.user_id != user:
                    record.sudo().write({'user_id': user.id})
        return res