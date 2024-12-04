from odoo import fields, models

class HostelRoomMember(models.Model):
    _name = 'hostel.room.member'
    _description = 'Hostel room member date'

    name  = fields.Char(string='name')