from odoo import http
from odoo import exceptions, models
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _auth_method_base_group_user(cls):
        cls._auth_method_user()
        if not request.env.user.has_group('base.group_user'):
            raise exceptions.AccessDenied()

    # this is for the exercise
    @classmethod
    def _auth_method_groups(cls, group_xmlids=None):
        cls._auth_method_user()
        if not any(map(request.env.user.has_group, group_xmlids or [])):
            raise exceptions.AccessDenied()