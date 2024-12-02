from odoo import fields, models, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    is_hostel_rector = fields.Boolean("Hostel Rector", help="Activa si la persona es rector de un hostal")
    assign_room_ids = fields.Many2many('hostel.room', string='Authored Books')
    count_assign_room = fields.Integer('Number of Authored Books', compute="_compute_count_room")

    @api.depends('assign_room_ids')
    def _compute_count_room(self):
        for partner in self:
            partner.count_assign_room = len(partner.assign_room_ids)
