# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class c:\users\vojd\projects\addons\empty(models.Model):
#     _name = 'c:\users\vojd\projects\addons\empty.c:\users\vojd\projects\addons\empty'
#     _description = 'c:\users\vojd\projects\addons\empty.c:\users\vojd\projects\addons\empty'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
