from os.path import join as opj
from odoo import models, api, exceptions
import logging

_logger = logging.getLogger(__name__)


EXPORTS_DIR = opj(os.path.dirname(__file__), 'export')

class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    @api.model
    def export_stock_level(self, stock_location):
        _logger.info(f'export stock level for {stock_location.name}')
        products = self.with_context(location=stock_location.id).search([])
        products = products.filtered('qty_available')
        _logger.debug(f'{len(products)} products in the location')
        fname = opj(EXPORTS_DIR, 'stock_level.txt')
        
        try:
            with open(fname, 'w') as fobj:
                for prod in products:
                    fobj.write(f'{prod.name}\t{prod.qty_available}\n')
        except IOError:
            _logger.exception('Error while writing to %s in %s', 'stock_level.txt', EXPORTS_DIR)
            raise exceptions.UserError('unable to save file')

