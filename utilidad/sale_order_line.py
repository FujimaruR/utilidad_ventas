from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_average_margin_percentage(self):
        sale_price = discount = cost = margin_amount = 0.0
        line_cost = line_margin_amount = margin_percentage = 0.0
        for record in self:
            if record.order_line:
                for line in record.order_line:
                    line.costo = line.product_id.standard_price * line.qty
                    precio_venta_con_impuestos = line.price_unit * (1 + (line.tax_id.amount / 100))
                    costo = 0.0
                    utilidadm = 0.0
                    sale_price = line.price_unit * line.product_uom_qty
                    discount = (sale_price * line.discount) / 100
                    costo = line.product_id.standard_price * line.product_uom_qty
                    line.margen = (sale_price - discount) - costo


    def action_confirm(self):
       for order in self:
          order._get_average_margin_percentage()
       res = super(SaleOrder, self).action_confirm()
       return res


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    costo = fields.Float("Costo")
    margen = fields.Float("Margen")






