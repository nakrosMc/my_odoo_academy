from odoo import fields, models, api
from odoo.exceptions import UserError

class HostelStudent(models.Model):
    _name = "hostel.student"
    _description = 'Hostel for student'
    _inherits = {'res.partner': 'partner_id'}
    _description = "Hostel Student Information"

    partner_id = fields.Many2one(
        'res.partner',
        ondelete='cascade',
        required=True
    )

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

    allocation_date = fields.Date(string='Date allocation')

    discharge_date = fields.Date(string='Date discharge')

    duration = fields.Integer(string="Duration", default=0)

    @api.onchange('allocation_date', 'discharge_date')
    def onchange_duration(self):
        if self.discharge_date and self.allocation_date:
            self.duration = (
                (self.discharge_date.year - self.allocation_date.year) * 12 +
                (self.discharge_date.month - self.allocation_date.month)
            )


    status = fields.Selection([('paid', 'paid'), ('unpaid', 'unpaid')])

    def action_assign_room(self):
        # Asegúrate de que se está actuando sobre un único registro
        self.ensure_one()

        # Verifica que el estudiante haya pagado antes de asignar una habitación
        if self.status != "paid":
            raise UserError(("You can't assign a room if it's not paid."))

        # Crea un registro de habitación como superusuario
        room_as_superuser = self.env['hostel.room'].sudo()
        room_rec = room_as_superuser.create({
            "name": "Room 103",
            "room_num": "103",
            "floor_num": 1,
            "category_id": 21,
            "hostel_id": self.hostel_id.id,
            "student_per_room" : 1
        })

    def action_remove_room(self):
        if self.env.context.get("is_hostel_room"):
            self.room_id = False

    def action_open_wizard(self):
        self.ensure_one()
        return {
            'name': 'Assign Room',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'assign.room.student.wizard',
            'target': 'new',
        }



