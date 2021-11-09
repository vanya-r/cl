from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)


class Res_Partner_CL(models.Model):
    _inherit = 'res.partner'
    # _inherits = ['res.partner', 'portal.mixin']
    vendor_type = fields.Selection([
        ('agent', 'Agent'),
        ('seller', 'Seller'),
        ('client', 'Client'),
    ], string='Vendor', default='client')
    parent_agent = fields.Many2one('res.partner', string='Agent')

    def get_portal_url(self, suffix=None, report_type=None, download=None, query_string=None, anchor=None):
        self.ensure_one()
        _logger.info(self)
        _logger.info(suffix)
        _logger.info(report_type)
        _logger.info(download)
        _logger.info(query_string)
        _logger.info(anchor)
        return f'/my/contacts/{self.id}'
        # return self.env['portal.mixin'].get_portal_url(suffix=None, report_type=None, download=None, query_string=None, anchor=None)
