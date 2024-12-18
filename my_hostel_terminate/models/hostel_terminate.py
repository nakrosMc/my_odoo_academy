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
        if not self.user_has_groups('my_hostel.group_hostel_manager'):
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


    def name_get(self):
        result = []
        for room in self:
            member = room.partner_ids.mapped('name')
            name = f"{room.name} ({', '.join(member)})"
            result.append((room.id, name))
        return result

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


class RoomCategory(models.Model):
    _inherit = 'hostel.category'

    max_allow_days = fields.Integer(
        'Maximum allows days',
        help="For how many days room can be assigned",
        default=10)
