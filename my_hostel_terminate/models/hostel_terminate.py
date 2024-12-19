from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class HostelRoom(models.Model):
    _inherit = 'hostel.room'

    remarks = fields.Text('Remarks')

    date_terminate = fields.Date('Date of Termination')
    category_id = fields.Many2one("hostel.category", string="Category")
    previous_room_id = fields.Many2one('hostel.room', string='Previous Room')

    def make_closed(self):
        day_to_allocate = self.category_id.max_allow_days or 10
        self.date_terminate = fields.Date.today() + timedelta(days=day_to_allocate)
        return super(HostelRoom, self).make_closed()

    def make_available(self):
        self.date_terminate = False
        return super(HostelRoom, self).make_available()

    @api.model_create_multi
    def create(self, values):
        user = self.env.user
        if not user.has_groups('my_hostel.group_hostel_manager'):
            values.get('remarks')
            if values.get('remarks'):
                raise UserError(
                    'You are not allowed to modify '
                    'remarks'
                )
        return super(HostelRoom, self).create(values)

    def write(self, values):
        user = self.env.user
        if not user.has_group('my_hostel.group_hostel_manager'):
            if values.get('remarks'):
                raise UserError(
                    'You are not allowed to modify '
                    'remarks'
                )
        return super(HostelRoom, self).write(values)


    @api.depends('name', 'partner_ids.name')
    def _compute_display_name(self):
        for room in self:
            member = room.partner_ids.mapped('name')
            room.display_name = f"{room.name} ({', '.join(member)})" if member else room.name

    @api.model
    def _name_search(self, name='', args=None, operator='ilike',
                    limit=100, name_get_uid=None):
        args = [] if args is None else args.copy()
        if not (name == '' and operator == 'ilike'):
            args += ['|', '|',
                    ('name', operator, name),
                    ('roon_num', operator, name),
                    ('partner_ids.name', operator, name)]
        return super(HostelRoom, self)._name_search(
            name=name, args=args, operator=operator,
            limit=limit, name_get_uid=name_get_uid)
    
    def group_ave(self):
        average = self._get_average_cost()
        _logger.info(average)

    @api.model
    def _get_average_cost(self):
        grouped_result = self.read_group(
            [('cost_price', "!=", False)],  # Dominio
            ['category_id', 'cost_price:avg'],  # Campos a acceder
            ['category_id']  # group_by
        )
        return grouped_result

    def action_category_with_amount(self):
            # Ejecutamos la consulta SQL para obtener el nombre y la cantidad
        self.env.cr.execute("""
                SELECT
                    hrc.name
                FROM
                    hostel_room AS hostel_room
                JOIN
                    hostel_category AS hrc ON hrc.id = hostel_room.category_id
                WHERE hostel_room.category_id = %(cate_id)s;
            """, {'cate_id': self.category_id.id})
        result = self.env.cr.fetchall()
        _logger.warning("Hostel Room With Amount: %s", result)

            # Obtenemos el resultado de la consulta
        result = self.env.cr.fetchall()

            # Registramos el resultado en el log
        _logger.warning("Hostel Room With Amount: %s", result)

class RoomCategory(models.Model):
    _inherit = 'hostel.category'

    max_allow_days = fields.Integer(
        'Maximum allows days',
        help="For how many days room can be assigned",
        default=10)
