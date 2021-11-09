# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError, ValidationError
from collections import OrderedDict
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)


class PortalContact(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'contact_count' in counters:
            # request.env.user.partner_id.id
            partner_id = request.env.user.partner_id
            contact_count = request.env['res.partner'].search_count([
                ('parent_agent', '=', partner_id.id),
            ])
            values['contact_count'] = contact_count
        return values
    # ------------------------------------------------------------
    # My Contacts
    # ------------------------------------------------------------

    # def _contact_get_page_view_values(self, contact, access_token, **kwargs):
    #     values = {
    #         'page_name': 'contact',
    #         'contact': contact,
    #     }
    #     return self._get_page_view_values(contact, access_token, values, 'my_contacts_history', False, **kwargs)

    @http.route(['/my/contacts', '/my/contacts/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_contacts(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        partner_id = request.env.user.partner_id
        partners = request.env['res.partner'].sudo()
        contacts = partners.search([
            ('parent_agent', '=', partner_id.id),
        ])
        _logger.info(contacts)
        values = self._prepare_portal_layout_values()

        domain = [('parent_agent', '=', partner_id.id)]

        # count for pager
        contact_count = partners.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/contacts",
            # url_args={'date_begin': date_begin,
            #           'date_end': date_end, 'sortby': sortby},
            total=contact_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        contacts = partners.search(
            domain,
            # order=order,
            limit=self._items_per_page, offset=pager['offset'])
        request.session['my_contacts_history'] = contacts.ids[:100]

        values.update({
            'date': date_begin,
            'contacts': contacts,
            'page_name': 'contact',
            'pager': pager,
            'default_url': '/my/contacts',
        })
        return request.render("cl.portal_my_contacts", values)

    @http.route(['/my/contacts/<int:partner_id>'], type='http', auth="public", website=True)
    def portal_my_partner_detail(self, partner_id, access_token=None, report_type=None, download=False, **kw):
        contact = request.env['res.partner'].sudo().search(
            [('id', '=', partner_id)])
        values = {'contact': contact, }
        return request.render("cl.portal_contact_page", values)

    @http.route("/my/contacts/new", auth="user", website=True)
    def portal_my_contacts_new(self, **kw):
        """Form to create a contact."""
        return self.portal_my_contacts_read(request.env["res.partner"].new())

    @http.route("/my/contacts/<int:partner_id>/edit",
                auth="user", website=True)
    def portal_my_contacts_edit(self, partner_id):
        """Form to edit a contact."""
        contact = request.env['res.partner'].sudo().search(
            [('id', '=', partner_id)])
        return self.portal_my_contacts_read(contact)

    @http.route("/my/contacts/create",
                auth="user", website=True)
    def portal_my_contacts_create(self, redirect="/my/contacts/{}", **post):
        """Create a contact."""
        values = self._contacts_fields()
        # values = self._contacts_clean_values(kwargs)
        _logger.info("Creating contact with: %s", values)
        _logger.info("Creating contact with: %s", post)
        partner_id = post['id']
        post.update(
            {'parent_agent': request.env.user.partner_id.id,
             'vendor_type': 'seller'})
        if partner_id:
            post.pop('id')
            partner = request.env['res.partner'].browse(int(partner_id))
            contact = partner.write(post)
        else:
            contact = request.env["res.partner"].create(post)
        _logger.info('Created with this ID: %s', contact)
        return request.redirect(redirect.format(partner_id))

    @http.route("/my/contacts/<model('res.partner'):contact>",
                auth="user", website=True)
    def portal_my_contacts_read(self, contact):
        """Read a contact form."""
        # values = self._contacts_fields()
        values = {
            "partner": contact,
            "fields": self._contacts_fields(),
        }
        return request.render(
            "cl.contacts_followup", values)

    def _contacts_fields_check(self, received):
        """Check received fields match those available."""
        disallowed = set(received) - set(self._contacts_fields())
        if disallowed:
            raise ValidationError(
                _("Fields not available: %s") % ", ".join(disallowed))

    def _contacts_fields(self):
        """Fields to display in the form."""
        return [
            "id",
            "name",
            "phone",
            "mobile",
            "email",
            "comment"
        ]
