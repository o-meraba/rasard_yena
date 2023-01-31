# -*- coding: utf-8 -*-

from email.policy import strict
import string
from odoo import models

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def send_supply_page(self):
        sale_order_lines = self.env['sale.order.line'].search([('order_id','=',self.id)]) # list sale order lines from active sale order quotation
        so_lines = [] # create a new list for sale_order_lines
        for so_line in sale_order_lines: 
            so_info = {
                    'product_id':so_line.product_id.id,
                    'currency_id': so_line.currency_id.id,
                    'product_uom': so_line.product_uom.id,
                    'sale_reference':self.name,
                    'sale_reference_id':self.id,
                    'product_name': so_line.name,
                    'quantity':so_line.product_uom_qty,
                    'sale_price': so_line.price_unit,
                    'subtotal': so_line.price_subtotal,
                    'x_customer_reference' : self.x_customer_reference,
                    'x_project_sales' : self.x_project_sales['id'],
                    'x_document_name' : self.x_document_name,
                    'rs_analytic_account_id' : self.analytic_account_id['id'],
                    }
            so_lines.append(so_info) # add sale_order line to so_lines list
            
        if self.env['supply.requests'].search_count([('sale_reference_id','=',self.id)]) == 0:    
            for so_line in so_lines:
                self.env['supply.requests'].create({'product_id':so_line['product_id'], 
                                            'currency_id':so_line['currency_id'],
                                            'product_uom_id':so_line['product_uom'],
                                            'so_reference':so_line['sale_reference'],   # create purchase order lines 
                                            'product_name':so_line['product_name'] ,
                                            'quantity':so_line['quantity'],
                                            'sale_price':so_line['sale_price'], 'subtotal':so_line['subtotal'], 
                                            'sale_reference_id':so_line['sale_reference_id'],
                                            'customer':self.partner_id.name,
                                            'salesperson':self.user_id.partner_id.name,
                                            'x_customer_reference':so_line['x_customer_reference'],
                                            'x_project_sales':so_line['x_project_sales'],
                                            'x_document_name':so_line['x_document_name'],
                                            'rs_analytic_account_id':so_line['rs_analytic_account_id'],
                                            })
                self.env.cr.commit()
        else:
            supply_requests=self.env['supply.requests'].search([('sale_reference_id','=',self.id)])
            for supply_request in supply_requests:
                self.env['supply.requests'].browse(supply_request.id).unlink()
                self.env.cr.commit()
            
            for so_line in so_lines:
                supp_req = self.env['supply.requests'].create({'product_id':so_line['product_id'], 
                                                'currency_id':so_line['currency_id'],
                                                'product_uom_id':so_line['product_uom'],
                                                'so_reference':so_line['sale_reference'],   # create purchase order lines 
                                                'product_name':so_line['product_name'] ,
                                                'quantity':so_line['quantity'], 
                                                'sale_price':so_line['sale_price'], 'subtotal':so_line['subtotal'], 
                                                'sale_reference_id':so_line['sale_reference_id'],
                                                'customer':self.partner_id.name,
                                                'salesperson':self.user_id.partner_id.name,
                                                'x_customer_reference':so_line['x_customer_reference'],
                                                'x_project_sales':so_line['x_project_sales'],
                                                'x_document_name':so_line['x_document_name'],
                                                'rs_analytic_account_id':so_line['rs_analytic_account_id'],
                                                })
        
        return {
        'name' :"Talepler",
        'view_type': 'form',
        'view_mode': 'tree,form',
        'res_model': 'supply.requests',
        'view_id ref="supply.requests.tree_view"': '',
        'type': 'ir.actions.act_window',
        'target': 'current',
        'nodestroy': True
    }