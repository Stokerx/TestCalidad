from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PosConfig(models.Model):
    _inherit = 'pos.config'

    @api.onchange('picking_type_id')
    def _onchange_picking_type_id(self):
        """Validar que el tipo de recolección sea de tipo 'outgoing'."""
        if not self.picking_type_id:
            return

        if self.picking_type_id.code != 'outgoing':
            self.picking_type_id = False
            return {
                'warning': {
                    'title': 'Tipo de Recolección Inválido',
                    'message': 'El tipo de recolección debe ser "Entrega"'
                }
            }
        
        return {'domain': {'picking_type_id': [('id', '=', self.picking_type_id.id)]}}

    @api.constrains('start_category')
    def _check_start_category(self):
        """Validar que la categoría de inicio esté en las categorías disponibles."""
        for config in self:
            if not (config.iface_available_categ_ids and config.start_category):
                continue
                
            if config.start_category not in config.iface_available_categ_ids:
                raise ValidationError(
                    "La categoría de inicio '%s' debe estar entre las categorías disponibles." 
                    % config.start_category.name
                )