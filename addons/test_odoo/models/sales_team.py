from odoo import models, fields

class SalesTeam(models.Model):
    _name = 'sales.team.test'
    _description = 'Equipo de Ventas'

    name = fields.Char(string='Nombre', required=True)