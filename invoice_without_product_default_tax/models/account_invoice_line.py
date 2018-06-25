# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools import float_is_zero, float_compare

class AccountInvoiceLineInh(models.Model):
    _inherit = "account.invoice.line"

    @api.onchange('name')
    def _onchange_line_name(self):
        
        partner = self.invoice_id.partner_id
        company = self.invoice_id.company_id
        currency = self.invoice_id.currency_id
        fpos = self.invoice_id.fiscal_position_id
        type = self.invoice_id.type
        if not partner:
            warning = {
                    'title': _('Warning!'),
                    'message': _('You must first select a partner!'),
                }
            return {'warning': warning}
        product = self.env['product.product'].search([('active','=',True)],limit=1)
        account = self.get_invoice_line_account(type, product, fpos, company)
        if account:
            self.account_id = account.id
        self._get_taxes_line(product)

        if company and currency:
            if company.currency_id != currency:
                self.price_unit = self.price_unit * currency.with_context(dict(self._context or {}, date=self.invoice_id.date_invoice)).rate


    def _get_taxes_line(self,product):
        """ Used in on_change to set taxes and price."""
        if self.invoice_id.type in ('out_invoice', 'out_refund'):
            taxes = product.taxes_id or self.account_id.tax_ids
        else:
            taxes = product.supplier_taxes_id or self.account_id.tax_ids

        # Keep only taxes of the company
        company_id = self.company_id or self.env.user.company_id
        taxes = taxes.filtered(lambda r: r.company_id == company_id)

        self.invoice_line_tax_ids = fp_taxes = self.invoice_id.fiscal_position_id.map_tax(taxes, product, self.invoice_id.partner_id)

        fix_price = self.env['account.tax']._fix_tax_included_price
        if self.invoice_id.type in ('in_invoice', 'in_refund'):
            prec = self.env['decimal.precision'].precision_get('Product Price')
            if not self.price_unit or float_compare(self.price_unit, product.standard_price, precision_digits=prec) == 0:
                self.price_unit = fix_price(product.standard_price, taxes, fp_taxes)
        else:
            self.price_unit = fix_price(product.lst_price, taxes, fp_taxes)
