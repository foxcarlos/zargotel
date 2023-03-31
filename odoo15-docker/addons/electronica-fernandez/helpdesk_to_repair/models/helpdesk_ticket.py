# -*- coding: utf-8 -*-

import logging
from bs4 import BeautifulSoup

from odoo.exceptions import UserError, ValidationError
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class HelpdeskTicketTag(models.Model):
    _inherit = "helpdesk.ticket.tag"

    def create(self, vals):
        self.env['repair.tags'].create_or_get_tag_repair([vals['name']])
        res = super().create(vals)
        return res

    def write(self, vals):
        self.env['repair.tags'].create_or_get_tag_repair([vals['name']])
        res = super().write(vals)
        return res


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    def search_tags_name(self, list_ids):
        """Search tag name for ids passed."""

        list_ids = list_ids or []
        tag_names = []
        if list_ids:
            tag_ids = self.env['helpdesk.ticket.tag'].search([('id', 'in', list_ids)])
            if tag_ids:
                tag_names = tag_ids.mapped('name')
        return tag_names

    @staticmethod
    def _get_author(message_ids):
        """Get authos from email in message_ids list."""

        author_id = None
        for message in message_ids:
            if message.author_id:
                author_id = message.author_id
                break
        return author_id

    @staticmethod
    def _parse_description(message_ids):
        """Parse description, removes the html tags and takes only tienda, centro and direccion."""

        description = ''
        for message in message_ids:
            store_pos = message.body.find('Tienda:')
            center_pos = message.body.find('Centro:')
            address_pos = message.body.find('Direcc')
            location_pos = message.body.find('Localidad')

            store_html = message.body[store_pos: center_pos]
            center_html = message.body[center_pos: address_pos]
            address_html = message.body[address_pos: location_pos]

            if store_pos > 0:
                store_soup = BeautifulSoup(store_html, "html.parser")
                center_soup = BeautifulSoup(center_html, "html.parser")
                address_soup = BeautifulSoup(address_html, "html.parser")

                store_text = store_soup.get_text() + '\n'
                center_text = center_soup.get_text() + '\n'
                address_text = address_soup.get_text() + '\n'
                description = f'{store_text} {center_text} {address_text}'
                break
        return description

    def open_wizard(self):
        """Open wizard form."""

        wizard_view = self.env.ref('helpdesk_to_repair.view_helpdesk_repair_wizard_form')
        context = dict(self.env.context, field1=self._context['default_ticket_id'])
        wizard_view.with_context(context).write({})

        ticket_id = self._context['default_ticket_id']
        number = self._context["default_number"]
        name = self._context["default_name"]
        user_id = self._context["default_user_id"]
        priority = self._context["default_priority"] or 0

        # priority for model repairs
        if int(priority) > 1:
            priority = '1'
        else:
            priority = '0'
        partner_id = self._context["default_partner_id"] or []

        # DEFINE TAGS HelpDesk and Repair
        tag_ids = self._context["default_tag_ids"]
        tag_names = self.search_tags_name(tag_ids[0][2])
        tag_list_id = self.env['repair.tags'].create_or_get_tag_repair(tag_names)

        #  DEFINE DESCRIPTION
        message_ids = self.message_ids.filtered(lambda m: m.message_type == 'email')
        description = self._parse_description(message_ids)
        author_id = self._get_author(message_ids) or []

        if not partner_id and not author_id:
            raise ValidationError(_('''The contact is mandatory, as a general rule the contact is taken from 
            the person who sent the e-mail to generate the ticket, 
            if this is not possible please add the contact manually.'''))

        return {
            'name': 'Export data from Helpdesk to Repair',
            'type': 'ir.actions.act_window',
            'res_model': 'helpdesk.repair.wizard',
            'view_mode': 'form',
            'view_id': wizard_view.id,
            'context': {
                'default_t_ticket_id': ticket_id,
                'default_t_number': number,
                'default_t_name': name,
                'default_r_user_id': user_id,
                'default_r_priority': priority,
                'default_r_partner_id': partner_id or author_id,
                'default_r_tag_ids': [[6, False, tag_list_id]],
                'default_r_description': description,
            },
            'target': 'new',
        }
