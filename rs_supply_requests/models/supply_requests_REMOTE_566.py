# -*- coding: utf-8 -*-
import string
from odoo import models, fields

class SupplyRequests(models.Model):
    _name = 'supply.requests'
    _description = 'Supply Requests'

    so_line_id = fields.Integer(string="ID")
    so_reference = fields.Char(string="SO Ref")
    product_name = fields.Char(string="Product Name")
    quantity = fields.Integer(string="Quantity")
    sale_price = fields.Float(string="Sale Price")
    subtotal = fields.Float(string="Subtotal")
    status = fields.Char(string="Status")
    product_id = fields.Integer(string=" Product ID")
    vendor_id = fields.Integer(string="Vendor ID")
    currency_id = fields.Integer(string="Currency ID")
    product_uom_id = fields.Integer(string="Product UOM ID")
    sale_reference_id = fields.Integer("Sale Reference")
    customer = fields.Char(string="Customer")
    salesperson= fields.Char(string="Salesperson")
    x_customer_reference = fields.Char(string="C-Reference No")
    x_project_sales = fields.Many2one("project.project", string="Project Number") 
    x_document_name = fields.Char(string="Report PDF Project Number")
    rs_analytic_account_id = fields.Many2one("account.analytic.account", string="Analytic Account")
    
    def create_purchase_order(self):            
        selected_ids = self.env.context.get('active_ids', [])
        selected_records = self.env['supply.requests'].browse(selected_ids)
    
        so_references = [] #create a list for vendors
        for rec in selected_records: 
            so_references.append(rec['so_reference']) 
        
        so_reference_list_set = set(so_references)
        so_references_unique_list = (list(so_reference_list_set)) # create a uniq list for vendors
        if(len(so_references_unique_list)==1):
            purchase_order_q = self.env['purchase.order'].create({
                                                        'partner_id':94654,
                                                        'origin':"",
                                                        'x_customer_ref':self[0].x_customer_reference,
                                                        'x_project_purchase':self[0].x_project_sales['id'],
                                                        'x_document_name':self[0].x_document_name,
                                                        })
            for rec in selected_records:
                self.env['purchase.order.line'].create({'partner_id':rec['vendor_id'] , 'name':rec['product_name'],   # create purchase order lines 
                                                'product_qty':rec['quantity'] ,
                                                'price_subtotal':rec['subtotal'], 'order_id':purchase_order_q.id,
                                                'currency_id':rec['currency_id'], 'product_uom_qty':rec['quantity'], 
                                                'product_uom':rec['product_uom_id'],'product_id':rec['product_id'], 
                                                'price_total':rec['subtotal'],
                                                'account_analytic_id' : self[0].rs_analytic_account_id['id'],
                                                })
            self.env.cr.commit()     
        
            return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'purchase.order',
            'res_id':purchase_order_q.id,
            'view_id ref="purchase.order.tree_view"': '',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'nodestroy': True
            }
        else:
            return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'danger',
                'sticky': False,
                'message': "You cannot select different sale orders! Please select same sale order records.",
            }
        }
