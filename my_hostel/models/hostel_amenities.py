from odoo import models, fields

class HostelAmenities(models.Model):
    _name = "hostel.amenities"
    _description = "Hostel Amenities"

    name = fields.Char(string="Name", help="Provided Hostel Amenity")
    active = fields.Boolean("Active", 
                            help="Activate/Deactivate whether the amenity should be given or not")
