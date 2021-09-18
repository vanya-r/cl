from odoo import api, fields, models


class Product_template_CL(models.Model):
    _inherit = 'product.template'

    id_cl = fields.Char(string='ID')
    name_in_contract = fields.Char(string='Name In Contract')
    email = fields.Char(string='E-Mail')
    status_cl = fields.Selection(string='Status', selection=[('Deposit Approved', 'approved'), ('Deposit Denied', 'denied'),])
    address = fields.Char(string='Address')
    agent = fields.Many2one(comodel_name='res.partner', string='Agent')
    dd_days = fields.Integer(string='DD Days')
    apn_1 = fields.Char(string='APN #1')
    apn_2 = fields.Char(string='APN #2')
    # currency_id_company = fields.Many2one('res.currency', 'Currency', compute='_compute_currency_id')    
    deposit_amount = fields.Monetary(string='Deposit Amount', currency_field='currency_id')

    
    # def _compute_currency_id(self):
    #     main_company = self.env['res.company'].sudo().search([], limit=1, order="id")
    #     for template in self:
    #         template.currency_id_company = main_company.currency_id.id