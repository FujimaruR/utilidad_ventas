import xlsxwriter
from odoo import models

class InvoiceUtilidadXls(models.AbstractModel):
    _name = 'report.utilidad_ventas.invoice_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def get_lines(self, obj):
        lines = []

        domain = [
            ('order_id.date_order', '>=', obj.fecha_ini),
            ('order_id.date_order', '<=', obj.fecha_fin),
            ('state', '!=', 'draft'),
        ]

        if obj.producto:
            domain.append(('product_id', '=', obj.producto.id))

        receipt_ids = self.env['sale.order.line'].search(domain)

        for line in receipt_ids:
            vals = {
                'Producto': line.product_id.name,
                'Lote': line.product_template_id.name,
                'Descripcion': line.name,
                'Cantidad': line.product_uom_qty,
                'Entregado': line.state,
                'Facturado': line.order_partner_id.name,
                'UnidadDemedida': line.product_uom.name,
                'PrecioUnitario': line.price_unit,
                'Impuestos': [(impuesto.name, impuesto.amount) for impuesto in line.tax_id],
                'Descuento': line.discount,
                'Subtotal': line.price_subtotal,
            }
            lines.append(vals)

        return lines
    
    def generate_xlsx_report(self, workbook, data, wizard_obj):
        for obj in wizard_obj:
            lines = self.get_lines(obj)
            worksheet = workbook.add_worksheet('Reporte de utilidad')
            bold = workbook.add_format({'bold': True, 'align': 'center'})
            text = workbook.add_format({'font_size': 12, 'align': 'center'})

            worksheet.set_column(0, 0, 25)
            worksheet.set_column(1, 2, 25)
            worksheet.set_column(3, 3, 25)
            worksheet.set_column(4, 4, 25)
            worksheet.set_column(5, 5, 25)
            worksheet.set_column(6, 6, 25)
            worksheet.set_column(7, 7, 25)
            worksheet.set_column(8, 8, 25)
            worksheet.set_column(9, 9, 25)
            worksheet.set_column(10, 10, 25)

            worksheet.write('A1', 'Producto', bold)
            worksheet.write('B1', 'Lote', bold)
            worksheet.write('C1', 'Descripcion', bold)
            worksheet.write('D1', 'Cantidad', bold)
            worksheet.write('E1', 'Entregado', bold)
            worksheet.write('F1', 'Facturado', bold)
            worksheet.write('G1', 'Unidad de medida', bold)
            worksheet.write('H1', 'Precio unitario', bold)
            worksheet.write('I1', 'Impuestos', bold)
            worksheet.write('J1', 'Descuento', bold)
            worksheet.write('K1', 'Subtotal', bold)
            row = 1
            col = 0
            for res in lines:
                worksheet.write(row, col, res['Producto'], text)
                worksheet.write(row, col + 1, res['Lote'], text)
                worksheet.write(row, col + 2, res['Descripcion'], text)
                worksheet.write(row, col + 3, res['Cantidad'], text)
                worksheet.write(row, col + 4, res['Entregado'], text)
                worksheet.write(row, col + 5, res['Facturado'], text)
                worksheet.write(row, col + 6, res['UnidadDemedida'], text)
                worksheet.write(row, col + 7, str(self.env.user.company_id.currency_id.symbol) + str(res['PrecioUnitario']), text)
                impuestos_str = ', '.join([f'{nombre}: {monto}' for nombre, monto in res['Impuestos']])
                worksheet.write(row, col + 8, impuestos_str, text)
                worksheet.write(row, col + 9, res['Descuento'], text)
                worksheet.write(row, col + 10, str(self.env.user.company_id.currency_id.symbol) + str(res['Subtotal']), text)
                row = row + 1