from odoo import fields, models, api, _
import logging
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class HostelRoomCopy(models.Model):
    _name = "hostel.room.copy"
    _inherit = "hostel.room"
    _description = "Hostel Room Information Copy"

    
    hostel_amenities_ids = fields.Many2many("hostel.amenities",
        "hostel_room_copy_amenities_rel", 
        "room_id", "amenitiy_id",
        string="Amenities", 
        domain="[('active', '=', True)]",
        help="Select hostel room amenities")


    def filter_members(self):
        all_rooms = self.search([])  # Busca todas las habitaciones
        filtered_rooms = self.rooms_with_multiple_members(all_rooms)  # Filtra las habitaciones con múltiples miembros
        _logger.info(filtered_rooms)  # Devuelve el resultado filtrado

    @api.model
    def rooms_with_multiple_members(self, all_rooms):
        def predicate(room):
            if len(room.partner_ids) > 1:  # Verifica si la habitación tiene más de un miembro
                return True
            return False

        return all_rooms.filtered(predicate)  # Aplica el filtro y devuelve las habitaciones que cumplen la condición

    @api.model
    def get_hostel_names(self, all_rooms):
        return all_rooms.mapped('name')

    def mapped_rooms(self):
        all_rooms = self.search([])
        room_authors = self.get_hostel_names(all_rooms)
        _logger.info(f'Room Members: {room_authors}')

    def sort_room(self):
        all_rooms = self.search([])
        room_sort = self.sort_rooms_by_rating(all_rooms)
        _logger.info(room_sort)

    @api.model
    def sort_rooms_by_rating(self, all_rooms):
        orden_rent = all_rooms.sorted(key='rent_amount')
        return orden_rent.mapped('name')



