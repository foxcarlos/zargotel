# -*- coding: utf-8 -*-

import logging
from odoo.exceptions import UserError
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class HelpdeskToRepair(models.TransientModel):

    _name = 'helpdesk.repair.wizard'
    _description = 'Wizard helpdesk_to_repair'

    t_ticket_id = fields.Char(string='HelpDesk Ticket')
    t_number = fields.Char(string='HelpDesk Number')
    t_name = fields.Char(string='HelpDesk name')
    r_name = fields.Char(string='Repair number')
    r_priority = fields.Selection([('0', 'Normal'), ('1', 'Urgent')])
    r_description = fields.Text(string='Repair description')
    r_product_id = fields.Many2one('product.product', string='Product to repair')
    r_product_qty = fields.Integer(string='Product quantity')
    r_partner_id = fields.Many2one('res.partner', string='Client')
    r_sale_order_id = fields.Many2one('sale.order', 'Order id')
    r_user_id = fields.Many2one('res.users', 'Responsible person')
    r_schedule_date = fields.Date()
    r_location_id = fields.Many2one('stock.location', 'Location')
    r_guarantee_limit = fields.Date()
    r_invoiced_method = fields.Selection([
        ('none', 'without invoice'),
        ('b4repair', 'Before repair'),
        ('after_repair', 'After Repair')], 'invoiced_method')
    r_tag_ids = fields.Many2many('repair.tags', string='Repair tags')
    r_route_id = fields.Many2one('route.route', 'Route')

    @api.onchange('r_partner_id')
    def _onchange_r_partner_id(self):
        """Allows you to change the route_id domain according to the partner that you have."""

        if not self.r_partner_id:
            return []

        res = {}
        res_city_zip_ids = []
        zip_ids = []
        res_city_zip = self.env['res.city.zip']

        for child in self.r_partner_id.child_ids if self.r_partner_id.child_ids else []:
            if child.type == 'delivery':
                postal_code = child.name[1:]
                res_city_zip_ids = res_city_zip.search([('name', '=', postal_code)])

        if res_city_zip_ids:
            zip_ids = res_city_zip_ids.ids

        res['domain'] = {'r_route_id': [('zip', 'in', zip_ids)]}
        return res

    @api.model
    def apply(self, vals):
        """Export data."""

        wizard_ticket_id = self.search([('id', 'in', vals)])

        values = {
            'ticket_id': int(wizard_ticket_id.t_ticket_id),
            'name': wizard_ticket_id.t_number,
            'priority': wizard_ticket_id.r_priority,
            'description': wizard_ticket_id.r_description,
            'product_id': wizard_ticket_id.r_product_id.id,
            'product_uom': wizard_ticket_id.r_product_id.uom_id.id,
            'product_qty': wizard_ticket_id.r_product_qty,
            'partner_id': wizard_ticket_id.r_partner_id.id if wizard_ticket_id.r_partner_id else None,
            'sale_order_id': wizard_ticket_id.r_sale_order_id.id or None,
            'user_id': wizard_ticket_id.r_user_id.id or None,
            'schedule_date': wizard_ticket_id.r_schedule_date,
            'location_id': wizard_ticket_id.r_location_id.id,
            'guarantee_limit': wizard_ticket_id.r_guarantee_limit,
            'invoice_method': wizard_ticket_id.r_invoiced_method,
            'tag_ids': [[6, False, wizard_ticket_id.r_tag_ids.ids]],
            'route': wizard_ticket_id.r_route_id.id or None,
        }

        try:
            self.env['repair.order'].create(values)
            ticket_id = self.env['helpdesk.ticket'].browse(int(wizard_ticket_id.t_ticket_id))
            ticket_id.write({'stage_id': 2})
        except Exception as error:
            _logger.error('%s', error)
            raise UserError('%s', error)

        return True


