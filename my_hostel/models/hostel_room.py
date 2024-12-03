from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError
from odoo.tools.translate import _


class HostelRoom(models.Model):
    _name = "hostel.room"
    _description = 'amount of coins'
    _inherit = ['base.archive']
    

    name = fields.Char(string='Room name', required=True)
    room_num  = fields.Integer(string='Room No.')
    floor_num  = fields.Integer(string='Floor No.')

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency'
    )

    rent_amount = fields.Monetary(
        'Rent Amount', 
        help="Enter rent amount per month", 
        # currency_field='currency_id'  # opcional si el campo de moneda tiene otro nombre distinto a 'currency_id'
    )

    hostel_id = fields.Many2one(
        'hostel.hostel',
        'Hostel',
        help='Name of hostel'
    )

    studens_ids = fields.One2many('hostel.student', 'room_id',
        string='Studens', help='Enter students')

    hostel_amenities_ids = fields.Many2many("hostel.amenities",
        "hostel_room_amenities_rel", 
        "room_id", "amenitiy_id",
        string="Amenities", 
        domain="[('active', '=', True)]",
        help="Select hostel room amenities")

    student_per_room = fields.Integer(
    "Student Per Room",
    required=True,
    help="Estudiantes asignados por habitación"
    )
    availability = fields.Float(
        compute="_compute_check_availability",
        string="Availability",
        store=True,
        help="Disponibilidad de la habitación en el hostel"
    )

    admission_date = fields.Date(
    "Admission Date",
    help="Fecha de admisión al hostel",
    default=fields.Datetime.today
    )

    discharge_date = fields.Date(
        "Discharge Date",
        help="Fecha de egreso del estudiante"
    )

    duration = fields.Integer(
        "Duration",
        compute="_compute_check_duration",
        inverse="_inverse_duration",
        help="Duración de la estadía"
    )

    partner_ids = fields.Many2many('res.partner', string='Assigned Partners')
    
    state = fields.Selection([
        ('draft', 'unavailable'),
        ('available', 'available'),
        ('closed', 'closed')],
        'State', default="draft")

    @api.depends("student_per_room", "studens_ids")
    def _compute_check_availability(self):
        """Método para calcular la disponibilidad de habitaciones"""
        for rec in self:
            rec.availability = rec.student_per_room - len(rec.studens_ids.ids)

    @api.constrains("rent_amount")
    def _check_rent_amount(self):
        """Restricción para verificar el monto de alquiler negativo"""
        if self.rent_amount < 0:
            raise ValidationError(("¡El monto de alquiler mensual no debe ser un valor negativo!"))

    @api.depends("admission_date", "discharge_date")
    def _compute_check_duration(self):
        """Método para calcular la duración"""
        for rec in self:
            if rec.discharge_date and rec.admission_date:
                rec.duration = (rec.discharge_date - rec.admission_date).days
    
    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [
            ('draft', 'available'),
            ('available', 'closed'),
            ('closed', 'draft')
        ]
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        for room in self:
            if room.is_allowed_transition(room.state, new_state):
                room.state = new_state
            else:
                continue

    def make_available(self):
        self.change_state('available')

    def make_closed(self):
        self.change_state('closed')


    # def make_draft(self):
    #     self.change_state('draft')

    def _inverse_duration(self):
        for stu in self:
            if stu.discharge_date and stu.admission_date:
                duration = (stu.discharge_date - stu.admission_date).days
                if duration != stu.duration:
                    stu.discharge_date = (
                        stu.admission_date + timedelta(days=stu.duration)
                    ).strftime('%Y-%m-%d')

    def change_state(self, new_state):
        for room in self:
            if room.is_allowed_transition(room.state, new_state):
                room.state = new_state
            else:
                msg = _(f'Moving from {room.state} to {new_state} is not allow')
                raise UserError(msg)

    _sql_constraints = [
    ("room_num_unique", "unique(room_num)", "¡El número de habitación debe ser único!")
    ]