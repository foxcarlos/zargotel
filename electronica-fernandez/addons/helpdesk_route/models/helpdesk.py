# -*- coding: utf-8 -*-

from odoo import models, fields, api


class helpdesk_route(models.Model):

    _inherit = "repair.order"
    
    route = fields.Many2one('route.route')
