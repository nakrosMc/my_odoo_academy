from odoo import _, api, fields, models, tools

class HostelStage(models.Model):
    _name = 'hostel.stage'
    _description = 'Hostel Stage' 
    _order = 'sequence, name'

    name = fields.Char("Name")
    sequence = fields.Integer("Sequence")
    fold = fields.Boolean("Fold?")
