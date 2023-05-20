# -*- coding: utf-8 -*-

import logging
from odoo.exceptions import UserError
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class RepairOrder(models.Model):
    _inherit = "repair.order"

    ticket_id = fields.Many2one('helpdesk.ticket', string='Ticket ID')

    def write(self, vals):
        """If state == done , then close ticket."""

        state = vals.get('state', False)
        if state == 'done':
            val_ticket_id = self.env['helpdesk.ticket'].browse(self.ticket_id.id)
            if val_ticket_id:
                val_ticket_id.write({'stage_id': 4})
        res = super().write(vals)
        return res


class RepairTag(models.Model):
    _inherit = "repair.tags"

    def create_or_get_tag_repair(self, tag_names):
        """Create tag repair or get id list
            params: string list name
            Example: ['Fail', 'Computer', ]
        """

        if not isinstance(tag_names, list):
            return []

        response_list_id = []
        for tag in tag_names:
            domain = [('name', '=', tag)]
            searched = self.search(domain).mapped('id')
            if searched:
                response_list_id.append(searched)
            else:
                response_list_id.append(self.create({'name': tag}))

        return response_list_id
