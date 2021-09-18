from odoo import api, fields, models


class Res_Partner_CL(models.Model):
    _inherit = 'res.partner'
    vendor_type = fields.Selection([
        ('agent', 'Agent'),
        ('seller', 'Seller'), 
    ], string='Vendor', default='agent')
    parent_agent = fields.Many2one('res.partner', string='Agent')