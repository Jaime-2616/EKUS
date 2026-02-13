# -*- coding: utf-8 -*-
{
    'name': "Gestión de Coches",
    'summary': "Módulo para gestión de vehículos y garaje",
    'description': """
        Este módulo permite gestionar un inventario de coches.
        Incluye:
        - Registro de vehículos con características técnicas
        - Gestión de marcas y modelos
        - Control de mantenimiento
        - Seguimiento de estado y disponibilidad
    """,
    'author': "Jaime",
    'website': "",
    'category': 'Automotive',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/coche_views.xml',
        'views/marca_views.xml',
        'views/mantenimiento_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
}