from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError
from odoo.tools.translate import _
import logging

_logger = logging.getLogger(__name__)


class HostelRoom(models.Model):
    _name = "hostel.room"
    _description = 'amount of coins'
    _inherit = ['base.archive']
    
    name = fields.Char(string='Room name', required=True)
    cost_price = fields.Float('Room Cost')
    category_id = fields.Many2one('hostel.category')
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

    # member_ids = fields.Many2many(
    #     comodel_name='res.partner',
    #     relation='hostel_room_member_rel',  # Relación de la tabla intermedia
    #     column1='room_id',  # Nombre de la columna en la tabla intermedia
    #     column2='member_id',  # Nombre de la columna en la tabla intermedia
    #     string='Members'
    # )

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

    def log_all_room_members(self):
        hostel_room_obj = self.env['hostel.room.member']
        all_members = hostel_room_obj.search([])
        print("ALL MEMBERS", all_members)
        return True

    def update_room_no(self):
        self.ensure_one()
        self.room_num = "10"

    def find_room(self):
        domain = [  
            '|',  
            '&', ('name', 'ilike', 'The Penth House'),  
            ('category_id.name', 'ilike', 'prueba'),
            '&', ('name', 'ilike', 'tiburon'),  
            ('category_id.name', 'ilike', 'Parent category')  
            ]  
        rooms = self.search(domain)  
        _logger.info(f'Room found: {rooms}')
        return True

    def find_partner(self):
        partnerObj = self.env['res.partner']
        domain=[
            '&', ('name','ilike','SerpentCS'),
            ('company_id.name','=','SCS')
        ]
        partner = partnerObj.search(domain)
        _logger.info(partner)
        return True

    def get_recordsets(self):
    # Primer conjunto de registros: contactos cuyo nombre contiene "SerpentCS"
        recordset1 = self.env['res.partner'].search([('name', 'ilike', 'SerpentCS')])

    # Segundo conjunto de registros: contactos de una compañía específica
        recordset2 = self.env['res.partner'].search([('company_id.name', '=', 'SCS')])

    # Retornar ambos conjuntos
        return recordset1, recordset2

    def combine_recordsets(self):
    # Obtener los dos recordsets
        recordset1, recordset2 = self.get_recordsets()

    # Unir los recordsets (sin duplicados)
        combined_recordset = recordset1 | recordset2

    # Imprimir los registros combinados
        _logger.info(f"Combined Recordset: {combined_recordset}")
        return combined_recordset

        
    _sql_constraints = [
        ("room_num_unique", "unique(room_num)", "¡El número de habitación debe ser único!")
    ]