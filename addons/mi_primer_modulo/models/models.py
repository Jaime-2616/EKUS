# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date

class Marca(models.Model):
    _name = 'marca'
    _description = 'Marca de Coche'
    _order = 'name'

    name = fields.Char(string='Marca', required=True)
    pais_origen = fields.Char(string='País de Origen')
    fundacion = fields.Integer(string='Año de Fundación')
    descripcion = fields.Text(string='Descripción')
    
    # Relaciones
    coche_ids = fields.One2many('coche', 'marca_id', string='Coches')
    
    # Contador
    total_coches = fields.Integer(string='Total Coches', compute='_compute_total_coches')
    
    @api.depends('coche_ids')
    def _compute_total_coches(self):
        for marca in self:
            marca.total_coches = len(marca.coche_ids)


class Coche(models.Model):
    _name = 'coche'
    _description = 'Coche'
    _rec_name = 'matricula'
    _order = 'matricula'

    # Identificación
    matricula = fields.Char(string='Matrícula', required=True, size=10, help='Matrícula del vehículo')
    vin = fields.Char(string='Número de Chasis (VIN)', size=17, help='Vehicle Identification Number')
    
    # Características
    marca_id = fields.Many2one('marca', string='Marca', required=True)
    modelo = fields.Char(string='Modelo', required=True)
    color = fields.Char(string='Color')
    año_fabricacion = fields.Integer(string='Año de Fabricación')
    
    # Especificaciones técnicas
    tipo_combustible = fields.Selection([
        ('gasolina', 'Gasolina'),
        ('diesel', 'Diésel'),
        ('hibrido', 'Híbrido'),
        ('electrico', 'Eléctrico'),
        ('gpl', 'GPL')
    ], string='Combustible', default='gasolina')
    
    potencia = fields.Integer(string='Potencia (CV)')
    cilindrada = fields.Integer(string='Cilindrada (cc)')
    kilometraje = fields.Integer(string='Kilómetros')
    
    # Estado
    estado = fields.Selection([
        ('nuevo', 'Nuevo'),
        ('usado', 'Usado'),
        ('reparacion', 'En Reparación'),
        ('vendido', 'Vendido')
    ], string='Estado', default='usado')
    
    disponible = fields.Boolean(string='Disponible', default=True)
    fecha_compra = fields.Date(string='Fecha de Compra')
    precio_compra = fields.Float(string='Precio de Compra', digits=(10, 2))
    precio_venta = fields.Float(string='Precio de Venta', digits=(10, 2))
    
    # Campos calculados
    años_antiguedad = fields.Integer(string='Años de Antigüedad', compute='_compute_antiguedad')
    nombre_completo = fields.Char(string='Coche', compute='_compute_nombre_completo')
    
    # Relaciones
    mantenimiento_ids = fields.One2many('mantenimiento', 'coche_id', string='Historial de Mantenimiento')
    
    # Métodos calculados
    @api.depends('año_fabricacion')
    def _compute_antiguedad(self):
        for coche in self:
            if coche.año_fabricacion:
                coche.años_antiguedad = date.today().year - coche.año_fabricacion
            else:
                coche.años_antiguedad = 0
    
    @api.depends('marca_id', 'modelo', 'matricula')
    def _compute_nombre_completo(self):
        for coche in self:
            coche.nombre_completo = f"{coche.marca_id.name if coche.marca_id else ''} {coche.modelo} - {coche.matricula}"
    
    # Restricciones
    _sql_constraints = [
        ('matricula_unique', 'UNIQUE(matricula)', 'La matrícula ya existe en el sistema'),
        ('vin_unique', 'UNIQUE(vin)', 'El número de chasis (VIN) ya existe'),
    ]


class Mantenimiento(models.Model):
    _name = 'mantenimiento'
    _description = 'Mantenimiento de Coche'
    _order = 'fecha desc'

    # Información básica
    name = fields.Char(string='Referencia', required=True, default='Nuevo Mantenimiento')
    coche_id = fields.Many2one('coche', string='Coche', required=True)
    fecha = fields.Date(string='Fecha', default=fields.Date.today)
    kilometros = fields.Integer(string='Kilómetros en el Momento')
    
    # Tipo de mantenimiento
    tipo = fields.Selection([
        ('revision', 'Revisión General'),
        ('cambio_aceite', 'Cambio de Aceite'),
        ('frenos', 'Cambio de Frenos'),
        ('neumaticos', 'Cambio de Neumáticos'),
        ('bateria', 'Cambio de Batería'),
        ('otros', 'Otros')
    ], string='Tipo de Mantenimiento', required=True)
    
    # Detalles
    descripcion = fields.Text(string='Descripción del Trabajo')
    costo = fields.Float(string='Costo', digits=(10, 2))
    taller = fields.Char(string='Taller')
    
    # Estado
    completado = fields.Boolean(string='Completado', default=True)
    
    # Campos relacionados automáticamente
    coche_matricula = fields.Char(string='Matrícula', related='coche_id.matricula', store=True)
    coche_modelo = fields.Char(string='Modelo', related='coche_id.modelo', store=True)