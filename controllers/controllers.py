# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import json,request


class Truffleapp(http.Controller):
    @http.route(['/truffleapp/getProduct','/truffleapp/getProduct/<int:prodid>'] ,auth='public',type="http")
    def getProduct(self,prodid=None,**kw):
        if prodid:
            domain=[("id","=",prodid)]
        else:
            domain=[]
        proddata= http.request.env["truffleapp.productmodel"].sudo().search_read(domain,["name","price","stock","category","path_category","weight","mesure","quality"])
        data={"status":200,"data":proddata}
        return http.Response(json.dumps(data).encode("utf8"),mimetype="application/json")

    @http.route(['/truffleapp/getCategories','/truffleapp/getCategories/<int:catid>'] ,auth='public',type="http")
    def getCategories(self,catid=None,**kw):
        if catid:
            domain=[("id","=",catid)]
        else:
            domain=[]
        catdata= http.request.env["truffleapp.categorymodel"].sudo().search_read(domain,["name","parent_category","child_categories","category_path"])
        data={"status":200,"data":catdata}
        return http.Response(json.dumps(data).encode("utf8"),mimetype="application/json")
    
    @http.route(['/truffleapp/getOrders','/truffleapp/getOrders/<int:ordid>'] ,auth='public',type="http")
    def getOrders(self,ordid=None,**kw):
        if ordid:
            domain=[("id","=",ordid)]
        else:
            domain=[]
        ordid= http.request.env["truffleapp.ordermodel"].sudo().search_read(domain,["name","data","orderLine","iva_percentage","total_without_iva","total_amount","client","state","invoice"])
        for order in ordid:
            order['data'] = order['data'].isoformat() if order.get('data') else None
        data={"status":200,"data":ordid}
        return http.Response(json.dumps(data).encode("utf8"),mimetype="application/json")

    @http.route(['/truffleapp/getOrdersLine/<int:ordid>'] ,auth='public',type="http")
    def getOrderLine(self,ordid=None,**kw):
        if ordid:
            domain=[("order","=",ordid)]
        else:
            domain=[]
        ordid= http.request.env["truffleapp.orderlinemodel"].sudo().search_read(domain,["product","quantity","weight","mesure","price_unit","price_subtotal","order"])
        data={"status":200,"data":ordid}
        return http.Response(json.dumps(data).encode("utf8"),mimetype="application/json")
    
    @http.route(['/truffleapp/getInvoices','/truffleapp/getInvoices/<int:ordid>'] ,auth='public',type="http")
    def getInvoices(self,ordid=None,**kw):
        if ordid:
            domain=[("id","=",ordid)]
        else:
            domain=[]
        ordid= http.request.env["truffleapp.facturamodel"].sudo().search_read(domain,["name","date","lines","total_amount","iva_percentage","total_without_iva","state","clients","active","order"])
        for order in ordid:
            order['date'] = order['date'].isoformat() if order.get('date') else None
        data={"status":200,"data":ordid}
        return http.Response(json.dumps(data).encode("utf8"),mimetype="application/json")
    
    @http.route(['/truffleapp/getInvoices/<int:ordid>'] ,auth='public',type="http")
    def getInvoicesLine(self,ordid=None,**kw):
        if ordid:
            domain=[("invoice","=",ordid)]
        else:
            domain=[]
        ordid= http.request.env["truffleapp.facturalineamodel"].sudo().search_read(domain,["product","quantity","weigth","mesure","price_unit","price_subtotal","invoice"])
        data={"status":200,"data":ordid}
        return http.Response(json.dumps(data).encode("utf8"),mimetype="application/json")
    
    @http.route(['/truffleapp/getClients','/truffleapp/getClients/<int:partnerid>'], auth='public', type="http")
    def getClients(self, partnerid=None, **kw):
        if partnerid:
            domain = [("id", "=", partnerid)]
        else:
            domain = []
        partner_data = http.request.env["res.partner"].sudo().search_read(domain, ["id", "name"])
        
        data = {"status": 200, "data": partner_data}
        return http.Response(json.dumps(data).encode("utf8"), mimetype="application/json")




    @http.route('/truffleapp/addOrder', auth='public', type="json", methods=["POST"])
    def addOrder(self, **kw):
        try:
            # Obtener datos de la solicitud JSON
            data = request.httprequest.json
            # Validar que se proporciona el ID del cliente y al menos una línea de orden
            if 'client_id' not in data or 'order_lines' not in data or not data['order_lines']:
                return {"status": 400, "error": "Se requiere el ID del cliente y al menos una línea de orden."}
        
            # Crear las líneas de orden
            order_lines_data = [{'product': line['product'], 'quantity': line['quantity']} for line in data['order_lines']]
            order_lines = request.env['truffleapp.orderlinemodel'].sudo().create(order_lines_data)

            # Crear la orden y asociar las líneas de orden a la orden
            new_order = request.env['truffleapp.ordermodel'].sudo().create({
                'client': data['client_id'],
                'iva_percentage': data['iva'],
                'orderLine': [(6, 0, order_lines.ids)],  # Asociar las líneas de orden a la orden
                # Puedes agregar más campos de la orden según sea necesario
            })
            return {
                "status": 201,
                "order_id": new_order.id,
            }
        except Exception as e:
            return {"status": 404, "error": str(e)}

    @http.route('/truffleapp/updateOrder', auth='public', type="json", methods=["PUT"])
    def updateOrder(self, **kw):
        try:
            # Obtener datos de la solicitud JSON
            data = request.httprequest.json
            # Validar que se proporciona el ID de la orden y al menos una línea de orden
            if 'order_id' not in data or 'order_lines' not in data or not data['order_lines']:
                return {"status": 400, "error": "Se requiere el ID de la orden y al menos una línea de orden."}
            # Obtener la orden existente
            order_id = data['order_id']
            existing_order = request.env['truffleapp.ordermodel'].sudo().browse(order_id)
            if not existing_order:
                return {"status": 404, "error": f"No se encontró la orden con ID {order_id}."}
            # Actualizar la orden
            existing_order.write({
                'iva_percentage': data.get('iva', existing_order.iva_percentage),
                'state':data["state"]
                # Puedes agregar más campos que desees actualizar
            })
            # Actualizar las líneas de orden
            order_lines_data = [{'product': line['product'], 'quantity': line['quantity']} for line in data['order_lines']]
            existing_order.orderLine.unlink()  # Eliminar las líneas de la orden existentes
            order_lines = request.env['truffleapp.orderlinemodel'].sudo().create(order_lines_data)
            existing_order.write({
                'orderLine': [(6, 0, order_lines.ids)],  # Asociar las nuevas líneas de orden a la orden
            })
            return {
                "status": 200,
                "message": "Orden actualizada exitosamente.",
            }
        except Exception as e:
            return {"status": 404, "error": str(e)}

    @http.route('/truffleapp/deleteOrder', auth='public', type="json", methods=["DELETE"])
    def deleteOrder(self, **kw):
        response = request.httprequest.json
        try:
            catdata = http.request.env["truffleapp.ordermodel"].sudo().search([("id", "=", response["id"])])
            catdata.sudo().unlink()
            data = {
                "status": 200,
                "message": "orden eliminada exitosamente."
            }
        except Exception as e:
            data = {
                "status": 404,
                "error": str(e)  # Convertir la excepción a cadena para incluir en la respuesta
            }
        return data

    @http.route('/truffleapp/addCategory' ,auth='public',type="json",methods=["POST"])
    def addCategory(self,**kw):
        response= request.httprequest.json
        try:
            result=http.request.env["truffleapp.categorymodel"].sudo().create(response)
            data={
                "status":201,
                "id":result.id
            }
            return data
        except Exception as e:
            data={
                "status":404,
                "error":e
            }
            return data
        

    @http.route('/truffleapp/updateCategory' ,auth='public',type="json",methods=["PUT"])
    def updateCategory(self,**kw):
        response=request.httprequest.json
        try:
            catdata=http.request.env["truffleapp.categorymodel"].sudo().search([("id","=",response["id"])])
            catdata.sudo().write(response)
            data={
                "status":201,
                "id":catdata.id
            }
        except Exception as e:
            data={
                "status":404,
                "error":e
            }
            return data
    
    @http.route('/truffleapp/deleteCategory', auth='public', type="json", methods=["DELETE"])
    def deleteCategory(self, **kw):
        response = request.httprequest.json
        try:
            catdata = http.request.env["truffleapp.categorymodel"].sudo().search([("id", "=", response["id"])])
            catdata.sudo().unlink()
            data = {
                "status": 200,
                "message": "Categoría eliminada exitosamente."
            }
        except Exception as e:
            data = {
                "status": 404,
                "error": str(e)  # Convertir la excepción a cadena para incluir en la respuesta
            }
        return data
