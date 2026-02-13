# -*- coding: utf-8 -*-
{
    'name': 'Eeskola',
    'version': '1.0',
    'summary': 'Eeskola modulua - Ikasleen kudeaketa',
    'category': 'Education',
    'author': 'jaime',
    'depends': ['base'],
    'data': [
        'views/student_views.xml',      
        'security/ir.model.access.csv', 
    ],
    'installable': True,
    'application': True,
}