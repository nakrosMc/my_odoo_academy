from odoo import fields, models, api

class Hostel(models.Model):
    _name = 'hostel.hostel'
    _description = "Información sobre el hostel"
    _order = "id desc, name"
    _rec_name = 'hostel_code'
    
    name = fields.Char(string="Nombre del hostel", required=True)
    hostel_code = fields.Char(string="Código", required=True)
    street = fields.Char('Calle')
    street2 = fields.Char('Calle2')
    zip = fields.Char('Código Postal', change_default=True)
    city = fields.Char('Ciudad')
    state_id = fields.Many2one("res.country.state", string='Estado')
    country_id = fields.Many2one('res.country', string='País')
    phone = fields.Char('Teléfono', required=True)
    mobile = fields.Char('Móvil', required=True)
    email = fields.Char('Correo electrónico')
    hostel_floors = fields.Integer(string="Total Floors")
    image = fields.Binary('Hostel Image')
    active = fields.Boolean("Active", default=True, help="Activate/Deactivate hostel record")
    type = fields.Selection(
        [("male", "Boys"), ("female", "Girls"), ("common", "Common")], 
        "Type", help="Type of Hostel", required=True, default="common"
    )
    other_info = fields.Text("Other Information", help="Enter more information")
    description = fields.Html('Description')
    hostel_rating = fields.Float('Hostel Average Rating',
        digits='Rating Value'
    )
    category_id = fields.Many2one('hostel.category', string="Category")

    ref_doc_id = fields.Reference(
    selection="_referencable_models",
    string="Reference Document"
)


    @api.model
    def _referencable_models(self):
        models_obj = self.env["ir.model"]
        print(models)
        models_ids = models_obj.search([("field_id.name", "=", "message_ids")])
        print(models_ids)
        return [(x.model, x.name) for x in models_ids]