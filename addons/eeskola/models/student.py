from odoo import models, fields

class EeskolaStudent(models.Model):
    _name = 'eeskola.student'
    _description = 'Eeskola Student'
    _rec_name = 'name'

    name = fields.Char(string='Izena', required=True)
    surname = fields.Char(string='Abizena')
    student_age = fields.Integer(string='Adina')
    student_day_of_birth = fields.Date(string='Jaiotze data')
    student_gender = fields.Selection([
        ('m', 'Gizona'),
        ('f', 'Emakumea'),
        ('o', 'Beste')
    ], string='Generoa')
    student_blood_group = fields.Selection([
        ('A+', 'A+ve'), ('B+', 'B+ve'), ('O+', 'O+ve'), ('AB+', 'AB+ve'),
        ('A-', 'A-ve'), ('B-', 'B-ve'), ('O-', 'O-ve'), ('AB-', 'AB-ve')
    ], string='Odol taldea')