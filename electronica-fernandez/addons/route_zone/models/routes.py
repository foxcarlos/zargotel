# -*- coding: utf-8 -*-

from odoo import models, fields, api


class routes_zones(models.Model):
     _name = 'route.zone'
     _description = 'routes zones'

     name = fields.Char()
     description = fields.Text()


class routes_routes(models.Model):
     _name = 'route.route'
     _description = 'Routes'

     name = fields.Char()
     route_zone = fields.Many2one('route.zone', string="Zone")
     zip = fields.Many2one('res.city.zip', string='C.P.')
          