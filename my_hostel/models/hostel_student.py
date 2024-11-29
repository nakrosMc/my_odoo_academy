from odoo import fields, models

class HostelStudent(models.Model):
    _name = "hostel.student"
    _description = 'Hostel for student'

    name = fields.Char('Student Name')

    gender = fields.Selection([('male', 'MALE'), ('female', 'Female'), ('other', 'Other')], string='Gender', help='Student gender')
    

    activate = fields.Boolean(
        'Activate',
        default=True,
        help='Activate/Deactivate hostel record'
    )

    room_id = fields.Many2one(
        'hostel.room',
        string='Room',
        help='Select hostel room'
        )

    hostel_id = fields.Many2one("hostel.hostel", related="room_id.hostel_id")