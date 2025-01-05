from odoo import models, fields, api, _
import qrcode
import base64
import io

class AccountMove(models.Model):
    _inherit = 'account.move'

    qr_invoice = fields.Binary(string="Código QR", compute='_compute_qr_invoice', store=True)
    total_quantity = fields.Float(string="Total Cantidad", compute='_compute_total_quantity', store=True,
                                     help="Total de la cantidad de productos en la factura")
    serie_factura = fields.Char(string="Serie Factura", compute='_compute_serie_correlativo', store=True)
    correlativo_factura = fields.Char(string="Correlativo Factura", compute='_compute_serie_correlativo', store=True)
    sales_team_test_id = fields.Many2one('sales.team.test', string="Canal de Ventas")
    invoice_date_issue = fields.Datetime(string="Fecha de Emisión", readonly=True, index=True, copy=False,
                                         help="Fecha de emisión de la factura")
    @api.onchange('date')
    def _onchange_date(self):
        self.invoice_date_issue = fields.Datetime.now()

    def action_post(self):
        res = super(AccountMove, self).action_post()
        for move in self:
            if not move.invoice_date_issue:
                move.invoice_date_issue = fields.Datetime.now()
        return res
    
    @api.depends('invoice_line_ids.quantity')
    def _compute_total_quantity(self):
        for record in self:
            record.total_quantity = sum(record.invoice_line_ids.mapped('quantity'))

    @api.depends('state', 'amount_total', 'partner_id', 'invoice_date', 'name', 'total_quantity')
    def _compute_qr_invoice(self):
        for inv in self:
            if inv.state == 'posted':
                qr_string = f"{inv.name}|{inv.partner_id.name}|{inv.invoice_date}|{inv.total_quantity}|{inv.amount_total}"
                inv.qr_invoice = inv.generate_qr_code(qr_string)['x_qr_invoice']
            else:
                inv.qr_invoice = False

    def generate_qr_code(self, qr_string):
        qr = qrcode.QRCode(version=4, box_size=4, border=1)
        qr.add_data(qr_string)
        qr.make(fit=True)
        img = qr.make_image()
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue())
        return {'x_qr_invoice': img_str}

    @api.depends('name')
    def _compute_serie_correlativo(self):
        for inv in self:
            if inv.name and inv.name != '/':
                name_parts = inv.name.split('/')
                if len(name_parts) >= 2:
                    inv.serie_factura = name_parts[0] + name_parts[1]
                    inv.correlativo_factura = name_parts[-1]
                else:
                    inv.serie_factura = False
                    inv.correlativo_factura = False
            else:
                inv.serie_factura = False
                inv.correlativo_factura = False