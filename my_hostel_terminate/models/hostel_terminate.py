from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError

class HostelRoom(models.Model):
    _inherit = 'hostel.room'

    remarks = fields.Text('Remarks')

    date_terminate = fields.Date('Date of Termination')
    category_id = fields.Many2one("hostel.category", string="Category")

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


class RoomCategory(models.Model):
    _inherit = 'hostel.category'

    max_allow_days = fields.Integer(
        'Maximum allows days',
        help="For how many days room can be assigned",
        default=10)
