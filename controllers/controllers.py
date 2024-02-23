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
            domain=[("id","=",ordid)]
        else:
            domain=[]
        ordid= http.request.env["truffleapp.orderlinemodel"].sudo().search_read(domain,["product","quantity","weight","mesure","price_unit","price_subtotal"])
        data={"status":200,"data":ordid}
        return http.Response(json.dumps(data).encode("utf8"),mimetype="application/json")

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
    
    @http.route(['/truffleapp/getInvoices','/truffleapp/getInvoices/<int:ordid>'] ,auth='public',type="http")
    def getInvoices(self,ordid=None,**kw):
        if ordid:
            domain=[("id","=",ordid)]
        else:
            domain=[]
        ordid= http.request.env["truffleapp.facturamodel"].sudo().search_read(domain,["name","date","lines","total_amount","iva_percentage","total_without_iva","state","clients","active"])
        for order in ordid:
            order['date'] = order['date'].isoformat() if order.get('date') else None
        data={"status":200,"data":ordid}
        return http.Response(json.dumps(data).encode("utf8"),mimetype="application/json")


    # @http.route('/truffleapp/deleteCategory' ,auth='public',type="json",methods=["DELETE"])
    # def deleteCategory(self,**kw):
    #     response=request.httprequest.json
    #     try:
    #         catdata=http.request.env["truffleapp.categorymodel"].sudo().search[[("id","=",response["id"])]]
    #         catdata.sudo().unlink(response)
    #         data = {
    #                 "status": 200,
    #                 "message": "Categoría eliminada exitosamente."
    #             }
    #     except Exception as e:
    #         data={
    #             "status":404,
    #             "error":e
    #         }
    #         return data